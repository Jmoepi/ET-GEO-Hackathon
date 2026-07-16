import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatScore(score: number): string {
  return score.toFixed(0);
}

export function stressColor(score: number): string {
  if (score <= 20) return "text-stress-healthy";
  if (score <= 40) return "text-stress-monitor";
  if (score <= 60) return "text-stress-moderate";
  if (score <= 80) return "text-stress-high";
  return "text-stress-critical";
}

export function stressBg(score: number): string {
  if (score <= 20) return "bg-stress-healthy/15";
  if (score <= 40) return "bg-stress-monitor/15";
  if (score <= 60) return "bg-stress-moderate/15";
  if (score <= 80) return "bg-stress-high/15";
  return "bg-stress-critical/15";
}

export function stressBorder(score: number): string {
  if (score <= 20) return "border-stress-healthy";
  if (score <= 40) return "border-stress-monitor";
  if (score <= 60) return "border-stress-moderate";
  if (score <= 80) return "border-stress-high";
  return "border-stress-critical";
}

export function stressHex(score: number): string {
  if (score <= 20) return "#22c55e";
  if (score <= 40) return "#eab308";
  if (score <= 60) return "#f97316";
  if (score <= 80) return "#ef4444";
  return "#dc2626";
}

export function stressLabel(score: number): string {
  if (score <= 20) return "Healthy";
  if (score <= 40) return "Monitor";
  if (score <= 60) return "Moderate";
  if (score <= 80) return "High Stress";
  return "Critical";
}

export function recommendationLabel(type: string): string {
  const map: Record<string, string> = {
    irrigate_immediately: "Irrigate Immediately",
    irrigate_tonight: "Irrigate Tonight",
    delay_irrigation: "Delay Irrigation",
    monitor: "Monitor",
    no_action: "No Action",
  };
  return map[type] ?? type;
}

export function priorityColor(priority: string): string {
  if (priority === "critical") return "text-stress-critical";
  if (priority === "high") return "text-stress-high";
  if (priority === "moderate") return "text-stress-moderate";
  return "text-stress-monitor";
}
