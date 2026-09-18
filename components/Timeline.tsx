"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface TimelineProps {
  entries: { id: string; date: string; title: string }[];
  activeIndex: number;
  className?: string;
}

function getYearMonth(dateStr: string) {
  const d = new Date(dateStr + "T00:00:00");
  return {
    year: d.getFullYear(),
    month: d.toLocaleDateString("en-US", { month: "short" }),
  };
}

export default function Timeline({
  entries,
  activeIndex,
  className,
}: TimelineProps) {
  const grouped = entries.reduce<
    Record<number, { month: string; index: number }[]>
  >((acc, entry, i) => {
    const { year, month } = getYearMonth(entry.date);
    if (!acc[year]) acc[year] = [];
    acc[year].push({ month, index: i });
    return acc;
  }, {});

  return (
    <nav
      className={cn("flex flex-col gap-4", className)}
      aria-label="Diary timeline"
    >
      {Object.entries(grouped).map(([year, items]) => (
        <div key={year} className="flex flex-col gap-1">
          <span
            className="text-xs font-medium text-gold tracking-wider uppercase mb-1"
            style={{ fontFamily: "var(--font-inter)" }}
          >
            {year}
          </span>
          {items.map(({ month, index }) => {
            const isActive = index === activeIndex;
            return (
              <a
                key={index}
                href={`#entry-${entries[index].id}`}
                className={cn(
                  "flex items-center gap-2 py-1 px-2 rounded text-sm transition-all duration-300 no-underline",
                  isActive
                    ? "text-accent bg-accent/5"
                    : "text-muted hover:text-ink"
                )}
                style={{ fontFamily: "var(--font-inter)" }}
              >
                <motion.div
                  className={cn(
                    "w-1.5 h-1.5 rounded-full flex-shrink-0",
                    isActive ? "bg-accent" : "bg-muted/40"
                  )}
                  animate={isActive ? { scale: [1, 1.4, 1] } : {}}
                  transition={{ duration: 0.4 }}
                />
                <span>{month}</span>
              </a>
            );
          })}
        </div>
      ))}
    </nav>
  );
}
