"use client";

import { useEffect, useState, useRef } from "react";
import { motion, useInView } from "framer-motion";
import { useRouter } from "next/navigation";
import confetti from "canvas-confetti";
import { getConfig } from "@/lib/content";

const ease = [0.22, 1, 0.36, 1] as const;

export default function Credits() {
  const config = getConfig();
  const router = useRouter();
  const [confettiFired, setConfettiFired] = useState(false);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);
  const finaleRef = useRef<HTMLDivElement>(null);
  const isFinaleInView = useInView(finaleRef, { amount: 0.5 });

  useEffect(() => {
    setPrefersReducedMotion(
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  }, []);

  useEffect(() => {
    if (isFinaleInView && !confettiFired && !prefersReducedMotion) {
      setConfettiFired(true);
      try {
        const end = Date.now() + 2000;
        const colors = ["#E5384A", "#F5C16C", "#ffffff"];
        (function frame() {
          confetti({ particleCount: 3, angle: 60, spread: 55, origin: { x: 0, y: 0.7 }, colors });
          confetti({ particleCount: 3, angle: 120, spread: 55, origin: { x: 1, y: 0.7 }, colors });
          if (Date.now() < end) requestAnimationFrame(frame);
        })();
      } catch {}
    }
  }, [isFinaleInView, confettiFired, prefersReducedMotion]);

  const credits = [
    { role: "Starring", names: `${config.myName} & ${config.partnerName}` },
    { role: "Created by", names: "Love" },
    { role: "Directed by", names: "Fate" },
    { role: "Written by", names: "Us" },
    { role: "Produced by", names: "Every single day together" },
    { role: "Filmed on location", names: "Everywhere we've been" },
    { role: "Original score", names: "Our favorite songs" },
    { role: "Special thanks", names: "To everyone who believed in us" },
  ];

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      <div className="max-w-2xl mx-auto px-6 py-24">
        {/* Header */}
        <motion.div
          className="text-center mb-16"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, ease }}
        >
          <h1
            className="text-6xl sm:text-7xl mb-4"
            style={{ fontFamily: "var(--font-bebas)", color: "var(--accent)" }}
          >
            {config.appName}
          </h1>
          <p className="text-text-dim text-sm tracking-widest uppercase">
            Season 3 Finale
          </p>
        </motion.div>

        {/* Credits list */}
        <div className="space-y-8 mb-20">
          {credits.map((credit, i) => (
            <motion.div
              key={credit.role}
              className="text-center"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.6, delay: i * 0.08, ease }}
            >
              <p className="text-text-dim text-xs tracking-widest uppercase mb-1">
                {credit.role}
              </p>
              <p className="text-2xl sm:text-3xl" style={{ fontFamily: "var(--font-bebas)" }}>
                {credit.names}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Final letter */}
        <motion.div
          className="text-center mb-20"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 1 }}
        >
          <div className="w-16 h-px bg-accent mx-auto mb-10" />
          {config.finalLetter.map((para, i) => (
            <motion.p
              key={i}
              className="text-lg sm:text-xl text-white/80 leading-relaxed mb-4"
              style={{ fontFamily: "var(--font-inter)" }}
              initial={{ opacity: 0, y: 15 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, amount: 0.3 }}
              transition={{ duration: 0.6, delay: i * 0.12, ease }}
            >
              {para}
            </motion.p>
          ))}
        </motion.div>

        {/* Renewed for Season 4 */}
        <motion.div
          ref={finaleRef}
          className="text-center"
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8, ease }}
        >
          <p className="text-text-dim text-sm mb-4">Renewed for</p>
          <h2
            className="text-5xl sm:text-6xl mb-6"
            style={{ fontFamily: "var(--font-bebas)", color: "var(--gold)" }}
          >
            Season 4
          </h2>

          {/* Heart */}
          <motion.div
            className="mb-8"
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            transition={{ type: "spring", stiffness: 200, damping: 15, delay: 0.3 }}
          >
            <svg width="40" height="36" viewBox="0 0 40 36" fill="var(--accent)" className="mx-auto">
              <path d="M20 36L17.1 33.36C6.8 24 0 17.84 0 10.2C0 3.96 4.92 0 11.2 0C14.76 0 18.2 1.64 20 4.16C21.8 1.64 25.24 0 28.8 0C35.08 0 40 3.96 40 10.2C40 17.84 33.2 24 22.9 33.36L20 36Z" />
            </svg>
          </motion.div>

          <motion.button
            onClick={() => router.push("/browse")}
            className="px-8 py-3 bg-white/10 border border-white/30 rounded text-white cursor-pointer hover:bg-white/20 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Watch Again
          </motion.button>
        </motion.div>
      </div>
    </div>
  );
}
