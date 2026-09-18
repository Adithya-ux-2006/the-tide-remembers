"use client";

import { useEffect, useCallback } from "react";
import Image from "next/image";
import { motion, AnimatePresence } from "framer-motion";
import { useRouter } from "next/navigation";
import type { Entry } from "@/lib/types";
import { formatDate } from "@/lib/utils";

interface DetailModalProps {
  entry: Entry | null;
  onClose: () => void;
}

export default function DetailModal({ entry, onClose }: DetailModalProps) {
  const router = useRouter();

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    },
    [onClose]
  );

  useEffect(() => {
    if (entry) {
      document.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [entry, handleKeyDown]);

  return (
    <AnimatePresence>
      {entry && (
        <motion.div
          className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          {/* Backdrop */}
          <div className="fixed inset-0 bg-black/70 backdrop-blur-sm" onClick={onClose} />

          {/* Modal */}
          <motion.div
            className="relative z-10 w-full max-w-3xl mx-4 my-8 sm:my-16 rounded-lg overflow-hidden bg-bg-elev shadow-2xl"
            layoutId={`card-${entry.id}`}
            transition={{ type: "spring", stiffness: 260, damping: 28 }}
          >
            {/* Close */}
            <button
              onClick={onClose}
              className="absolute top-4 right-4 z-20 w-8 h-8 rounded-full bg-bg-elev/80 flex items-center justify-center text-text-dim hover:text-text cursor-pointer"
              aria-label="Close"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>

            {/* Backdrop image */}
            <div className="relative h-64 sm:h-80">
              {entry.backdrop && (
                <Image
                  src={entry.backdrop}
                  alt={entry.title}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, 768px"
                />
              )}
              <div className="absolute inset-0 bg-gradient-to-t from-bg-elev via-bg-elev/50 to-transparent" />

              {/* Title overlay */}
              <div className="absolute bottom-6 left-6 right-6">
                <h2 className="text-4xl sm:text-5xl mb-3" style={{ fontFamily: "var(--font-bebas)" }}>
                  {entry.title}
                </h2>
                <div className="flex items-center gap-3 text-sm">
                  <motion.button
                    onClick={() => router.push(`/watch/${entry.id}`)}
                    className="flex items-center gap-2 px-5 py-2 bg-white text-black rounded font-semibold text-sm cursor-pointer"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                      <polygon points="5,3 19,12 5,21" />
                    </svg>
                    Play
                  </motion.button>
                  <button className="w-9 h-9 rounded-full border-2 border-text-dim/50 flex items-center justify-center text-text-dim hover:border-text hover:text-text transition-colors cursor-pointer" aria-label="Add to list">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <line x1="12" y1="5" x2="12" y2="19" />
                      <line x1="5" y1="12" x2="19" y2="12" />
                    </svg>
                  </button>
                  <button className="w-9 h-9 rounded-full border-2 border-text-dim/50 flex items-center justify-center text-text-dim hover:border-text hover:text-text transition-colors cursor-pointer" aria-label="Like">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                      <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3zM7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            {/* Details */}
            <div className="p-6">
              <div className="flex items-center gap-3 text-sm mb-4">
                <span className="text-green-400 font-semibold">100% Match</span>
                <span className="text-text-dim">{formatDate(entry.date)}</span>
                {entry.runtime && <span className="text-text-dim">{entry.runtime}</span>}
                <span className="px-1.5 py-0.5 border border-text-dim/50 text-text-dim text-xs rounded">Rated: Forever</span>
              </div>

              <p className="text-text-dim text-sm leading-relaxed mb-6">
                {entry.synopsis}
              </p>

              {/* Tags */}
              <div className="flex flex-wrap gap-2 mb-6">
                {entry.tags.map((tag) => (
                  <span key={tag} className="px-3 py-1 bg-card rounded-full text-xs text-text-dim">
                    {tag}
                  </span>
                ))}
              </div>

              {/* Episode info */}
              <div className="border-t border-white/10 pt-4">
                <p className="text-sm text-text-dim">
                  Season {entry.season} · Episode {entry.episode} · {formatDate(entry.date)}
                </p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
