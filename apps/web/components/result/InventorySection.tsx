"use client";

import { motion } from "framer-motion";
import type { ParallelSouvenir } from "@/types";

interface SouvenirCardProps {
  souvenir: ParallelSouvenir;
}

const ICON_MAP: Record<string, string> = {
  ticket: "🎫",
  letter: "✉️",
  photo: "📷",
  key: "🗝️",
  ring: "💍",
};

export function SouvenirCard({ souvenir }: SouvenirCardProps) {
  const icon = ICON_MAP[souvenir.icon_type] || "📦";

  return (
    <motion.div
      className="paper-card p-6 sm:p-8 max-w-lg mx-auto text-center"
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
    >
      {/* Icon */}
      <motion.div
        className="text-4xl mb-4"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.4 }}
      >
        {icon}
      </motion.div>

      {/* Label */}
      <p className="text-[10px] text-stone-400 tracking-wider uppercase mb-2">
        来自平行宇宙的纪念品
      </p>

      {/* Item name */}
      <h3 className="font-serif text-lg sm:text-xl text-stone-700 mb-3">
        {souvenir.item_name}
      </h3>

      {/* Description */}
      <p className="text-stone-500 text-sm leading-loose">
        {souvenir.description}
      </p>
    </motion.div>
  );
}
