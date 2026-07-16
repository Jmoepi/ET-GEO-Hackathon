const API_BASE = "/api/v1";

function getAuthHeaders(): HeadersInit {
  const token = localStorage.getItem("vinemind_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...getAuthHeaders(),
      ...options.headers,
    },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.detail ?? `Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  auth: {
    login: (email: string, password: string) =>
      request<{ access_token: string; token_type: string }>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      }),
    me: () => request<import("@/utils/types").User>("/auth/me"),
  },

  vineyards: {
    list: () => request<import("@/utils/types").Vineyard[]>("/vineyards"),
    get: (id: string) => request<import("@/utils/types").Vineyard>(`/vineyards/${id}`),
  },

  blocks: {
    list: (vineyardId?: string) =>
      request<import("@/utils/types").Block[]>(`/blocks${vineyardId ? `?vineyard_id=${vineyardId}` : ""}`),
    get: (id: string) => request<import("@/utils/types").Block>(`/blocks/${id}`),
  },

  stress: {
    get: (blockId: string) => request<import("@/utils/types").StressScore>(`/stress/${blockId}`),
    history: (blockId: string, days = 30) =>
      request<import("@/utils/types").StressScore[]>(`/stress/history/${blockId}?days=${days}`),
    calculate: (blockId: string) =>
      request<import("@/utils/types").StressScore>(`/stress/calculate/${blockId}`, { method: "POST" }),
  },

  recommendations: {
    list: (status?: string) =>
      request<import("@/utils/types").Recommendation[]>(`/recommendations${status ? `?rec_status=${status}` : ""}`),
    get: (blockId: string) => request<import("@/utils/types").Recommendation>(`/recommendations/${blockId}`),
    evidence: (blockId: string) => request<import("@/utils/types").DecisionEvidence>(`/evidence/${blockId}`),
  },

  copilot: {
    chat: (message: string) =>
      request<import("@/utils/types").CopilotResponse>("/copilot/chat", {
        method: "POST",
        body: JSON.stringify({ message }),
      }),
  },
};
