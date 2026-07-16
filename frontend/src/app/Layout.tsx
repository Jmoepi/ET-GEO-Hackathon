import { NavLink, Outlet } from "react-router-dom";
import { cn } from "@/utils/lib";
import { useUIStore } from "@/state/store";
import {
  LayoutDashboard,
  Map,
  Layers,
  ListChecks,
  Bot,
  ChevronLeft,
  ChevronRight,
  Sprout,
} from "lucide-react";

const navItems = [
  { to: "/", icon: LayoutDashboard, label: "Dashboard" },
  { to: "/explorer", icon: Map, label: "Explorer" },
  { to: "/decisions", icon: ListChecks, label: "Decision Centre" },
  { to: "/copilot", icon: Bot, label: "AI Copilot" },
];

export function Sidebar() {
  const { sidebarOpen, toggleSidebar } = useUIStore();

  return (
    <aside
      className={cn(
        "fixed left-0 top-0 h-screen bg-surface-card border-r border-surface-border z-40",
        "flex flex-col transition-all duration-300",
        sidebarOpen ? "w-60" : "w-16"
      )}
    >
      <div className="flex items-center gap-3 px-4 h-16 border-b border-surface-border">
        <Sprout className="w-7 h-7 text-vineyard-500 shrink-0" />
        {sidebarOpen && (
          <span className="font-semibold text-lg text-text-primary whitespace-nowrap">
            VineMind
          </span>
        )}
      </div>

      <nav className="flex-1 py-4 px-2 space-y-1">
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors",
                isActive
                  ? "bg-vineyard-500/15 text-vineyard-500"
                  : "text-text-secondary hover:bg-surface-hover hover:text-text-primary"
              )
            }
          >
            <item.icon className="w-5 h-5 shrink-0" />
            {sidebarOpen && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      <button
        onClick={toggleSidebar}
        className="flex items-center justify-center h-12 border-t border-surface-border text-text-muted hover:text-text-primary transition-colors"
      >
        {sidebarOpen ? <ChevronLeft className="w-5 h-5" /> : <ChevronRight className="w-5 h-5" />}
      </button>
    </aside>
  );
}

export function AppShell() {
  const { sidebarOpen } = useUIStore();

  return (
    <div className="min-h-screen">
      <Sidebar />
      <main
        className={cn(
          "transition-all duration-300 min-h-screen",
          sidebarOpen ? "ml-60" : "ml-16"
        )}
      >
        <div className="p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
