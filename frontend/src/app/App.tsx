import { Routes, Route } from "react-router-dom";
import { AppShell } from "./Layout";
import { DashboardPage } from "@/pages/Dashboard";
import { ExplorerPage } from "@/pages/Explorer";
import { DecisionCentrePage } from "@/pages/DecisionCentre";
import { CopilotPage } from "@/pages/Copilot";

export function App() {
  return (
    <Routes>
      <Route element={<AppShell />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/explorer" element={<ExplorerPage />} />
        <Route path="/explorer/:blockId" element={<ExplorerPage />} />
        <Route path="/decisions" element={<DecisionCentrePage />} />
        <Route path="/copilot" element={<CopilotPage />} />
      </Route>
    </Routes>
  );
}
