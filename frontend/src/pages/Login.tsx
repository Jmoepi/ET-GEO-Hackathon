import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/state/store";
import { api } from "@/services/api";
import { Sprout, Loader2 } from "lucide-react";

export function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await api.auth.login(email, password);
      localStorage.setItem("vinemind_token", res.access_token);
      const user = await api.auth.me();
      login(res.access_token, user);
      navigate("/");
    } catch (err: any) {
      localStorage.removeItem("vinemind_token");
      setError(err?.message || "Invalid email or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-surface px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-vineyard-500/15 mb-4">
            <Sprout className="w-8 h-8 text-vineyard-500" />
          </div>
          <h1 className="text-3xl font-bold text-text-primary">VineMind AI</h1>
          <p className="text-text-secondary mt-2">Irrigation Decision-Support Platform</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-surface-card rounded-2xl border border-surface-border p-8 space-y-5">
          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1.5">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="jeffrey@vinemind.ai"
              className="w-full bg-surface-input border border-surface-border rounded-lg px-4 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-vineyard-500/50 transition-colors"
              required
              autoFocus
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-secondary mb-1.5">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              className="w-full bg-surface-input border border-surface-border rounded-lg px-4 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-vineyard-500/50 transition-colors"
              required
            />
          </div>

          {error && (
            <div className="text-sm text-stress-high bg-stress-high/10 border border-stress-high/20 rounded-lg px-4 py-2.5">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full py-2.5 bg-vineyard-500 text-white rounded-lg text-sm font-semibold hover:bg-vineyard-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : null}
            {loading ? "Signing in..." : "Sign In"}
          </button>

          <p className="text-xs text-text-muted text-center">
            Demo: <span className="text-text-secondary">jeffrey@vinemind.ai</span> / <span className="text-text-secondary">demo1234</span>
          </p>
        </form>
      </div>
    </div>
  );
}
