"use client";

import { useRef, useState, useEffect } from "react";
import { motion, useInView } from "framer-motion";
import EntryPage from "./EntryPage";
import Timeline from "./Timeline";
import type { Entry } from "@/lib/types";

interface DiaryScrollerProps {
  entries: Entry[];
}

export default function DiaryScroller({ entries }: DiaryScrollerProps) {
  const [activeIndex, setActiveIndex] = useState(0);
  const observerRefs = useRef<(Element | null)[]>([]);

  useEffect(() => {
    const observers: IntersectionObserver[] = [];

    observerRefs.current.forEach((el, i) => {
      if (!el) return;
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setActiveIndex(i);
          }
        },
        { threshold: 0.5 }
      );
      observer.observe(el);
      observers.push(observer);
    });

    return () => {
      observers.forEach((o) => o.disconnect());
    };
  }, [entries]);

  return (
    <div className="relative">
      {/* Desktop timeline sidebar */}
      <div className="hidden lg:block fixed left-6 top-1/2 -translate-y-1/2 z-30 w-32">
        <Timeline entries={entries} activeIndex={activeIndex} />
      </div>

      {/* Mobile progress bar */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-30 h-1 bg-paper-dark">
        <motion.div
          className="h-full bg-accent"
          style={{
            width: `${((activeIndex + 1) / entries.length) * 100}%`,
          }}
          transition={{ duration: 0.3 }}
        />
      </div>

      {/* Entries */}
      <div className="lg:ml-40">
        {entries.map((entry, i) => (
          <div key={entry.id} ref={(el) => { observerRefs.current[i] = el; }}>
            <EntryPage entry={entry} index={i} priority={i < 2} />
          </div>
        ))}
      </div>
    </div>
  );
}
