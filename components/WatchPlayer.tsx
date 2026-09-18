"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import type { Entry } from "@/lib/types";
import { getEntries } from "@/lib/content";
import { setProgress } from "@/lib/progress";
import { useReducedMotion } from "framer-motion";

interface WatchPlayerProps {
  entry: Entry;
}

export default function WatchPlayer({ entry }: WatchPlayerProps) {
  const router = useRouter();
  const [currentBeat, setCurrentBeat] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [showControls, setShowControls] = useState(true);
  const [showSkip, setShowSkip] = useState(true);
  const prefersReducedMotion = useReducedMotion();
  const controlsTimerRef = useRef<ReturnType<typeof setTimeout>>(undefined);
  const beatTimerRef = useRef<ReturnType<typeof setTimeout>>(undefined);
  const images = entry.images.length > 0 ? entry.images : [entry.thumb];
  const paragraphs = entry.story.split("\n\n").filter(Boolean);
  const beats = paragraphs.map((text, i) => ({
    text,
    image: images[i % images.length],
  }));
  const totalBeats = beats.length;

  // Auto-advance beats
  useEffect(() => {
    if (isPaused || currentBeat >= totalBeats) return;
    beatTimerRef.current = setTimeout(() => {
      if (currentBeat < totalBeats - 1) {
        setCurrentBeat((prev) => prev + 1);
      }
    }, 6000);
    return () => clearTimeout(beatTimerRef.current);
  }, [currentBeat, isPaused, totalBeats]);

  // Save progress
  useEffect(() => {
    setProgress(entry.id, currentBeat);
  }, [entry.id, currentBeat]);

  // Auto-hide controls
  const resetControlsTimer = useCallback(() => {
    setShowControls(true);
    if (controlsTimerRef.current) clearTimeout(controlsTimerRef.current);
    controlsTimerRef.current = setTimeout(() => setShowControls(false), 3000);
  }, []);

  useEffect(() => {
    resetControlsTimer();
    return () => { if (controlsTimerRef.current) clearTimeout(controlsTimerRef.current); };
  }, [resetControlsTimer]);

  // Keyboard
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      resetControlsTimer();
      switch (e.key) {
        case " ":
          e.preventDefault();
          setIsPaused((p) => !p);
          break;
        case "ArrowRight":
          setCurrentBeat((prev) => Math.min(prev + 1, totalBeats - 1));
          break;
        case "ArrowLeft":
          setCurrentBeat((prev) => Math.max(prev - 1, 0));
          break;
        case "Escape":
          router.push("/browse");
          break;
        case "f":
          if (document.fullscreenElement) document.exitFullscreen();
          else document.documentElement.requestFullscreen();
          break;
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [totalBeats, router, resetControlsTimer]);

  const nextEpisode = useCallback(() => {
    const entries = getEntries();
    const idx = entries.findIndex((e) => e.id === entry.id);
    if (idx < entries.length - 1) {
      router.push(`/watch/${entries[idx + 1].id}`);
    } else {
      router.push("/credits");
    }
  }, [entry.id, router]);

  const beat = beats[currentBeat];

  return (
    <div
      className="fixed inset-0 bg-black z-50"
      onMouseMove={resetControlsTimer}
      onClick={resetControlsTimer}
    >
      {/* Crossfade images */}
      <AnimatePresence mode="wait">
        <motion.div
          key={`${entry.id}-${currentBeat}`}
          className="absolute inset-0"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 1 }}
        >
          <motion.div
            className="absolute inset-0"
            animate={prefersReducedMotion ? {} : {
              scale: [1, 1.06],
              x: currentBeat % 2 === 0 ? [0, -10] : [0, 10],
              y: [0, -5],
            }}
            transition={{ duration: 6, ease: "linear" }}
          >
            <Image
              src={beat?.image || entry.thumb}
              alt={entry.title}
              fill
              className="object-cover"
              sizes="100vw"
            />
          </motion.div>
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/30" />
        </motion.div>
      </AnimatePresence>

      {/* Subtitle text */}
      <AnimatePresence mode="wait">
        <motion.div
          key={`text-${currentBeat}`}
          className="absolute bottom-24 sm:bottom-32 left-0 right-0 px-6 sm:px-16 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.6 }}
        >
          <p className="text-lg sm:text-2xl text-white/90 leading-relaxed max-w-3xl mx-auto drop-shadow-lg" style={{ fontFamily: "var(--font-inter)" }}>
            {beat?.text}
          </p>
        </motion.div>
      </AnimatePresence>

      {/* Skip intro card */}
      <AnimatePresence>
        {showSkip && currentBeat === 0 && (
          <motion.div
            className="absolute bottom-36 right-6 sm:right-16"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: 20 }}
          >
            <motion.button
              onClick={() => setShowSkip(false)}
              className="px-5 py-2.5 bg-white/10 border border-white/30 rounded text-sm text-white cursor-pointer hover:bg-white/20 transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Skip to the good part
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Controls overlay */}
      <AnimatePresence>
        {showControls && (
          <motion.div
            className="absolute inset-0 pointer-events-none"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {/* Top bar */}
            <div className="absolute top-0 left-0 right-0 p-4 sm:p-6 flex items-center gap-4 bg-gradient-to-b from-black/60 to-transparent pointer-events-auto">
              <motion.button
                onClick={() => router.push("/browse")}
                className="text-white cursor-pointer"
                whileHover={{ scale: 1.1 }}
                aria-label="Back"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <polyline points="15,18 9,12 15,6" />
                </svg>
              </motion.button>
              <div>
                <p className="text-sm text-white font-semibold">{entry.title}</p>
                <p className="text-xs text-white/60">S{entry.season} E{entry.episode}</p>
              </div>
            </div>

            {/* Bottom controls */}
            <div className="absolute bottom-0 left-0 right-0 p-4 sm:p-6 bg-gradient-to-t from-black/80 to-transparent pointer-events-auto">
              {/* Scrub bar */}
              <div className="flex items-center gap-2 mb-4">
                {beats.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrentBeat(i)}
                    className={`h-1 flex-1 rounded transition-all cursor-pointer ${
                      i === currentBeat ? "bg-accent" : i < currentBeat ? "bg-white/40" : "bg-white/20"
                    }`}
                    aria-label={`Go to beat ${i + 1}`}
                  />
                ))}
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <motion.button
                    onClick={() => setCurrentBeat(Math.max(currentBeat - 1, 0))}
                    className="text-white cursor-pointer"
                    whileHover={{ scale: 1.1 }}
                    aria-label="Previous beat"
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polygon points="19,20 9,12 19,4" fill="currentColor" />
                      <line x1="5" y1="4" x2="5" y2="20" />
                    </svg>
                  </motion.button>

                  <motion.button
                    onClick={() => setIsPaused(!isPaused)}
                    className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center text-white cursor-pointer"
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    aria-label={isPaused ? "Play" : "Pause"}
                  >
                    {isPaused ? (
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                        <polygon points="5,3 19,12 5,21" />
                      </svg>
                    ) : (
                      <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                        <rect x="6" y="4" width="4" height="16" rx="1" />
                        <rect x="14" y="4" width="4" height="16" rx="1" />
                      </svg>
                    )}
                  </motion.button>

                  <motion.button
                    onClick={() => setCurrentBeat(Math.min(currentBeat + 1, totalBeats - 1))}
                    className="text-white cursor-pointer"
                    whileHover={{ scale: 1.1 }}
                    aria-label="Next beat"
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <polygon points="5,4 15,12 5,20" fill="currentColor" />
                      <line x1="19" y1="4" x2="19" y2="20" />
                    </svg>
                  </motion.button>
                </div>

                <div className="flex items-center gap-3">
                  <span className="text-xs text-white/60">{currentBeat + 1} / {totalBeats}</span>
                  <motion.button
                    onClick={nextEpisode}
                    className="px-4 py-1.5 bg-white/10 border border-white/30 rounded text-xs text-white cursor-pointer hover:bg-white/20 transition-colors"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    {currentBeat >= totalBeats - 1 ? "Next Episode" : "Skip"}
                  </motion.button>
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* End of episode - next episode countdown */}
      <AnimatePresence>
        {currentBeat >= totalBeats - 1 && !isPaused && (
          <motion.div
            className="absolute bottom-40 right-6 sm:right-16"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 3 }}
          >
            <motion.button
              onClick={nextEpisode}
              className="px-6 py-3 bg-white text-black rounded font-semibold cursor-pointer"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Next Episode →
            </motion.button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
