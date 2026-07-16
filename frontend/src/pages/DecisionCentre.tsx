import { useRecommendations, useBlocks } from "@/hooks/useApi";
import { RecommendationCard } from "@/components/ui/RecommendationCard";
import { recommendationLabel, cn } from "@/utils/lib";
import { useState } from "react";

const FILTERS = [
  { key: "all", label: "All" },
  { key: "irrigate_immediately", label: "Critical" },
  { key: "irrigate_tonight", label: "Tonight" },
  { key: "delay_irrigation", label: "Delay" },
  { key: "monitor", label: "Monitor" },
  { key: "no_action", label: "No Action" },
];

export function DecisionCentrePage() {
  const [filter, setFilter] = useState("all");
  const { data: recommendations } = useRecommendations(filter === "all" ? undefined : filter);
  const { data: blocks } = useBlocks();

  const blockMap = new Map(blocks?.map((b) => [b.id, b]) ?? []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Decision Centre</h1>
        <p className="text-text-secondary mt-1">Irrigation prioritisation and recommendations</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {FILTERS.map((f) => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            className={cn(
              "px-3 py-1.5 rounded-lg text-sm font-medium transition-colors",
              filter === f.key
                ? "bg-vineyard-500/15 text-vineyard-500 border border-vineyard-500/30"
                : "bg-surface-card text-text-secondary border border-surface-border hover:bg-surface-hover"
            )}
          >
            {f.label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {recommendations?.map((rec) => {
          const block = blockMap.get(rec.block_id);
          return (
            <RecommendationCard
              key={rec.id}
              recommendation={rec}
              blockName={block?.name ?? rec.block_id.slice(0, 8)}
              cultivar={block?.cultivar ?? undefined}
            />
          );
        })}
        {(!recommendations || recommendations.length === 0) && (
          <p className="text-text-muted text-center py-12 col-span-full">No recommendations match this filter.</p>
        )}
      </div>
    </div>
  );
}
