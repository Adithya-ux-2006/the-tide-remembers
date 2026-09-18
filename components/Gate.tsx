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
      const stored = sessionStorage.getItem("diary-unlocked");
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
        try {
          sessionStorage.setItem("diary-unlocked", "true");
        } catch {}
        onUnlock();
      } else {
        setError(true);
        setInput("");
        setTimeout(() => setError(false), 800);
      }
    },
    [input, passcode, onUnlock]
  );

  if (!passcode) {
    onUnlock();
    return null;
  }

  if (unlocked) return null;

  return (
    <AnimatePresence>
      <motion.div
        className="fixed inset-0 z-50 flex items-center justify-center bg-paper"
        initial={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.6 }}
      >
        <motion.div
          className="w-[90vw] max-w-sm rounded-2xl bg-paper-dark p-8 shadow-xl border border-gold/30"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.5 }}
        >
          <h2
            className="text-center text-2xl mb-2 text-ink"
            style={{ fontFamily: "var(--font-caveat)" }}
          >
            Say our secret word
          </h2>
          <p className="text-center text-muted text-sm mb-6">
            Enter the passcode to continue
          </p>

          <motion.form
            onSubmit={handleSubmit}
            animate={error ? { x: [0, -12, 12, -8, 8, -4, 4, 0] } : {}}
            transition={{ duration: 0.5 }}
          >
            <input
              type="password"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gold/40 bg-paper text-ink text-center text-lg focus:outline-none focus:ring-2 focus:ring-accent/50 mb-4"
              autoFocus
              placeholder="..."
              aria-label="Passcode"
            />
            <motion.button
              type="submit"
              className="w-full py-3 rounded-lg bg-accent text-paper font-medium cursor-pointer"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              Open
            </motion.button>
          </motion.form>

          {error && (
            <motion.p
              className="text-accent text-sm text-center mt-3"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              That&apos;s not it, try again...
            </motion.p>
          )}
        </motion.div>
      </motion.div>
    </AnimatePresence>
  );
}
