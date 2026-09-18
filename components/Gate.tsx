"use client";

import { useState, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface GateProps {
  passcode: string;
  onUnlock: () => void;
}

export default function Gate({ passcode, onUnlock }: GateProps) {
  const [input, setInput] = useState("");
  const [error, setError] = useState(false);
  const [unlocked, setUnlocked] = useState(false);

  useEffect(() => {
    try {
      const stored = sessionStorage.getItem("usplus-unlocked");
      if (stored === "true") {
        setUnlocked(true);
        onUnlock();
      }
    } catch {}
  }, [onUnlock]);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      if (input === passcode) {
        setUnlocked(true);
        try { sessionStorage.setItem("usplus-unlocked", "true"); } catch {}
        onUnlock();
      } else {
        setError(true);
        setInput("");
        setTimeout(() => setError(false), 800);
      }
    },
    [input, passcode, onUnlock]
  );

  if (!passcode) { onUnlock(); return null; }
  if (unlocked) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-[90] flex items-center justify-center bg-black"
        exit={{ opacity: 0 }}
        transition={{ duration: 0.4 }}
      >
        <motion.div
          className="w-[85vw] max-w-sm rounded-lg p-8 bg-bg-elev border border-white/10"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.1, duration: 0.4 }}
        >
          <h2 className="text-center text-2xl mb-1 text-text" style={{ fontFamily: "var(--font-bebas)" }}>
            Enter Access Code
          </h2>
          <p className="text-center text-text-dim text-sm mb-6">
            This diary is private.
          </p>
          <motion.form
            onSubmit={handleSubmit}
            animate={error ? { x: [0, -10, 10, -6, 6, -3, 3, 0] } : {}}
            transition={{ duration: 0.4 }}
          >
            <input
              type="password"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="w-full px-4 py-3 rounded bg-card border border-white/10 text-text text-center text-lg focus:outline-none focus:border-accent mb-4"
              autoFocus
              placeholder="••••••"
              aria-label="Passcode"
            />
            <motion.button
              type="submit"
              className="w-full py-3 rounded bg-accent text-white font-semibold cursor-pointer"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Continue
            </motion.button>
          </motion.form>
          {error && (
            <motion.p className="text-accent text-sm text-center mt-3" initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
              Incorrect code. Try again.
            </motion.p>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
