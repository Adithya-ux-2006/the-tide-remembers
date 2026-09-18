"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import Cover from "@/components/Cover";
import Gate from "@/components/Gate";
import SmoothScroll from "@/components/SmoothScroll";
import { getConfig } from "@/lib/content";

const ease = [0.22, 1, 0.36, 1] as const;

export default function HomePage() {
  const [unlocked, setUnlocked] = useState(false);
  const [transitioning, setTransitioning] = useState(false);
  const router = useRouter();
  const config = getConfig();

  const handleUnlock = useCallback(() => {
    setUnlocked(true);
  }, []);

  const handleOpen = useCallback(() => {
    setTransitioning(true);
    setTimeout(() => {
      router.push("/diary");
    }, 1000);
  }, [router]);

  const needsGate = !!config.passcode;

  return (
    <SmoothScroll>
      <AnimatePresence mode="wait">
        {transitioning ? (
          <motion.div
            key="curtain"
            className="fixed inset-0 z-50 flex"
            initial={{ opacity: 1 }}
            animate={{ opacity: 1 }}
          >
            {/* Left curtain */}
            <motion.div
              className="w-1/2 h-full bg-paper-dark"
              initial={{ x: 0 }}
              animate={{ x: "-100%" }}
              transition={{ duration: 0.9, ease }}
            />
            {/* Right curtain */}
            <motion.div
              className="w-1/2 h-full bg-paper-dark"
              initial={{ x: 0 }}
              animate={{ x: "100%" }}
              transition={{ duration: 0.9, ease }}
            />
          </motion.div>
        ) : (
          <motion.div
            key="cover"
            initial={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            {needsGate && !unlocked ? (
              <Gate passcode={config.passcode} onUnlock={handleUnlock} />
            ) : (
              <Cover onOpen={handleOpen} />
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </SmoothScroll>
  );
}
