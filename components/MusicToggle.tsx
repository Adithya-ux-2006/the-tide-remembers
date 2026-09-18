"use client";

import { useState, useEffect, useRef, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Howl } from "howler";

export default function MusicToggle() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const soundRef = useRef<Howl | null>(null);

  useEffect(() => {
    try {
      const saved = localStorage.getItem("usplus-music");
      if (saved === "true") setIsPlaying(true);
    } catch {}

    const sound = new Howl({
      src: ["/audio/song.mp3"],
      html5: true,
      loop: true,
      volume: 0.4,
      onload: () => setIsLoaded(true),
      onloaderror: () => setIsLoaded(false),
    });
    soundRef.current = sound;
    return () => { sound.unload(); };
  }, []);

  useEffect(() => {
    if (!soundRef.current || !isLoaded) return;
    if (isPlaying) soundRef.current.play();
    else soundRef.current.pause();
    try { localStorage.setItem("usplus-music", String(isPlaying)); } catch {}
  }, [isPlaying, isLoaded]);

  const toggle = useCallback(() => setIsPlaying((p) => !p), []);

  if (!isLoaded) return null;

  return (
    <motion.button
      onClick={toggle}
      className="fixed bottom-20 md:bottom-6 right-6 z-40 w-10 h-10 rounded-full bg-card/90 backdrop-blur-sm border border-white/10 shadow-lg flex items-center justify-center cursor-pointer"
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      aria-label={isPlaying ? "Pause music" : "Play music"}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 1 }}
    >
      <AnimatePresence mode="wait">
        {isPlaying ? (
          <motion.svg key="pause" width="14" height="14" viewBox="0 0 16 16" fill="var(--accent)" initial={{ scale: 0.8 }} animate={{ scale: 1 }} exit={{ scale: 0.8 }}>
            <rect x="3" y="2" width="4" height="12" rx="1" />
            <rect x="9" y="2" width="4" height="12" rx="1" />
          </motion.svg>
        ) : (
          <motion.svg key="play" width="14" height="14" viewBox="0 0 16 16" fill="var(--text-dim)" initial={{ scale: 0.8 }} animate={{ scale: 1 }} exit={{ scale: 0.8 }}>
            <polygon points="3,2 14,8 3,14" />
          </motion.svg>
        )}
      </AnimatePresence>
    </motion.button>
  );
}
