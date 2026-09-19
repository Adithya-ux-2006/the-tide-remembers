"use client";

import Image from "next/image";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import type { Entry } from "@/lib/types";

interface CardProps {
  entry: Entry;
  index?: number;
}

export default function Card({ entry, index = 0 }: CardProps) {
  const router = useRouter();

  return (
    <motion.div
      className="flex-shrink-0 cursor-pointer group"
      style={{ width: 200 }}
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.1 }}
      transition={{ duration: 0.4, delay: index * 0.04, ease: [0.22, 1, 0.36, 1] as const }}
    >
      <motion.button
        onClick={() => router.push(`/watch/${entry.id}`)}
        className="w-full text-left cursor-pointer block"
        whileHover={{ scale: 1.35, zIndex: 20, y: -20 }}
        transition={{ type: "spring", stiffness: 300, damping: 25 }}
        aria-label={`${entry.title}, Season ${entry.season} Episode ${entry.episode}`}
      >
        {/* Thumbnail */}
        <div className="relative rounded overflow-hidden bg-card aspect-video">
          <Image
            src={entry.thumb}
            alt={entry.title}
            width={320}
            height={180}
            className="w-full h-full object-cover"
            loading="lazy"
          />
          {/* Hover play icon */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-200 flex items-end justify-start p-2">
            <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="black">
                <polygon points="5,3 19,12 5,21" />
              </svg>
            </div>
          </div>
        </div>

        {/* Text below — fixed height container for alignment */}
        <div className="mt-2 h-12 overflow-hidden">
          <p className="text-sm text-text font-medium truncate leading-tight">{entry.title}</p>
          <p className="text-xs text-text-dim mt-1 truncate leading-tight">
            <span className="text-green-400">100% Match</span>
            <span className="mx-1">·</span>
            <span>S{entry.season} E{entry.episode}</span>
          </p>
        </div>
      </motion.button>
    </motion.div>
  );
}
