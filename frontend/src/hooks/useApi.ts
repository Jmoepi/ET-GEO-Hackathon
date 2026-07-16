import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/services/api";

export function useVineyards() {
  return useQuery({ queryKey: ["vineyards"], queryFn: () => api.vineyards.list() });
}

export function useVineyard(id: string) {
  return useQuery({ queryKey: ["vineyard", id], queryFn: () => api.vineyards.get(id), enabled: !!id });
}

export function useBlocks(vineyardId?: string) {
  return useQuery({ queryKey: ["blocks", vineyardId], queryFn: () => api.blocks.list(vineyardId) });
}

export function useBlock(id: string) {
  return useQuery({ queryKey: ["block", id], queryFn: () => api.blocks.get(id), enabled: !!id });
}

export function useStressScore(blockId: string) {
  return useQuery({ queryKey: ["stress", blockId], queryFn: () => api.stress.get(blockId), enabled: !!blockId });
}

export function useStressHistory(blockId: string, days = 30) {
  return useQuery({
    queryKey: ["stress-history", blockId, days],
    queryFn: () => api.stress.history(blockId, days),
    enabled: !!blockId,
  });
}

export function useCalculateStress(blockId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: () => api.stress.calculate(blockId),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["stress"] });
      qc.invalidateQueries({ queryKey: ["stress-history", blockId] });
    },
  });
}

export function useRecommendations(status?: string) {
  return useQuery({ queryKey: ["recommendations", status], queryFn: () => api.recommendations.list(status) });
}

export function useRecommendation(blockId: string) {
  return useQuery({ queryKey: ["recommendation", blockId], queryFn: () => api.recommendations.get(blockId), enabled: !!blockId });
}

export function useDecisionEvidence(blockId: string) {
  return useQuery({ queryKey: ["evidence", blockId], queryFn: () => api.recommendations.evidence(blockId), enabled: !!blockId });
}

export function useCopilotChat() {
  return useMutation({ mutationFn: (message: string) => api.copilot.chat(message) });
}
