"use client";

import { useRef, useEffect, useState } from "react";
import { motion, useScroll, useTransform, useInView } from "framer-motion";
import confetti from "canvas-confetti";

interface FinalPageProps {
  finalLetter: string;
}

const ease = [0.22, 1, 0.36, 1] as const;

export default function FinalPage({ finalLetter }: FinalPageProps) {
  const ref = useRef<HTMLElement>(null);
  const isInView = useInView(ref, { amount: 0.6 });
  const [confettiFired, setConfettiFired] = useState(false);
  const [prefersReducedMotion, setPrefersReducedMotion] = useState(false);

  useEffect(() => {
    setPrefersReducedMotion(
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  }, []);

  useEffect(() => {
    if (isInView && !confettiFired && !prefersReducedMotion) {
      setConfettiFired(true);
      try {
        const end = Date.now() + 1500;
        const colors = ["#c96f6f", "#e8b4a0", "#c9a46a", "#fbf6ee"];
        (function frame() {
          confetti({
            particleCount: 3,
            angle: 60,
            spread: 55,
            origin: { x: 0, y: 0.7 },
            colors,
          });
          confetti({
            particleCount: 3,
            angle: 120,
            spread: 55,
            origin: { x: 1, y: 0.7 },
            colors,
          });
          if (Date.now() < end) requestAnimationFrame(frame);
        })();
      } catch {}
    }
  }, [isInView, confettiFired, prefersReducedMotion]);

  const paragraphs = finalLetter.split("\n\n");

  return (
    <motion.section
      ref={ref}
      className="min-h-screen flex flex-col items-center justify-center py-24 px-6 relative overflow-hidden"
      style={{
        background:
          "linear-gradient(180deg, var(--paper-dark) 0%, #2b2320 60%, #1a1512 100%)",
      }}
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true, amount: 0.2 }}
      transition={{ duration: 1 }}
    >
      {/* Decorative elements */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-[10%] left-[20%] w-40 h-40 rounded-full bg-accent/5" />
        <div className="absolute bottom-[20%] right-[10%] w-32 h-32 rounded-full bg-gold/5" />
      </div>

      <div className="max-w-xl mx-auto text-center relative z-10">
        {/* Heading */}
        <motion.h2
          className="text-4xl sm:text-5xl text-paper mb-8"
          style={{ fontFamily: "var(--font-caveat)" }}
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8, delay: 0.2, ease }}
        >
          For You
        </motion.h2>

        {/* Love letter paragraphs */}
        {paragraphs.map((para, i) => (
          <motion.p
            key={i}
            className="text-lg sm:text-xl leading-relaxed text-paper/80 mb-6"
            style={{ fontFamily: "var(--font-cormorant)" }}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, amount: 0.3 }}
            transition={{ duration: 0.6, delay: 0.3 + i * 0.15, ease }}
          >
            {para}
          </motion.p>
        ))}

        {/* Divider */}
        <motion.div
          className="w-16 h-px bg-gold mx-auto my-10"
          initial={{ scaleX: 0 }}
          whileInView={{ scaleX: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.5, ease }}
        />

        {/* Closing */}
        <motion.p
          className="text-2xl sm:text-3xl text-paper/90 mb-8"
          style={{ fontFamily: "var(--font-caveat)" }}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.6 }}
        >
          Here&apos;s to many more years
        </motion.p>

        {/* Heart SVG with path animation */}
        <motion.div
          className="flex justify-center"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.7 }}
        >
          <motion.svg
            width="60"
            height="54"
            viewBox="0 0 40 36"
            fill="none"
            className="text-accent"
            initial={{ scale: 0.8 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.8 }}
          >
            <motion.path
              d="M20 36L17.1 33.36C6.8 24 0 17.84 0 10.2C0 3.96 4.92 0 11.2 0C14.76 0 18.2 1.64 20 4.16C21.8 1.64 25.24 0 28.8 0C35.08 0 40 3.96 40 10.2C40 17.84 33.2 24 22.9 33.36L20 36Z"
              fill="currentColor"
              initial={{ pathLength: 0 }}
              whileInView={{ pathLength: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 1.5, delay: 0.9, ease }}
            />
          </motion.svg>
        </motion.div>
      </div>
    </motion.section>
  );
}
