"use client";

import { motion } from "framer-motion";

interface SoulSummaryProps {
  text: string;
}

export function SoulSummary({ text }: SoulSummaryProps) {
  if (!text) return null;

  const sentences = text
    .split(/(?<=[。！？])/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);

  return (
    <motion.div
      className="text-center max-w-2xl mx-auto px-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <p className="font-serif text-xl sm:text-2xl md:text-3xl font-light leading-loose tracking-wide text-stone-600">
        {sentences.map((sentence, i) => (
          <motion.span
            key={i}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.3 + i * 0.4,
              duration: 0.6,
              ease: "easeOut",
            }}
          >
            {sentence}
          </motion.span>
        ))}
      </p>
    </motion.div>
  );
}
