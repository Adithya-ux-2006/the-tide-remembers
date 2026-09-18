"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { useRouter } from "next/navigation";
import { trySet } from "@/lib/utils";
import { getConfig } from "@/lib/content";

interface Profile {
  name: string;
  emoji: string;
}

export default function ProfileSelect() {
  const [selected, setSelected] = useState<number | null>(null);
  const router = useRouter();
  const config = getConfig();

  const profiles: Profile[] = [
    { name: config.myName, emoji: "👤" },
    { name: config.partnerName, emoji: "👤" },
    { name: "Us", emoji: "❤️" },
  ];

  const handleSelect = (index: number) => {
    setSelected(index);
    trySet("usplus-profile", profiles[index].name);
    setTimeout(() => router.push("/browse"), 600);
  };

  return (
    <motion.div
      className="min-h-screen flex flex-col items-center justify-center bg-bg px-4"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
    >
      <motion.h2
        className="text-3xl sm:text-4xl text-text-dim mb-12"
        style={{ fontFamily: "var(--font-bebas)" }}
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        Who&apos;s watching?
      </motion.h2>

      <div className="flex gap-6 sm:gap-10">
        {profiles.map((profile, i) => (
          <motion.button
            key={profile.name}
            onClick={() => handleSelect(i)}
            className="flex flex-col items-center gap-3 cursor-pointer group"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + i * 0.1 }}
          >
            <motion.div
              className={`w-24 h-24 sm:w-32 sm:h-32 rounded-lg flex items-center justify-center text-5xl sm:text-6xl border-2 transition-colors duration-200 ${
                selected === i
                  ? "border-white bg-white/10"
                  : "border-transparent bg-card group-hover:border-white/50"
              }`}
              animate={selected === i ? { scale: 1.15 } : { scale: 1 }}
              whileHover={{ scale: 1.08 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              {profile.emoji}
            </motion.div>
            <span className="text-sm text-text-dim group-hover:text-text transition-colors">
              {profile.name}
            </span>
          </motion.button>
        ))}
      </div>
    </motion.div>
  );
}
