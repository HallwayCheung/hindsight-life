"use client";

import { motion } from "framer-motion";
import type { V4TimelineNode } from "@/types";

interface TimelineCardsProps {
  nodes: V4TimelineNode[];
}

const staggerContainer = {
  hidden: {},
  show: { transition: { staggerChildren: 0.2 } },
};

const staggerItem = {
  hidden: { opacity: 0, y: 16 },
  show: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.5, ease: "easeOut" as const },
  },
};

export function TimelineCards({ nodes }: TimelineCardsProps) {
  return (
    <motion.div
      className="space-y-6"
      variants={staggerContainer}
      initial="hidden"
      animate="show"
    >
      {nodes.map((node) => (
        <motion.div key={node.year} variants={staggerItem}>
          {/* Year marker */}
          <div className="flex items-center gap-3 mb-3">
            <div className="h-px flex-1 bg-stone-200" />
            <span className="text-xs text-stone-400 tracking-widest shrink-0 font-mono">
              {node.year}
            </span>
            <div className="h-px flex-1 bg-stone-200" />
          </div>

          {/* Journal entry card */}
          <div className="paper-card overflow-hidden">
            <div className="grid grid-cols-1 md:grid-cols-2">
              {/* Reality */}
              <div className="p-5 md:p-6 md:border-r border-stone-100">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  <span className="text-[10px] text-emerald-700 tracking-wider uppercase">
                    现实
                  </span>
                </div>
                <p className="text-stone-600 text-sm leading-loose">
                  {node.reality_snapshot}
                </p>
              </div>

              {/* Parallel */}
              <div className="p-5 md:p-6 bg-stone-50/50">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-orange-400" />
                  <span className="text-[10px] text-orange-700 tracking-wider uppercase">
                    平行宇宙
                  </span>
                </div>
                <p className="text-stone-600 text-sm leading-loose">
                  {node.parallel_snapshot}
                </p>
              </div>
            </div>

            {/* Divergence point */}
            {node.divergence_point && (
              <div className="px-5 py-3 md:px-6 border-t border-stone-100 bg-stone-50/30">
                <p className="text-stone-400 text-xs text-center tracking-wider">
                  {node.divergence_point}
                </p>
              </div>
            )}
          </div>
        </motion.div>
      ))}
    </motion.div>
  );
}
