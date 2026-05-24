"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MadLibsInput } from "@/components/portal/MadLibsInput";
import { AgentConsole } from "@/components/simulation/AgentConsole";
import { PortalBackground } from "@/components/portal/PortalBackground";
import { ResultDashboard } from "@/components/result/ResultDashboard";
import { useSimulation } from "@/hooks/useSimulation";
import { adaptSimulationData } from "@/lib/adapter";
import type { RegretScenario, V4DashboardData } from "@/types";

type ViewMode = "form" | "console" | "result";

// V4 Mock data — warm, healing, human
const MOCK_DATA: V4DashboardData = {
  soul_summary:
    "你为了留住晚霞，错过了清晨的列车。平行宇宙里的你拥有了属于自己的车队，但副驾驶上，再也没有当年那个陪你躲雨的人。",
  emotional_metrics: {
    happiness_battery: { reality: 80, parallel: 30, label: "快乐电量" },
    regret_index: { reality: 20, parallel: 65, label: "遗憾指数" },
    peace_of_mind: { reality: 90, parallel: 15, label: "内心平静度" },
  },
  parallel_souvenir: {
    item_name: "一张褪色的头等舱机票",
    description: "这是你在平行宇宙中频繁出差的证明。航程很远，但降落时没人接机。",
    icon_type: "ticket",
  },
  future_letter: {
    greetings: "展信佳：",
    content:
      "我是做出了那个选择的你。不要羡慕我，我现在的体检报告一塌糊涂，昨晚又失眠到了凌晨三点。其实，我时常会偷偷溜到你的世界看你，看你下班后在街角买的那束花，看你安稳的睡眠。照顾好现在的自己，那就是我们最好的结局。",
    signature: "—— 另一个时空的你",
  },
  timeline_nodes: [
    {
      year: 2021,
      reality_snapshot: "在老家按揭了一套小房子，周末和朋友去江边露营。",
      parallel_snapshot: "拿到了人生第一个百万年薪，但确诊了中度抑郁状态。",
      divergence_point: "得失守恒",
    },
    {
      year: 2023,
      reality_snapshot: "升了职，虽然工资涨得慢，但每天下班还能赶上夕阳。",
      parallel_snapshot: "跳槽到更大的平台，开始频繁出差，护照盖满了章。",
      divergence_point: "有些风景，只有慢下来才看得到",
    },
    {
      year: 2025,
      reality_snapshot: "孩子上幼儿园了，周末带他去公园喂鸽子。",
      parallel_snapshot: "拿到了梦寐以求的期权，但体检报告上多了三个箭头。",
      divergence_point: "时间会告诉你，什么才是真正的财富",
    },
  ],
};

export default function PortalPage() {
  const simulation = useSimulation();
  const [view, setView] = useState<ViewMode>("form");

  // Auto-transition to result when simulation completes
  useEffect(() => {
    if (simulation.phase === "complete" && view === "console") {
      const timer = setTimeout(() => setView("result"), 600);
      return () => clearTimeout(timer);
    }
  }, [simulation.phase, view]);

  const handleSubmit = async (scenario: RegretScenario) => {
    setView("console");
    await simulation.start({
      scenario,
      depth: 5,
      include_narrative: true,
    });
  };

  const handleRestart = () => {
    setView("form");
    simulation.reset();
  };

  // Use real data if available, otherwise fall back to mock
  const dashboardData: V4DashboardData =
    simulation.timelineData && simulation.universeState
      ? adaptSimulationData(
          simulation.timelineData,
          simulation.universeState,
          simulation.narrativeData
        )
      : MOCK_DATA;

  return (
    <main className="relative min-h-screen flex flex-col overflow-hidden bg-[#F9F8F6]">
      <PortalBackground />

      <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-4 py-8 sm:py-12">
        {/* Main content */}
        <AnimatePresence mode="wait">
          {view === "form" && (
            <motion.div
              key="form"
              className="w-full max-w-2xl"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -16 }}
              transition={{ delay: 0.1, duration: 0.4 }}
            >
              <MadLibsInput
                onSubmit={handleSubmit}
                isLoading={simulation.isStreaming}
              />
            </motion.div>
          )}

          {view === "console" && (
            <motion.div
              key="console"
              className="w-full max-w-2xl"
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
            >
              <AgentConsole
                events={simulation.events}
                isStreaming={simulation.isStreaming}
              />

              {/* Phase progress */}
              <div className="mt-6 flex items-center justify-center flex-wrap gap-x-5 gap-y-2">
                {(
                  [
                    "planning",
                    "timeline",
                    "analysis",
                    "risk",
                    "narrative",
                    "complete",
                  ] as const
                ).map((phase) => {
                  const agent = getAgentForPhase(phase);
                  const isCurrent = simulation.phase === phase;
                  const isDone = simulation.events.some(
                    (e) => e.status === "complete" && e.agent === agent
                  );

                  return (
                    <div
                      key={phase}
                      className={`flex items-center gap-1.5 text-xs transition-colors duration-300 ${
                        isCurrent
                          ? "text-emerald-700"
                          : isDone
                          ? "text-stone-500"
                          : "text-stone-300"
                      }`}
                    >
                      <div
                        className={`w-1.5 h-1.5 rounded-full transition-colors duration-300 ${
                          isCurrent
                            ? "bg-emerald-500 animate-pulse"
                            : isDone
                            ? "bg-stone-400"
                            : "bg-stone-200"
                        }`}
                      />
                      {getPhaseLabel(phase)}
                    </div>
                  );
                })}
              </div>

              {simulation.error && (
                <div className="mt-4 text-center text-rose-600 text-sm">
                  {simulation.error}
                </div>
              )}
            </motion.div>
          )}

          {view === "result" && (
            <motion.div
              key="result"
              className="w-full"
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.4 }}
            >
              <ResultDashboard data={dashboardData} onRestart={handleRestart} />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Footer */}
        {view !== "result" && (
          <motion.footer
            className="mt-auto pt-10 pb-4 text-center"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
          >
            <p className="text-stone-300 text-[10px] tracking-wider">
              后悔药 v4.0 &middot; 写给平行宇宙的信
            </p>
            <p className="text-stone-200 text-[10px] mt-0.5">
              此系统生成的内容仅为推演，不构成任何人生建议
            </p>
          </motion.footer>
        )}
      </div>
    </main>
  );
}

function getAgentForPhase(phase: string): string {
  const map: Record<string, string> = {
    planning: "planner",
    timeline: "timeline",
    analysis: "macro_economy",
    risk: "risk",
    narrative: "narrative",
  };
  return map[phase] || "";
}

function getPhaseLabel(phase: string): string {
  const map: Record<string, string> = {
    planning: "规划",
    timeline: "时间线",
    analysis: "环境分析",
    risk: "风险评估",
    narrative: "叙事生成",
    complete: "完成",
  };
  return map[phase] || phase;
}
