import { cn, stressHex, stressLabel, stressBg } from "@/utils/lib";

interface StressBadgeProps {
  score: number;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
}

export function StressBadge({ score, size = "md", showLabel = true }: StressBadgeProps) {
  const sizeClasses = {
    sm: "text-xs px-2 py-0.5",
    md: "text-sm px-3 py-1",
    lg: "text-base px-4 py-1.5",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full font-medium border",
        sizeClasses[size],
        stressBg(score)
      )}
      style={{ borderColor: stressHex(score) + "40", color: stressHex(score) }}
    >
      <span
        className="w-2 h-2 rounded-full"
        style={{ backgroundColor: stressHex(score) }}
      />
      {showLabel && <span>{stressLabel(score)}</span>}
      <span className="font-mono">{score.toFixed(0)}</span>
    </span>
  );
}
