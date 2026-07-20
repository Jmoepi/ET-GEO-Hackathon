import { useEffect, useRef, useState } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";
import { cn, stressHex } from "@/utils/lib";
import type { Block } from "@/utils/types";

mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || "";

interface StressMapEntry {
  stress_score: number;
  stress_category: string;
}

interface VineyardMapProps {
  blocks: Block[];
  stressMap: Map<string, StressMapEntry>;
  selectedBlockId: string | null;
  onBlockClick: (blockId: string) => void;
  className?: string;
}

export function VineyardMap({ blocks, stressMap, selectedBlockId, onBlockClick, className }: VineyardMapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<mapboxgl.Map | null>(null);
  const [mapLoaded, setMapLoaded] = useState(false);

  useEffect(() => {
    if (!mapContainer.current || map.current) return;

    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/mapbox/satellite-streets-v12",
      center: [18.86, -33.93],
      zoom: 11,
    });

    map.current.addControl(new mapboxgl.NavigationControl(), "top-right");
    map.current.addControl(new mapboxgl.FullscreenControl(), "top-right");

    map.current.on("load", () => setMapLoaded(true));

    return () => {
      map.current?.remove();
      map.current = null;
    };
  }, []);

  useEffect(() => {
    if (!map.current || !mapLoaded) return;

    const existingSources = map.current.getStyle().sources;
    if (existingSources["vineyard-blocks"]) return;

    const features: GeoJSON.Feature[] = blocks.map((block) => {
      let geometry: GeoJSON.Geometry;

      if (block.geometry) {
        try {
          geometry = JSON.parse(block.geometry);
        } catch {
          const center = getBlockCenter(block);
          geometry = {
            type: "Point",
            coordinates: [center.lng, center.lat],
          };
        }
      } else {
        const center = getBlockCenter(block);
        geometry = {
          type: "Point",
          coordinates: [center.lng, center.lat],
        };
      }

      const stress = stressMap.get(block.id);

      return {
        type: "Feature" as const,
        id: block.id,
        properties: {
          blockId: block.id,
          name: block.name,
          cultivar: block.cultivar ?? "Unknown",
          stressScore: stress?.stress_score ?? 0,
          stressCategory: stress?.stress_category ?? "no_data",
        },
        geometry,
      };
    });

    map.current.addSource("vineyard-blocks", {
      type: "geojson",
      data: {
        type: "FeatureCollection",
        features,
      },
    });

    map.current.addLayer({
      id: "block-fill",
      type: "fill",
      source: "vineyard-blocks",
      paint: {
        "fill-color": [
          "interpolate",
          ["linear"],
          ["get", "stressScore"],
          0, "#22c55e",
          20, "#22c55e",
          21, "#eab308",
          40, "#eab308",
          41, "#f97316",
          60, "#f97316",
          61, "#ef4444",
          80, "#ef4444",
          81, "#dc2626",
          100, "#dc2626",
        ],
        "fill-opacity": 0.45,
      },
    });

    map.current.addLayer({
      id: "block-outline",
      type: "line",
      source: "vineyard-blocks",
      paint: {
        "line-color": [
          "interpolate",
          ["linear"],
          ["get", "stressScore"],
          0, "#22c55e",
          20, "#22c55e",
          21, "#eab308",
          40, "#eab308",
          41, "#f97316",
          60, "#f97316",
          61, "#ef4444",
          80, "#ef4444",
          81, "#dc2626",
          100, "#dc2626",
        ],
        "line-width": 2,
      },
    });

    map.current.addLayer({
      id: "block-labels",
      type: "symbol",
      source: "vineyard-blocks",
      layout: {
        "text-field": ["get", "name"],
        "text-size": 12,
        "text-anchor": "center",
      },
      paint: {
        "text-color": "#f8fafc",
        "text-halo-color": "#0f1729",
        "text-halo-width": 1.5,
      },
    });

    map.current.addLayer({
      id: "block-points",
      type: "circle",
      source: "vineyard-blocks",
      paint: {
        "circle-radius": 6,
        "circle-color": [
          "interpolate",
          ["linear"],
          ["get", "stressScore"],
          0, "#22c55e",
          20, "#22c55e",
          21, "#eab308",
          40, "#eab308",
          41, "#f97316",
          60, "#f97316",
          61, "#ef4444",
          80, "#ef4444",
          81, "#dc2626",
          100, "#dc2626",
        ],
        "circle-stroke-color": "#0f1729",
        "circle-stroke-width": 2,
      },
    });

    const popup = new mapboxgl.Popup({
      closeButton: false,
      closeOnClick: false,
      className: "vineyard-popup",
    });

    map.current.on("mouseenter", "block-fill", (e) => {
      if (!map.current) return;
      map.current.getCanvas().style.cursor = "pointer";

      const feature = e.features?.[0];
      if (!feature) return;

      const props = feature.properties as Record<string, any>;
      const score = props.stressScore ?? 0;
      const color = stressHex(score);

      popup
        .setLngLat(e.lngLat)
        .setHTML(
          `<div style="background:#1a2332;border:1px solid #2d3a4e;border-radius:8px;padding:10px 14px;color:#f8fafc;font-family:Inter,system-ui,sans-serif;">
            <div style="font-weight:600;margin-bottom:4px;">${props.name}</div>
            <div style="font-size:12px;color:#94a3b8;margin-bottom:6px;">${props.cultivar}</div>
            <div style="display:flex;align-items:center;gap:6px;">
              <span style="width:8px;height:8px;border-radius:50%;background:${color};"></span>
              <span style="font-size:13px;font-weight:500;color:${color};">Score: ${score}</span>
            </div>
          </div>`
        )
        .addTo(map.current);
    });

    map.current.on("mouseleave", "block-fill", () => {
      if (!map.current) return;
      map.current.getCanvas().style.cursor = "";
      popup.remove();
    });

    map.current.on("click", "block-fill", (e) => {
      const feature = e.features?.[0];
      if (feature) {
        const props = feature.properties as Record<string, any>;
        onBlockClick(props.blockId);
      }
    });

    return () => {
      map.current?.removeLayer("block-labels");
      map.current?.removeLayer("block-outline");
      map.current?.removeLayer("block-fill");
      map.current?.removeLayer("block-points");
      map.current?.removeSource("vineyard-blocks");
    };
  }, [mapLoaded, blocks, stressMap, onBlockClick]);

  useEffect(() => {
    if (!map.current || !mapLoaded || !selectedBlockId) return;

    const source = map.current.getSource("vineyard-blocks") as mapboxgl.GeoJSONSource;
    if (!source) return;

    const data = source._data as GeoJSON.FeatureCollection;
    const feature = data.features.find((f) => (f.properties as any)?.blockId === selectedBlockId);
    if (feature && feature.geometry.type === "Polygon") {
      const poly = feature.geometry as GeoJSON.Polygon;
      const coords = poly.coordinates[0];
      if (coords && coords.length > 0) {
        const bounds = new mapboxgl.LngLatBounds();
        coords.forEach((c: number[]) => bounds.extend(c as [number, number]));
        map.current.fitBounds(bounds, { padding: 60, duration: 500 });
      }
    }
  }, [selectedBlockId, mapLoaded]);

  return (
    <div ref={mapContainer} className={cn("w-full h-full rounded-xl overflow-hidden", className)} />
  );
}

function getBlockCenter(block: Block): { lat: number; lng: number } {
  if (block.geometry) {
    try {
      const geom = JSON.parse(block.geometry);
      if (geom.type === "Polygon" && geom.coordinates?.[0]) {
        const coords: number[][] = geom.coordinates[0];
        if (coords.length > 0) {
          let sumLng = 0;
          let sumLat = 0;
          for (const c of coords) {
            sumLng += c[0] ?? 0;
            sumLat += c[1] ?? 0;
          }
          return { lat: sumLat / coords.length, lng: sumLng / coords.length };
        }
      }
      if (geom.type === "Point" && geom.coordinates) {
        return { lat: geom.coordinates[1] ?? -33.93, lng: geom.coordinates[0] ?? 18.86 };
      }
    } catch {}
  }
  return { lat: -33.93 + Math.random() * 0.1, lng: 18.86 + Math.random() * 0.1 };
}
