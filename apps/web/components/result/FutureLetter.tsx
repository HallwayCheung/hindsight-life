"use client";

import { motion } from "framer-motion";
import type { FutureLetter as FutureLetterType } from "@/types";

interface FutureLetterProps {
  letter: FutureLetterType;
}

export function FutureLetter({ letter }: FutureLetterProps) {
  const paragraphs = letter.content
    .split(/(?<=[。！？])/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);

  // Group sentences into paragraphs (every 2-3 sentences)
  const groupedParagraphs: string[] = [];
  for (let i = 0; i < paragraphs.length; i += 2) {
    groupedParagraphs.push(paragraphs.slice(i, i + 2).join(""));
  }

  return (
    <motion.div
      className="letter-paper p-6 sm:p-8 md:p-10 max-w-2xl mx-auto"
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
    >
      {/* Greeting */}
      <motion.p
        className="font-serif text-xl sm:text-2xl text-stone-700 mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        {letter.greetings}
      </motion.p>

      {/* Content paragraphs */}
      <div className="space-y-4">
        {groupedParagraphs.map((para, i) => (
          <motion.p
            key={i}
            className="font-serif text-base sm:text-lg text-stone-600 leading-loose tracking-wide"
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 + i * 0.3, duration: 0.5 }}
          >
            {para}
          </motion.p>
        ))}
      </div>

      {/* Signature */}
      <motion.p
        className="font-serif text-base sm:text-lg text-stone-500 mt-8 text-right"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 + groupedParagraphs.length * 0.3 + 0.3 }}
      >
        {letter.signature}
      </motion.p>
    </motion.div>
  );
}
