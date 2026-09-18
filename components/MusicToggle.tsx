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
      const saved = localStorage.getItem("diary-music");
      if (saved === "true") {
        setIsPlaying(true);
      }
    } catch {}

    // Check if audio file exists
    const sound = new Howl({
      src: ["/audio/song.mp3"],
      html5: true,
      loop: true,
      volume: 0.5,
      onload: () => setIsLoaded(true),
      onloaderror: () => setIsLoaded(false),
    });

    soundRef.current = sound;

    return () => {
      sound.unload();
    };
  }, []);

  useEffect(() => {
    if (!soundRef.current || !isLoaded) return;
    if (isPlaying) {
      soundRef.current.play();
    } else {
      soundRef.current.pause();
    }
    try {
      localStorage.setItem("diary-music", String(isPlaying));
    } catch {}
  }, [isPlaying, isLoaded]);

  const toggle = useCallback(() => {
    setIsPlaying((prev) => !prev);
  }, []);

  if (!isLoaded) return null;

  return (
    <motion.button
      onClick={toggle}
      className="fixed bottom-6 right-6 z-40 w-12 h-12 rounded-full bg-paper-dark/90 backdrop-blur-sm border border-gold/30 shadow-lg flex items-center justify-center cursor-pointer"
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.95 }}
      aria-label={isPlaying ? "Pause music" : "Play music"}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 1, duration: 0.5 }}
    >
      <AnimatePresence mode="wait">
        {isPlaying ? (
          <motion.svg
            key="pause"
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="currentColor"
            className="text-accent"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            <rect x="3" y="2" width="4" height="12" rx="1" />
            <rect x="9" y="2" width="4" height="12" rx="1" />
          </motion.svg>
        ) : (
          <motion.svg
            key="play"
            width="16"
            height="16"
            viewBox="0 0 16 16"
            fill="currentColor"
            className="text-muted"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
          >
            <polygon points="3,2 14,8 3,14" />
          </motion.svg>
        )}
      </AnimatePresence>
    </motion.button>
  );
}
