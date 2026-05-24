"use client";

import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import type { RegretScenario } from "@/types";
import { cn } from "@/lib/utils";

interface MadLibsInputProps {
  onSubmit: (scenario: RegretScenario) => void;
  isLoading?: boolean;
  onFieldChange?: (filledCount: number) => void;
}

function InlineField({
  value,
  onChange,
  placeholder,
  width = "w-32 sm:w-40",
  type = "text",
}: {
  value: string;
  onChange: (v: string) => void;
  placeholder: string;
  width?: string;
  type?: string;
}) {
  return (
    <span className={cn("inline-block relative", width)}>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={cn(
          "w-full bg-transparent border-b-2 border-stone-300",
          "focus:border-emerald-600",
          "text-stone-800 font-medium placeholder:text-stone-400",
          "outline-none transition-all duration-300",
          "text-center py-0.5",
          type === "number" && "font-mono tracking-wider"
        )}
        {...(type === "number"
          ? { min: "1970", max: "2030", maxLength: 4 }
          : {})}
      />
    </span>
  );
}

export function MadLibsInput({
  onSubmit,
  isLoading,
  onFieldChange,
}: MadLibsInputProps) {
  const [year, setYear] = useState("");
  const [alternative, setAlternative] = useState("");
  const [current, setCurrent] = useState("");
  const [feeling, setFeeling] = useState("");
  const [showOptional, setShowOptional] = useState(false);
  const [age, setAge] = useState("");
  const [education, setEducation] = useState("");
  const [industry, setIndustry] = useState("");
  const [city, setCity] = useState("");

  const handleFieldChange = useCallback(
    (setter: (v: string) => void, v: string) => {
      setter(v);
      setTimeout(() => {
        const fields = [year, alternative, current, feeling];
        const newFilled = fields.filter((f) => f.trim().length > 0).length;
        onFieldChange?.(newFilled);
      }, 0);
    },
    [year, alternative, current, feeling, onFieldChange]
  );

  const isFormValid =
    year.trim().length === 4 &&
    /^\d{4}$/.test(year.trim()) &&
    alternative.trim().length > 0 &&
    current.trim().length > 0 &&
    feeling.trim().length > 0;

  const handleSubmit = () => {
    if (!isFormValid) return;
    const scenario: RegretScenario = {
      choice_point: current.trim(),
      time_node: `${year.trim()}-01`,
      alternative: alternative.trim(),
      current_state: feeling.trim(),
      ...(age.trim() && { user_age_at_time: parseInt(age.trim()) }),
      ...(education.trim() && { user_education: education.trim() }),
      ...(industry.trim() && { user_industry: industry.trim() }),
      ...(city.trim() && { user_city: city.trim() }),
    };
    onSubmit(scenario);
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-8">
      {/* Title */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="font-serif text-3xl sm:text-4xl md:text-5xl font-light text-stone-700 tracking-wide">
          后悔药
        </h1>
        <p className="mt-3 text-stone-400 text-sm sm:text-base leading-relaxed">
          写一封信，给那个做了另一个选择的自己
        </p>
      </motion.div>

      {/* The Mad Libs sentence */}
      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
        className="text-center"
      >
        <p className="text-stone-500 text-lg sm:text-xl md:text-2xl leading-[2.2] sm:leading-[2.5] tracking-wide font-serif">
          在{" "}
          <InlineField
            value={year}
            onChange={(v) => handleFieldChange(setYear, v)}
            placeholder="2018"
            width="w-20 sm:w-24"
            type="number"
          />{" "}
          年，我原本可以{" "}
          <InlineField
            value={alternative}
            onChange={(v) => handleFieldChange(setAlternative, v)}
            placeholder="去深圳加入腾讯"
            width="w-40 sm:w-52"
          />{" "}
          ，但我选择了{" "}
          <InlineField
            value={current}
            onChange={(v) => handleFieldChange(setCurrent, v)}
            placeholder="留在老家国企"
            width="w-40 sm:w-52"
          />{" "}
          。现在的我感觉{" "}
          <InlineField
            value={feeling}
            onChange={(v) => handleFieldChange(setFeeling, v)}
            placeholder="平淡但安稳"
            width="w-36 sm:w-44"
          />{" "}
          。
        </p>
      </motion.div>

      {/* Optional context toggle */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <button
          type="button"
          onClick={() => setShowOptional(!showOptional)}
          className="text-xs text-stone-400 hover:text-stone-600 transition-colors tracking-wide"
        >
          <span
            className={cn(
              "inline-block mr-1 transition-transform duration-200 text-[8px]",
              showOptional && "rotate-90"
            )}
          >
            ▶
          </span>
          补充信息（可选）
        </button>
      </motion.div>

      {/* Optional fields */}
      <AnimatePresence>
        {showOptional && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.25 }}
            className="overflow-hidden"
          >
            <div className="flex flex-wrap justify-center gap-4 text-sm">
              {[
                {
                  label: "当时年龄",
                  value: age,
                  setter: setAge,
                  placeholder: "25",
                  type: "number",
                },
                {
                  label: "学历",
                  value: education,
                  setter: setEducation,
                  placeholder: "本科 计算机",
                },
                {
                  label: "行业",
                  value: industry,
                  setter: setIndustry,
                  placeholder: "互联网",
                },
                {
                  label: "城市",
                  value: city,
                  setter: setCity,
                  placeholder: "成都",
                },
              ].map((opt) => (
                <div
                  key={opt.label}
                  className="flex items-center gap-2 text-stone-500"
                >
                  <span className="text-[11px] text-stone-400">
                    {opt.label}
                  </span>
                  <input
                    type={opt.type || "text"}
                    value={opt.value}
                    onChange={(e) => opt.setter(e.target.value)}
                    placeholder={opt.placeholder}
                    className="w-24 bg-transparent border-b border-stone-200 focus:border-stone-400 text-stone-700 placeholder:text-stone-300 outline-none text-xs py-0.5 transition-colors"
                  />
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Submit button */}
      <motion.div
        className="text-center"
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <button
          onClick={handleSubmit}
          disabled={!isFormValid || isLoading}
          className={cn(
            "px-8 py-3 rounded-xl text-sm tracking-widest",
            "bg-emerald-700 hover:bg-emerald-600 text-white font-medium",
            "disabled:opacity-30 disabled:cursor-not-allowed",
            "transition-all duration-300 shadow-sm"
          )}
        >
          {isLoading ? (
            <span className="flex items-center gap-2">
              <span className="animate-spin text-xs">◎</span>
              正在穿越时空...
            </span>
          ) : (
            "开始推演"
          )}
        </button>
      </motion.div>
    </div>
  );
}
