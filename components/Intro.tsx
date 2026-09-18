"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { trySessionGet, trySessionSet } from "@/lib/utils";

interface IntroProps {
  appName: string;
  onComplete: () => void;
}

export default function Intro({ appName, onComplete }: IntroProps) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const seen = trySessionGet("usplus-intro-seen");
    if (seen) {
      onComplete();
      return;
    }
    setVisible(true);
    const timer = setTimeout(() => {
      trySessionSet("usplus-intro-seen", "true");
      setVisible(false);
      setTimeout(onComplete, 500);
    }, 2500);
    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="fixed inset-0 z-[100] bg-black flex items-center justify-center cursor-pointer"
          onClick={() => {
            trySessionSet("usplus-intro-seen", "true");
            setVisible(false);
            onComplete();
          }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <motion.div
            className="relative"
            initial={{ scale: 0.5, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
          >
            {/* Glow */}
            <motion.div
              className="absolute inset-0 blur-3xl rounded-full"
              style={{ background: "radial-gradient(circle, var(--accent) 0%, transparent 70%)" }}
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: [0, 0.4, 0.2], scale: [0.5, 1.2, 1] }}
              transition={{ duration: 2, ease: "easeOut" }}
            />

            {/* Wordmark */}
            <motion.h1
              className="relative text-8xl sm:text-9xl font-normal tracking-tight"
              style={{
                fontFamily: "var(--font-bebas)",
                color: "var(--accent)",
                textShadow: "0 0 40px rgba(229,56,74,0.5)",
              }}
              initial={{ y: 20 }}
              animate={{ y: 0 }}
              transition={{ delay: 0.3, duration: 0.6 }}
            >
              {appName}
            </motion.h1>

            {/* Light streak */}
            <motion.div
              className="absolute top-0 left-0 w-full h-full pointer-events-none"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
            >
              <motion.div
                className="absolute top-1/2 left-0 w-32 h-0.5 bg-gradient-to-r from-transparent via-white/60 to-transparent -translate-y-1/2"
                initial={{ x: "-100%" }}
                animate={{ x: "400%" }}
                transition={{ duration: 1.2, delay: 0.6, ease: "easeInOut" }}
              />
            </motion.div>
          </motion.div>

          <motion.p
            className="absolute bottom-12 text-text-dim text-sm"
            initial={{ opacity: 0 }}
            animate={{ opacity: [0, 1, 0] }}
            transition={{ duration: 2, delay: 1.5 }}
          >
            Skip
          </motion.p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
