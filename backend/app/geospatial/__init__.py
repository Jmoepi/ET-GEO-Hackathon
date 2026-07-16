"""
Geospatial Processing Pipeline
Processes ET-GEO raster data and vineyard block geometries.
"""
import numpy as np
from typing import Optional
from dataclasses import dataclass


@dataclass
class BlockStatistics:
    block_id: str
    mean: float
    median: float
    min_val: float
    max_val: float
    std: float
    pixel_count: int


def extract_block_statistics(raster_data: np.ndarray, nodata: Optional[float] = None) -> BlockStatistics:
    if nodata is not None:
        mask = raster_data != nodata
        valid = raster_data[mask]
    else:
        valid = raster_data[~np.isnan(raster_data)]

    if len(valid) == 0:
        return BlockStatistics(
            block_id="",
            mean=0.0,
            median=0.0,
            min_val=0.0,
            max_val=0.0,
            std=0.0,
            pixel_count=0,
        )

    return BlockStatistics(
        block_id="",
        mean=float(np.mean(valid)),
        median=float(np.median(valid)),
        min_val=float(np.min(valid)),
        max_val=float(np.max(valid)),
        std=float(np.std(valid)),
        pixel_count=int(len(valid)),
    )


def calculate_water_deficit(eto: float, eta: float) -> float:
    return eto - eta


def calculate_et_ratio(eta: float, eto: float) -> float:
    if eto == 0:
        return 0.0
    return eta / eto


def calculate_ndvi_trend(ndvi_current: float, ndvi_previous: float) -> float:
    return ndvi_current - ndvi_previous


def calculate_soil_moisture_index(current: float, seasonal_avg: float) -> float:
    if seasonal_avg == 0:
        return 0.0
    return current / seasonal_avg
