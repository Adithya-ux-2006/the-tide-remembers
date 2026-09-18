"use client";

import { useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import Intro from "@/components/Intro";
import Gate from "@/components/Gate";
import ProfileSelect from "@/components/ProfileSelect";
import { getConfig } from "@/lib/content";

type Phase = "intro" | "gate" | "profiles";

export default function HomePage() {
  const [phase, setPhase] = useState<Phase>("intro");
  const router = useRouter();
  const config = getConfig();

  const handleIntroComplete = useCallback(() => {
    if (config.passcode) {
      setPhase("gate");
    } else {
      setPhase("profiles");
    }
  }, [config.passcode]);

  const handleUnlock = useCallback(() => {
    setPhase("profiles");
  }, []);

  return (
    <AnimatePresence mode="wait">
      {phase === "intro" && (
        <motion.div key="intro" exit={{ opacity: 0 }} transition={{ duration: 0.5 }}>
          <Intro appName={config.appName} onComplete={handleIntroComplete} />
        </motion.div>
      )}

      {phase === "gate" && (
        <motion.div
          key="gate"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <Gate passcode={config.passcode} onUnlock={handleUnlock} />
        </motion.div>
      )}

      {phase === "profiles" && (
        <motion.div
          key="profiles"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.5 }}
        >
          <ProfileSelect />
        </motion.div>
      )}
    </AnimatePresence>
  );
}
