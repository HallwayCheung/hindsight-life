"use client";

import { motion } from "framer-motion";
import { SoulSummary } from "./SummaryPanel";
import { EmotionalBattery } from "./RadarChart";
import { TimelineCards } from "./NodeComparison";
import { SouvenirCard } from "./InventorySection";
import { FutureLetter } from "./FutureLetter";
import type { V4DashboardData } from "@/types";

interface ResultDashboardProps {
  data: V4DashboardData;
  onRestart: () => void;
}

function SectionLabel({ label }: { label: string }) {
  return (
    <div className="flex items-center gap-3 mb-6">
      <div className="w-1 h-4 rounded-full bg-stone-300" />
      <h2 className="text-xs text-stone-400 tracking-[0.2em] uppercase">
        {label}
      </h2>
      <div className="h-px flex-1 bg-stone-200" />
    </div>
  );
}

export function ResultDashboard({ data, onRestart }: ResultDashboardProps) {
  return (
    <div className="w-full min-h-screen">
      <div className="max-w-2xl mx-auto px-4 py-8 sm:py-12 space-y-12 sm:space-y-16">
        {/* ── Header ── */}
        <motion.header
          className="text-center space-y-3"
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <p className="text-[11px] text-stone-400 tracking-[0.3em] uppercase">
            推演完成
          </p>
          <h1 className="font-serif text-2xl sm:text-3xl font-light text-stone-700 tracking-wide">
            平行宇宙观测报告
          </h1>
          <div className="mx-auto w-16 h-px bg-stone-200" />
        </motion.header>

        {/* ── Soul Summary ── */}
        <section>
          <SectionLabel label="灵魂摘要" />
          <SoulSummary text={data.soul_summary} />
        </section>

        {/* ── Emotional Metrics ── */}
        <section>
          <SectionLabel label="情感电量" />
          <div className="paper-card p-6 sm:p-8">
            <EmotionalBattery metrics={data.emotional_metrics} />
          </div>
        </section>

        {/* ── Timeline ── */}
        <section>
          <SectionLabel label="命运节点" />
          <TimelineCards nodes={data.timeline_nodes} />
        </section>

        {/* ── Parallel Souvenir ── */}
        <section>
          <SectionLabel label="平行纪念品" />
          <SouvenirCard souvenir={data.parallel_souvenir} />
        </section>

        {/* ── Future Letter ── */}
        <section>
          <SectionLabel label="来自平行宇宙的信" />
          <FutureLetter letter={data.future_letter} />
        </section>

        {/* ── Restart ── */}
        <motion.div
          className="text-center pt-4 pb-8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
        >
          <button
            onClick={onRestart}
            className="text-sm text-stone-400 hover:text-stone-600 tracking-wide transition-colors
                       underline underline-offset-4 decoration-stone-300 hover:decoration-stone-500"
          >
            重新开始推演
          </button>
        </motion.div>
      </div>
    </div>
  );
}
