import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBlocks, useStressScore, useStressHistory, useRecommendation } from "@/hooks/useApi";
import { StressBadge } from "@/components/ui/StressBadge";
import { MetricCard } from "@/components/ui/MetricCard";
import { FeatureBreakdown } from "@/components/ui/FeatureBreakdown";
import { stressHex, recommendationLabel, cn } from "@/utils/lib";
import { Droplets, Thermometer, ArrowLeft, Info } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export function ExplorerPage() {
  const navigate = useNavigate();
  const { data: blocks } = useBlocks();
  const [selectedBlock, setSelectedBlock] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-text-primary">Vineyard Explorer</h1>
        <p className="text-text-secondary mt-1">Browse blocks and inspect water stress data</p>
      </div>

      {!selectedBlock ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {blocks?.map((block) => (
            <BlockCard key={block.id} block={block} onSelect={() => setSelectedBlock(block.id)} />
          ))}
          {(!blocks || blocks.length === 0) && (
            <p className="text-text-muted col-span-full text-center py-12">No blocks found.</p>
          )}
        </div>
      ) : (
        <BlockDetail blockId={selectedBlock} onBack={() => setSelectedBlock(null)} />
      )}
    </div>
  );
}

function BlockCard({ block, onSelect }: { block: { id: string; name: string; cultivar: string | null; area_ha: number | null }; onSelect: () => void }) {
  const { data: stress } = useStressScore(block.id);

  return (
    <button
      onClick={onSelect}
      className={cn(
        "text-left bg-surface-card rounded-xl border p-4 transition-all cursor-pointer",
        "hover:bg-surface-hover",
        stress ? "border-surface-border" : "border-surface-border"
      )}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-medium text-text-primary">{block.name}</h3>
          <p className="text-sm text-text-muted">{block.cultivar ?? "Unknown"}</p>
        </div>
        {stress && <StressBadge score={stress.stress_score} size="sm" />}
      </div>
      {block.area_ha && (
        <p className="text-xs text-text-muted">{block.area_ha} ha</p>
      )}
    </button>
  );
}

function BlockDetail({ blockId, onBack }: { blockId: string; onBack: () => void }) {
  const { data: stress } = useStressScore(blockId);
  const { data: history } = useStressHistory(blockId);
  const { data: recommendation } = useRecommendation(blockId);

  const chartData = history?.map((s) => ({
    date: new Date(s.generated_at).toLocaleDateString("en-ZA", { month: "short", day: "numeric" }),
    score: s.stress_score,
    confidence: s.confidence * 100,
  })).reverse() ?? [];

  return (
    <div className="space-y-6">
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-text-secondary hover:text-text-primary transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span className="text-sm">Back to blocks</span>
      </button>

      <div className="flex items-center gap-4">
        <h2 className="text-xl font-bold text-text-primary">Block Details</h2>
        {stress && <StressBadge score={stress.stress_score} size="md" />}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-surface-card rounded-xl border border-surface-border p-5">
            <h3 className="text-sm font-medium text-text-secondary mb-3">Stress Score History (30 days)</h3>
            {chartData.length > 0 ? (
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2d3a4e" />
                  <XAxis dataKey="date" tick={{ fill: "#64748b", fontSize: 11 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: "#64748b", fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: "#1a2332", border: "1px solid #2d3a4e", borderRadius: 8 }}
                    labelStyle={{ color: "#94a3b8" }}
                  />
                  <Line type="monotone" dataKey="score" stroke="#22c55e" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-text-muted text-sm text-center py-8">No historical data</p>
            )}
          </div>

          {recommendation && (
            <div className="bg-surface-card rounded-xl border border-surface-border p-5">
              <h3 className="text-sm font-medium text-text-secondary mb-2">Current Recommendation</h3>
              <p className="text-lg font-semibold" style={{ color: stressHex(recommendation.confidence * 100) }}>
                {recommendationLabel(recommendation.recommendation_type)}
              </p>
              {recommendation.explanation && (
                <p className="text-sm text-text-secondary mt-2">{recommendation.explanation}</p>
              )}
            </div>
          )}
        </div>

        <div className="space-y-6">
          {stress && (
            <div className="bg-surface-card rounded-xl border border-surface-border p-5">
              <h3 className="text-sm font-medium text-text-secondary mb-4">Feature Breakdown</h3>
              <FeatureBreakdown contributors={stress.contributors} />
            </div>
          )}

          <div className="bg-surface-card rounded-xl border border-surface-border p-5">
            <h3 className="text-sm font-medium text-text-secondary mb-3">Model Info</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-text-muted">Model</span>
                <span className="text-text-primary font-mono">{stress?.model_version ?? "WSM-1.0"}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-text-muted">Confidence</span>
                <span className="text-text-primary font-mono">{stress ? (stress.confidence * 100).toFixed(0) : "--"}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
