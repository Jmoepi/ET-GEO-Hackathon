import { cn } from "@/utils/lib";
import type { ReactNode } from "react";

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  icon?: ReactNode;
  trend?: "up" | "down" | "stable";
  className?: string;
}

export function MetricCard({ label, value, unit, icon, trend, className }: MetricCardProps) {
  return (
    <div className={cn("bg-surface-card rounded-xl border border-surface-border p-4", className)}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm text-text-secondary">{label}</span>
        {icon && <span className="text-text-muted">{icon}</span>}
      </div>
      <div className="flex items-baseline gap-1.5">
        <span className="text-2xl font-semibold font-mono text-text-primary">{value}</span>
        {unit && <span className="text-sm text-text-muted">{unit}</span>}
      </div>
      {trend && (
        <div className={cn("mt-1 text-xs font-medium", trend === "up" ? "text-stress-high" : trend === "down" ? "text-stress-healthy" : "text-text-muted")}>
          {trend === "up" ? "↑ Increasing" : trend === "down" ? "↓ Decreasing" : "→ Stable"}
        </div>
      )}
    </div>
  );
}
