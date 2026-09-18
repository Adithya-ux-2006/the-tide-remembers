"use client";

import { motion } from "framer-motion";
import DaysCounter from "./DaysCounter";
import { getConfig } from "@/lib/content";

interface CoverProps {
  onOpen: () => void;
}

const ease = [0.22, 1, 0.36, 1] as const;

export default function Cover({ onOpen }: CoverProps) {
  const config = getConfig();

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-paper">
      {/* Decorative elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-[15%] left-[10%] w-32 h-32 rounded-full bg-accent/5" />
        <div className="absolute bottom-[20%] right-[15%] w-48 h-48 rounded-full bg-gold/5" />
        <div className="absolute top-[40%] right-[8%] w-24 h-24 rounded-full bg-accent-2/10" />
      </div>

      {/* Book card */}
      <motion.div
        className="relative z-10 w-[90vw] max-w-md mx-auto"
        initial={{ opacity: 0, rotateX: 15, y: 40 }}
        animate={{ opacity: 1, rotateX: 0, y: 0 }}
        transition={{ duration: 1, ease, delay: 0.3 }}
      >
        <div
          className="rounded-2xl p-8 sm:p-10 shadow-2xl border border-gold/20 relative overflow-hidden"
          style={{
            background:
              "linear-gradient(135deg, var(--paper) 0%, var(--paper-dark) 100%)",
          }}
        >
          {/* Corner accent */}
          <div className="absolute top-0 right-0 w-20 h-20 bg-gradient-to-bl from-gold/10 to-transparent" />
          <div className="absolute bottom-0 left-0 w-16 h-16 bg-gradient-to-tr from-accent/10 to-transparent" />

          {/* Heart SVG */}
          <motion.div
            className="flex justify-center mb-6"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.6, duration: 0.5, type: "spring" }}
          >
            <svg
              width="40"
              height="36"
              viewBox="0 0 40 36"
              fill="none"
              className="text-accent"
            >
              <path
                d="M20 36L17.1 33.36C6.8 24 0 17.84 0 10.2C0 3.96 4.92 0 11.2 0C14.76 0 18.2 1.64 20 4.16C21.8 1.64 25.24 0 28.8 0C35.08 0 40 3.96 40 10.2C40 17.84 33.2 24 22.9 33.36L20 36Z"
                fill="currentColor"
              />
            </svg>
          </motion.div>

          {/* Title */}
          <motion.h1
            className="text-center text-4xl sm:text-5xl mb-2 text-ink"
            style={{ fontFamily: "var(--font-caveat)" }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.6 }}
          >
            Our Story
          </motion.h1>

          {/* Names */}
          <motion.p
            className="text-center text-lg text-muted mb-1"
            style={{ fontFamily: "var(--font-cormorant)" }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.6 }}
          >
            {config.myName} & {config.partnerName}
          </motion.p>

          {/* Gold divider */}
          <motion.div
            className="w-16 h-px bg-gold mx-auto my-5"
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ delay: 0.7, duration: 0.8, ease }}
          />

          {/* Anniversary badge */}
          <motion.div
            className="flex justify-center mb-6"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.75, duration: 0.5 }}
          >
            <div className="px-4 py-1.5 rounded-full border border-gold/40 text-gold text-sm tracking-wider uppercase">
              3 years
            </div>
          </motion.div>

          {/* Days counter */}
          <DaysCounter startDate={config.startDate} />

          {/* Open button */}
          <motion.div
            className="flex justify-center mt-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1, duration: 0.6 }}
          >
            <motion.button
              onClick={onOpen}
              className="px-8 py-3.5 rounded-full bg-accent text-paper font-medium text-lg cursor-pointer shadow-lg shadow-accent/20"
              style={{ fontFamily: "var(--font-inter)" }}
              whileHover={{ scale: 1.05, boxShadow: "0 8px 30px rgba(201,111,111,0.3)" }}
              whileTap={{ scale: 0.97 }}
              animate={{
                boxShadow: [
                  "0 4px 15px rgba(201,111,111,0.15)",
                  "0 4px 25px rgba(201,111,111,0.25)",
                  "0 4px 15px rgba(201,111,111,0.15)",
                ],
              }}
              transition={{
                boxShadow: { duration: 2, repeat: Infinity, ease: "easeInOut" },
              }}
            >
              Open our diary
            </motion.button>
          </motion.div>
        </div>
      </motion.div>
    </div>
  );
}
