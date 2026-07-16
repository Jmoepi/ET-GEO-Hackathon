import { cn, stressHex } from "@/utils/lib";
import type { FeatureContribution } from "@/utils/types";

interface FeatureBreakdownProps {
  contributors: FeatureContribution[];
  className?: string;
}

export function FeatureBreakdown({ contributors, className }: FeatureBreakdownProps) {
  const available = contributors.filter((c) => c.available);
  const maxWeighted = Math.max(...available.map((c) => c.weighted_score), 0.01);

  return (
    <div className={cn("space-y-3", className)}>
      {contributors.map((c) => {
        const pct = c.available ? (c.weighted_score / maxWeighted) * 100 : 0;
        const hex = c.available ? stressHex(c.normalised_value * 100) : "#64748b";

        return (
          <div key={c.metric}>
            <div className="flex items-center justify-between mb-1">
              <span className="text-sm text-text-secondary capitalize">
                {c.metric.replace(/_/g, " ")}
              </span>
              <div className="flex items-center gap-2 text-sm">
                <span className="font-mono text-text-primary">{c.raw_value.toFixed(2)}</span>
                <span className="text-text-muted">{c.unit}</span>
              </div>
            </div>
            <div className="h-2 bg-surface rounded-full overflow-hidden">
              <div
                className="h-full rounded-full transition-all duration-500"
                style={{
                  width: c.available ? `${pct}%` : "0%",
                  backgroundColor: hex,
                }}
              />
            </div>
            <div className="flex items-center justify-between mt-0.5">
              <span className="text-xs text-text-muted">
                Weight: {(c.weight * 100).toFixed(0)}%
              </span>
              <span className="text-xs text-text-muted">
                Score: {c.weighted_score.toFixed(3)}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
}
