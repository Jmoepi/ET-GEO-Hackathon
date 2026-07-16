import { cn, stressHex, recommendationLabel } from "@/utils/lib";
import { StressBadge } from "./StressBadge";
import type { Recommendation } from "@/utils/types";

interface RecommendationCardProps {
  recommendation: Recommendation;
  blockName: string;
  cultivar?: string;
  onClick?: () => void;
  className?: string;
}

export function RecommendationCard({ recommendation, blockName, cultivar, onClick, className }: RecommendationCardProps) {
  const hex = stressHex(recommendation.confidence * 100);

  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full text-left bg-surface-card rounded-xl border border-surface-border p-4",
        "hover:bg-surface-hover hover:border-surface-border/80 transition-all cursor-pointer",
        className
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-medium text-text-primary">{blockName}</h3>
          {cultivar && <p className="text-sm text-text-muted">{cultivar}</p>}
        </div>
        <StressBadge score={recommendation.confidence * 100} size="sm" showLabel={false} />
      </div>

      <div className="flex items-center gap-2 mb-2">
        <span
          className="text-sm font-semibold"
          style={{ color: hex }}
        >
          {recommendationLabel(recommendation.recommendation_type)}
        </span>
      </div>

      <div className="flex items-center justify-between text-xs text-text-muted">
        <span>Confidence: {(recommendation.confidence * 100).toFixed(0)}%</span>
        <span>{new Date(recommendation.generated_at).toLocaleDateString()}</span>
      </div>
    </button>
  );
}
