"""
Geospatial Processing Pipeline
Processes ET-GEO GeoTIFF rasters and vineyard block geometries.
Aggregates raster values per block and generates analytical features.
"""
import os
import json
from datetime import date
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field
import structlog

logger = structlog.get_logger()


@dataclass
class BlockMetrics:
    block_id: str
    block_name: str
    eta: Optional[float] = None
    eto: Optional[float] = None
    kc: Optional[float] = None
    ndvi: Optional[float] = None
    soil_moisture: Optional[float] = None
    observation_date: date = field(default_factory=date.today)
    data_source: str = "et-geo"
    processing_notes: list[str] = field(default_factory=list)


def extract_raster_stats(raster_path: str, geometry_geojson: Optional[str] = None) -> dict:
    try:
        import rasterio
        from rasterio.mask import mask as rasterio_mask
        import numpy as np
        import geopandas as gpd
        from shapely.geometry import shape

        with rasterio.open(raster_path) as src:
            if geometry_geojson:
                geom = shape(json.loads(geometry_geojson))
                gdf = gpd.GeoDataFrame({"geometry": [geom]}, crs="EPSG:4326")

                if gdf.crs != src.crs:
                    gdf = gdf.to_crs(src.crs)

                geom_list = [geom.__geo_interface__ for geom in gdf.geometry]

                try:
                    out_image, _ = rasterio_mask(src, geom_list, crop=True)
                    data = out_image[0]
                except ValueError:
                    data = src.read(1)
            else:
                data = src.read(1)

            nodata = src.nodata
            if nodata is not None:
                data = data[data != nodata]
            data = data[~np.isnan(data)]

            if len(data) == 0:
                return {"mean": 0.0, "median": 0.0, "min": 0.0, "max": 0.0, "std": 0.0, "pixel_count": 0}

            return {
                "mean": float(np.mean(data)),
                "median": float(np.median(data)),
                "min": float(np.min(data)),
                "max": float(np.max(data)),
                "std": float(np.std(data)),
                "pixel_count": int(len(data)),
            }

    except ImportError as e:
        logger.warning("Geospatial library not available", error=str(e))
        return {"mean": 0.0, "median": 0.0, "min": 0.0, "max": 0.0, "std": 0.0, "pixel_count": 0, "error": str(e)}
    except Exception as e:
        logger.error("Raster processing error", path=raster_path, error=str(e))
        return {"mean": 0.0, "median": 0.0, "min": 0.0, "max": 0.0, "std": 0.0, "pixel_count": 0, "error": str(e)}


def process_block_from_rasters(
    block_id: str,
    block_name: str,
    geometry_geojson: Optional[str],
    eta_path: Optional[str] = None,
    eto_path: Optional[str] = None,
    kc_path: Optional[str] = None,
    ndvi_path: Optional[str] = None,
    observation_date: date = None,
) -> BlockMetrics:
    if observation_date is None:
        observation_date = date.today()

    metrics = BlockMetrics(
        block_id=block_id,
        block_name=block_name,
        observation_date=observation_date,
    )

    if eta_path and os.path.exists(eta_path):
        stats = extract_raster_stats(eta_path, geometry_geojson)
        metrics.eta = stats.get("mean")
        if stats.get("pixel_count", 0) == 0:
            metrics.processing_notes.append("ETa: no pixels in block geometry")

    if eto_path and os.path.exists(eto_path):
        stats = extract_raster_stats(eto_path, geometry_geojson)
        metrics.eto = stats.get("mean")
        if stats.get("pixel_count", 0) == 0:
            metrics.processing_notes.append("ETo: no pixels in block geometry")

    if kc_path and os.path.exists(kc_path):
        stats = extract_raster_stats(kc_path, geometry_geojson)
        metrics.kc = stats.get("mean")

    if ndvi_path and os.path.exists(ndvi_path):
        stats = extract_raster_stats(ndvi_path, geometry_geojson)
        metrics.ndvi = stats.get("mean")

    return metrics


def load_block_geometry(geometry_path: str) -> Optional[str]:
    try:
        import geopandas as gpd

        gdf = gpd.read_file(geometry_path)
        if gdf.crs and str(gdf.crs) != "EPSG:4326":
            gdf = gdf.to_crs("EPSG:4326")

        if len(gdf) > 0:
            return gdf.geometry.iloc[0].__geo_interface__
        return None
    except Exception as e:
        logger.error("Failed to load geometry", path=geometry_path, error=str(e))
        return None


def list_raster_files(data_dir: str, pattern: str = "*.tif") -> dict[str, str]:
    result = {}
    data_path = Path(data_dir)
    if not data_path.exists():
        return result

    for tif_file in data_path.glob(pattern):
        name_lower = tif_file.name.lower()
        if "eta" in name_lower and "eto" not in name_lower:
            result["eta"] = str(tif_file)
        elif "eto" in name_lower:
            result["eto"] = str(tif_file)
        elif "kc" in name_lower:
            result["kc"] = str(tif_file)
        elif "ndvi" in name_lower:
            result["ndvi"] = str(tif_file)

    return result
