"use client";

import { useState, useEffect, useCallback } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence, useReducedMotion } from "framer-motion";
import { getFeaturedEntries } from "@/lib/content";

export default function Hero() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const prefersReducedMotion = useReducedMotion();
  const router = useRouter();
  const featured = getFeaturedEntries();
  const entry = featured[currentIndex] || featured[0];

  useEffect(() => {
    if (prefersReducedMotion || featured.length <= 1) return;
    const timer = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % featured.length);
    }, 10000);
    return () => clearInterval(timer);
  }, [featured.length, prefersReducedMotion]);

  const goToWatch = useCallback(() => {
    if (entry) router.push(`/watch/${entry.id}`);
  }, [entry, router]);

  if (!entry) return null;

  return (
    <div className="relative w-full h-[70vh] sm:h-[80vh] overflow-hidden">
      <AnimatePresence mode="wait">
        <motion.div
          key={entry.id}
          className="absolute inset-0"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.8 }}
        >
          {entry.backdrop && (
            <motion.div
              className="absolute inset-0"
              animate={prefersReducedMotion ? {} : { scale: [1, 1.08] }}
              transition={{ duration: 12, ease: "linear", repeat: Infinity, repeatType: "reverse" }}
            >
              <Image
                src={entry.backdrop}
                alt={entry.title}
                fill
                className="object-cover"
                sizes="100vw"
                priority
              />
            </motion.div>
          )}

          {/* Gradient overlays */}
          <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/40 to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-t from-bg via-transparent to-transparent" />

          {/* Content */}
          <div className="absolute bottom-20 sm:bottom-28 left-4 sm:left-8 lg:left-12 max-w-lg">
            <motion.h1
              className="text-5xl sm:text-7xl lg:text-8xl mb-2 leading-[0.9]"
              style={{ fontFamily: "var(--font-bebas)" }}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              {entry.title}
            </motion.h1>

            <motion.div
              className="flex flex-wrap items-center gap-x-3 gap-y-1 mb-3 text-sm"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <span className="text-green-400 font-semibold">100% Match</span>
              <span className="text-text-dim">S{entry.season} E{entry.episode}</span>
              {entry.runtime && <span className="text-text-dim">{entry.runtime}</span>}
              <span className="px-1.5 py-0.5 border border-text-dim/50 text-text-dim text-xs rounded">Rated: Forever</span>
            </motion.div>

            <motion.p
              className="text-text-dim text-sm sm:text-base mb-5 line-clamp-2 max-w-md"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.4 }}
            >
              {entry.synopsis}
            </motion.p>

            <motion.div
              className="flex gap-3"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
            >
              <motion.button
                onClick={goToWatch}
                className="flex items-center gap-2 px-6 py-2.5 bg-white text-black rounded font-semibold text-sm cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <polygon points="5,3 19,12 5,21" />
                </svg>
                Play
              </motion.button>
              <motion.button
                className="flex items-center gap-2 px-6 py-2.5 bg-white/20 text-white rounded text-sm cursor-pointer"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
                More Info
              </motion.button>
            </motion.div>
          </div>
        </motion.div>
      </AnimatePresence>

      {/* Nav dots */}
      {featured.length > 1 && (
        <div className="absolute bottom-8 right-4 sm:right-8 lg:right-12 flex gap-1.5">
          {featured.map((_, i) => (
            <button
              key={i}
              onClick={() => setCurrentIndex(i)}
              className={`w-8 h-1 rounded transition-all cursor-pointer ${
                i === currentIndex ? "bg-white" : "bg-white/30"
              }`}
              aria-label={`Go to featured ${i + 1}`}
            />
          ))}
        </div>
      )}
    </div>
  );
}
