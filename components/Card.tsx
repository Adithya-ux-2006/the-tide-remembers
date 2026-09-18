"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import type { Entry } from "@/lib/types";

interface CardProps {
  entry: Entry;
  index?: number;
  rank?: number;
  showProgress?: boolean;
  progress?: number;
}

export default function Card({ entry, index = 0, rank, showProgress = false, progress = 0 }: CardProps) {
  const router = useRouter();

  return (
    <motion.div
      className="relative flex-shrink-0 cursor-pointer group"
      style={{ width: "var(--card-w, 200px)" }}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.1 }}
      transition={{ duration: 0.4, delay: index * 0.04, ease: [0.22, 1, 0.36, 1] }}
    >
      <motion.button
        onClick={() => router.push(`/watch/${entry.id}`)}
        className="w-full text-left cursor-pointer"
        whileHover={{ scale: 1.35, zIndex: 20, y: -20 }}
        transition={{ type: "spring", stiffness: 300, damping: 25 }}
        aria-label={`${entry.title}, Season ${entry.season} Episode ${entry.episode}`}
      >
        <div className="relative rounded overflow-hidden bg-card aspect-video">
          {/* Rank number for top10 */}
          {rank !== undefined && (
            <div className="absolute left-1 bottom-0 z-10 text-6xl font-bold text-white/20 leading-none" style={{ fontFamily: "var(--font-bebas)" }}>
              {rank}
            </div>
          )}

          <Image
            src={entry.thumb}
            alt={entry.title}
            width={320}
            height={180}
            className="w-full h-full object-cover"
            loading="lazy"
          />

          {/* Hover overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-200">
            <div className="absolute bottom-2 left-2 right-2 flex items-center gap-2">
              <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="black">
                  <polygon points="5,3 19,12 5,21" />
                </svg>
              </div>
            </div>
          </div>

          {/* Progress bar */}
          {showProgress && progress > 0 && (
            <div className="absolute bottom-0 left-0 right-0 h-1 bg-white/20">
              <div className="h-full bg-accent" style={{ width: `${Math.min(progress, 100)}%` }} />
            </div>
          )}
        </div>

        {/* Info below card */}
        <div className="mt-2 px-0.5">
          <p className="text-sm text-text truncate">{entry.title}</p>
          <p className="text-xs text-text-dim mt-0.5">
            <span className="text-green-400">100% Match</span> · S{entry.season} E{entry.episode}
            {entry.runtime && ` · ${entry.runtime}`}
          </p>
        </div>
      </motion.button>
    </motion.div>
  );
}
