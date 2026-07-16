import { useBlocks, useStressScore, useRecommendations } from "@/hooks/useApi";
import { MetricCard } from "@/components/ui/MetricCard";
import { StressBadge } from "@/components/ui/StressBadge";
import { recommendationLabel, stressHex } from "@/utils/lib";
import { Droplets, Thermometer, Wind, Leaf, AlertTriangle, CheckCircle } from "lucide-react";

export function DashboardPage() {
  const { data: blocks } = useBlocks();
  const { data: recommendations } = useRecommendations();

  const criticalCount = recommendations?.filter((r) => r.recommendation_type === "irrigate_immediately").length ?? 0;
  const tonightCount = recommendations?.filter((r) => r.recommendation_type === "irrigate_tonight").length ?? 0;
  const totalBlocks = blocks?.length ?? 0;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-text-primary">Dashboard</h1>
          <p className="text-text-secondary mt-1">Vineyard irrigation overview</p>
        </div>
        <div className="text-right">
          <p className="text-sm text-text-muted">Last updated</p>
          <p className="text-sm font-medium text-text-primary">{new Date().toLocaleDateString()}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          label="Total Blocks"
          value={totalBlocks}
          icon={<Layers className="w-5 h-5" />}
        />
        <MetricCard
          label="Critical Alerts"
          value={criticalCount}
          icon={<AlertTriangle className="w-5 h-5" />}
        />
        <MetricCard
          label="Irrigate Tonight"
          value={tonightCount}
          icon={<Droplets className="w-5 h-5" />}
        />
        <MetricCard
          label="Healthy"
          value={totalBlocks - criticalCount - tonightCount}
          icon={<CheckCircle className="w-5 h-5" />}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-surface-card rounded-xl border border-surface-border p-5">
          <h2 className="text-lg font-semibold text-text-primary mb-4">Block Stress Overview</h2>
          <div className="space-y-3">
            {blocks?.map((block) => (
              <BlockStressRow key={block.id} blockId={block.id} blockName={block.name} cultivar={block.cultivar} />
            ))}
            {(!blocks || blocks.length === 0) && (
              <p className="text-text-muted text-sm">No blocks configured yet.</p>
            )}
          </div>
        </div>

        <div className="bg-surface-card rounded-xl border border-surface-border p-5">
          <h2 className="text-lg font-semibold text-text-primary mb-4">Pending Recommendations</h2>
          <div className="space-y-3">
            {recommendations?.slice(0, 5).map((rec) => (
              <div
                key={rec.id}
                className="flex items-center justify-between p-3 bg-surface rounded-lg"
              >
                <div>
                  <p className="text-sm font-medium text-text-primary">
                    {rec.block_id.slice(0, 8)}...
                  </p>
                  <p className="text-xs text-text-muted">
                    {recommendationLabel(rec.recommendation_type)}
                  </p>
                </div>
                <StressBadge score={rec.confidence * 100} size="sm" showLabel={false} />
              </div>
            ))}
            {(!recommendations || recommendations.length === 0) && (
              <p className="text-text-muted text-sm">No pending recommendations.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function Layers(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}>
      <path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z" /><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65" /><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65" />
    </svg>
  );
}

function BlockStressRow({ blockId, blockName, cultivar }: { blockId: string; blockName: string; cultivar?: string | null }) {
  const { data: stress } = useStressScore(blockId);

  return (
    <div className="flex items-center justify-between p-3 bg-surface rounded-lg">
      <div>
        <p className="text-sm font-medium text-text-primary">{blockName}</p>
        <p className="text-xs text-text-muted">{cultivar ?? "Unknown cultivar"}</p>
      </div>
      {stress ? (
        <StressBadge score={stress.stress_score} size="sm" />
      ) : (
        <span className="text-xs text-text-muted">No data</span>
      )}
    </div>
  );
}
