import { useEffect } from "react";
import { useAuthStore } from "@/state/store";
import { api } from "@/services/api";

export function AppInit() {
  const { token, setUser, logout } = useAuthStore();

  useEffect(() => {
    if (!token) return;
    api.auth.me()
      .then((user) => setUser(user))
      .catch(() => logout());
  }, [token, setUser, logout]);

  return null;
}
