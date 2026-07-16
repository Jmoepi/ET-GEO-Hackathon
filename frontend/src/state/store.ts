import { create } from "zustand";
import type { User } from "@/utils/types";

interface AuthState {
  token: string | null;
  user: User | null;
  isAuthenticated: boolean;
  login: (token: string, user: User) => void;
  logout: () => void;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: localStorage.getItem("vinemind_token"),
  user: null,
  isAuthenticated: !!localStorage.getItem("vinemind_token"),
  login: (token, user) => {
    localStorage.setItem("vinemind_token", token);
    set({ token, user, isAuthenticated: true });
  },
  logout: () => {
    localStorage.removeItem("vinemind_token");
    set({ token: null, user: null, isAuthenticated: false });
  },
  setUser: (user) => set({ user }),
}));

interface UIState {
  sidebarOpen: boolean;
  selectedBlockId: string | null;
  selectedVineyardId: string | null;
  copilotOpen: boolean;
  toggleSidebar: () => void;
  selectBlock: (id: string | null) => void;
  selectVineyard: (id: string | null) => void;
  toggleCopilot: () => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarOpen: true,
  selectedBlockId: null,
  selectedVineyardId: null,
  copilotOpen: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  selectBlock: (id) => set({ selectedBlockId: id }),
  selectVineyard: (id) => set({ selectedVineyardId: id }),
  toggleCopilot: () => set((s) => ({ copilotOpen: !s.copilotOpen })),
}));
