"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { daysBetween } from "@/lib/utils";

interface DaysCounterProps {
  startDate: string;
}

export default function DaysCounter({ startDate }: DaysCounterProps) {
  const [days, setDays] = useState<number | null>(null);

  useEffect(() => {
    setDays(daysBetween(startDate));
    const interval = setInterval(() => {
      setDays(daysBetween(startDate));
    }, 60000);
    return () => clearInterval(interval);
  }, [startDate]);

  if (days === null) return <span className="text-muted">...</span>;

  return (
    <motion.div
      className="flex flex-col items-center gap-1"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.8, duration: 0.6 }}
    >
      <span
        className="text-5xl font-light text-accent"
        style={{ fontFamily: "var(--font-caveat)" }}
      >
        {days.toLocaleString()}
      </span>
      <span className="text-sm text-muted tracking-widest uppercase">
        days together
      </span>
    </motion.div>
  );
}
