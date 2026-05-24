"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { AgentEvent, AgentName } from "@/types";
import { cn } from "@/lib/utils";

interface AgentConsoleProps {
  events: AgentEvent[];
  isStreaming: boolean;
}

const agentLabels: Record<AgentName, string> = {
  planner: "规划师",
  timeline: "时间线",
  macro_economy: "经济分析",
  industry: "行业分析",
  risk: "风险评估",
  narrative: "叙事者",
};

const agentColors: Record<AgentName, string> = {
  planner: "text-stone-600",
  timeline: "text-emerald-700",
  macro_economy: "text-slate-500",
  industry: "text-slate-500",
  risk: "text-orange-700",
  narrative: "text-rose-700",
};

const statusLabels: Record<string, string> = {
  thinking: "思考中",
  analyzing: "分析中",
  generating: "书写中",
  complete: "完成",
  error: "出错",
};

export function AgentConsole({ events, isStreaming }: AgentConsoleProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [events]);

  return (
    <div className="w-full paper-card overflow-hidden">
      {/* Header */}
      <div className="flex items-center gap-3 px-5 py-3 border-b border-stone-100">
        <span className="text-xs text-stone-400 tracking-wider">
          推演进度
        </span>
        {isStreaming && (
          <span className="ml-auto text-xs text-emerald-600 animate-gentle-pulse">
            书写中...
          </span>
        )}
      </div>

      {/* Events */}
      <div
        ref={scrollRef}
        className="max-h-[360px] overflow-y-auto p-5 space-y-2"
      >
        <AnimatePresence initial={false}>
          {events.map((event, index) => (
            <motion.div
              key={event.event_id || index}
              initial={{ opacity: 0, y: 4 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className="flex items-start gap-3 text-sm"
            >
              <span
                className={cn(
                  "font-medium whitespace-nowrap shrink-0",
                  agentColors[event.agent] || "text-stone-500"
                )}
              >
                {agentLabels[event.agent] || event.agent}
              </span>

              <span
                className={cn(
                  "text-xs shrink-0",
                  event.status === "complete" && "text-emerald-600",
                  event.status === "error" && "text-rose-600",
                  event.status === "thinking" && "text-stone-400",
                  event.status === "analyzing" && "text-slate-400",
                  event.status === "generating" && "text-orange-600"
                )}
              >
                {statusLabels[event.status] || event.status}
              </span>

              <span className="text-stone-500 text-xs">
                {event.message}
              </span>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Cursor */}
        {isStreaming && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-stone-400 text-xs pt-1"
          >
            <span className="animate-gentle-pulse">○</span>
          </motion.div>
        )}
      </div>
    </div>
  );
}
