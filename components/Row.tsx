"use client";

import { useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import useEmblaCarousel from "embla-carousel-react";
import { motion } from "framer-motion";
import Card from "./Card";
import type { Entry } from "@/lib/types";
import { getEntryProgress } from "@/lib/progress";

interface RowProps {
  title: string;
  entries: Entry[];
  isTop10?: boolean;
  isContinue?: boolean;
  id?: string;
}

export default function Row({ title, entries, isTop10 = false, isContinue = false, id }: RowProps) {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    align: "start",
    containScroll: "trimSnaps",
    slidesToScroll: 3,
  });
  const [canScrollPrev, setCanScrollPrev] = useState(false);
  const [canScrollNext, setCanScrollNext] = useState(false);
  const [showArrows, setShowArrows] = useState(false);

  const scrollPrev = useCallback(() => emblaApi?.scrollPrev(), [emblaApi]);
  const scrollNext = useCallback(() => emblaApi?.scrollNext(), [emblaApi]);

  const onSelect = useCallback(() => {
    if (!emblaApi) return;
    setCanScrollPrev(emblaApi.canScrollPrev());
    setCanScrollNext(emblaApi.canScrollNext());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    onSelect();
    emblaApi.on("select", onSelect);
    emblaApi.on("reInit", onSelect);
    return () => {
      emblaApi.off("select", onSelect);
      emblaApi.off("reInit", onSelect);
    };
  }, [emblaApi, onSelect]);

  if (isContinue && entries.length === 0) return null;

  return (
    <motion.section
      id={id}
      className="relative mb-8 sm:mb-10"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.1 }}
      transition={{ duration: 0.5 }}
      onMouseEnter={() => setShowArrows(true)}
      onMouseLeave={() => setShowArrows(false)}
    >
      <h2
        className="text-xl sm:text-2xl px-4 sm:px-8 lg:px-12 mb-3 text-text"
        style={{ fontFamily: "var(--font-bebas)" }}
      >
        {title}
      </h2>

      <div className="relative group">
        {canScrollPrev && (
          <motion.button
            className={`absolute left-0 top-0 bottom-0 w-12 z-10 bg-black/60 hover:bg-black/80 flex items-center justify-center cursor-pointer transition-opacity ${
              showArrows ? "opacity-100" : "opacity-0"
            }`}
            onClick={scrollPrev}
            aria-label="Scroll left"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <polyline points="15,18 9,12 15,6" />
            </svg>
          </motion.button>
        )}

        <div ref={emblaRef} className="embla overflow-hidden">
          <div className="embla__container pl-4 sm:pl-8 lg:pl-12 pr-4">
            {entries.map((entry, i) => (
              <div
                key={entry.id}
                className="embla__slide"
                style={{ "--card-w": isTop10 ? "140px" : "200px" } as React.CSSProperties}
              >
                {isTop10 ? (
                  <Top10Card entry={entry} rank={i + 1} />
                ) : isContinue ? (
                  <ContinueCard entry={entry} />
                ) : (
                  <Card entry={entry} index={i} />
                )}
              </div>
            ))}
          </div>
        </div>

        {canScrollNext && (
          <motion.button
            className={`absolute right-0 top-0 bottom-0 w-12 z-10 bg-black/60 hover:bg-black/80 flex items-center justify-center cursor-pointer transition-opacity ${
              showArrows ? "opacity-100" : "opacity-0"
            }`}
            onClick={scrollNext}
            aria-label="Scroll right"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
              <polyline points="9,18 15,12 9,6" />
            </svg>
          </motion.button>
        )}
      </div>
    </motion.section>
  );
}

function Top10Card({ entry, rank }: { entry: Entry; rank: number }) {
  const router = useRouter();

  return (
    <motion.button
      onClick={() => router.push(`/watch/${entry.id}`)}
      className="relative flex-shrink-0 cursor-pointer group"
      style={{ width: 140 }}
      whileHover={{ scale: 1.35, zIndex: 20, y: -20 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
      aria-label={`#${rank} ${entry.title}`}
    >
      <div className="relative w-[140px] h-[210px] rounded overflow-hidden bg-card">
        <div className="absolute left-0 bottom-0 z-10 text-[100px] font-bold text-white/10 leading-none" style={{ fontFamily: "var(--font-bebas)" }}>
          {rank}
        </div>
        <div className="absolute left-2 bottom-2 z-10 text-5xl font-bold text-white" style={{ fontFamily: "var(--font-bebas)" }}>
          {rank}
        </div>
        <img
          src={entry.thumb}
          alt={entry.title}
          className="w-full h-full object-cover"
          loading="lazy"
        />
      </div>
      <p className="text-xs text-text mt-2 truncate">{entry.title}</p>
    </motion.button>
  );
}

function ContinueCard({ entry }: { entry: Entry }) {
  const router = useRouter();
  const progress = getEntryProgress(entry.id);
  const pct = progress ? Math.min(((progress.beatIndex + 1) / 3) * 100, 95) : 0;

  return (
    <motion.button
      onClick={() => router.push(`/watch/${entry.id}`)}
      className="relative flex-shrink-0 cursor-pointer group"
      style={{ width: 200 }}
      whileHover={{ scale: 1.35, zIndex: 20, y: -20 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
      aria-label={`Continue ${entry.title}`}
    >
      <div className="relative rounded-t overflow-hidden bg-card aspect-video">
        <img
          src={entry.thumb}
          alt={entry.title}
          className="w-full h-full object-cover"
          loading="lazy"
        />
        <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/20">
          <div className="h-full bg-accent" style={{ width: `${pct}%` }} />
        </div>
      </div>
      <div className="bg-card rounded-b p-2">
        <p className="text-sm text-text truncate">{entry.title}</p>
        <p className="text-xs text-text-dim">Resume S{entry.season} E{entry.episode}</p>
      </div>
    </motion.button>
  );
}
