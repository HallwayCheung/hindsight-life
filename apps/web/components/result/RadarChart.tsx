"use client";

import { motion } from "framer-motion";
import type { EmotionalMetrics } from "@/types";

interface EmotionalBatteryProps {
  metrics: EmotionalMetrics;
}

const staggerContainer = {
  hidden: {},
  show: { transition: { staggerChildren: 0.15 } },
};

const staggerItem = {
  hidden: { opacity: 0, y: 12 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" as const },
  },
};

export function EmotionalBattery({ metrics }: EmotionalBatteryProps) {
  const entries = Object.entries(metrics);

  return (
    <motion.div
      className="space-y-6"
      variants={staggerContainer}
      initial="hidden"
      animate="show"
    >
      {entries.map(([key, metric]) => (
        <motion.div key={key} variants={staggerItem} className="space-y-2">
          {/* Label */}
          <div className="flex items-baseline justify-between">
            <span className="text-sm text-stone-600 font-medium">
              {metric.label}
            </span>
            <div className="flex items-baseline gap-3 text-xs">
              <span className="text-emerald-700">{metric.reality}%</span>
              <span className="text-stone-300">vs</span>
              <span className="text-orange-700">{metric.parallel}%</span>
            </div>
          </div>

          {/* Bars */}
          <div className="space-y-1.5">
            {/* Reality bar */}
            <div className="flex items-center gap-3">
              <span className="text-[10px] text-stone-400 w-6 shrink-0">
                现实
              </span>
              <div className="flex-1 h-2.5 bg-stone-100 rounded-full overflow-hidden">
                <motion.div
                  className="h-full rounded-full bg-gradient-to-r from-emerald-200 to-emerald-400"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: metric.reality / 100 }}
                  transition={{ delay: 0.3, duration: 0.8, ease: "easeOut" }}
                  style={{ transformOrigin: "left" }}
                />
              </div>
            </div>

            {/* Parallel bar */}
            <div className="flex items-center gap-3">
              <span className="text-[10px] text-stone-400 w-6 shrink-0">
                平行
              </span>
              <div className="flex-1 h-2.5 bg-stone-100 rounded-full overflow-hidden">
                <motion.div
                  className="h-full rounded-full bg-gradient-to-r from-orange-200 to-orange-400"
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: metric.parallel / 100 }}
                  transition={{ delay: 0.45, duration: 0.8, ease: "easeOut" }}
                  style={{ transformOrigin: "left" }}
                />
              </div>
            </div>
          </div>
        </motion.div>
      ))}
    </motion.div>
  );
}
