"use client";

import { useEffect, useCallback } from "react";
import Image from "next/image";
import { motion, AnimatePresence } from "framer-motion";

interface LightboxProps {
  images: string[];
  currentIndex: number | null;
  onClose: () => void;
  onNavigate: (index: number) => void;
  title: string;
}

export default function Lightbox({
  images,
  currentIndex,
  onClose,
  onNavigate,
  title,
}: LightboxProps) {
  const isOpen = currentIndex !== null;

  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (!isOpen) return;
      if (e.key === "Escape") onClose();
      if (e.key === "ArrowRight" && currentIndex !== null) {
        onNavigate((currentIndex + 1) % images.length);
      }
      if (e.key === "ArrowLeft" && currentIndex !== null) {
        onNavigate(
          (currentIndex - 1 + images.length) % images.length
        );
      }
    },
    [isOpen, currentIndex, images.length, onClose, onNavigate]
  );

  useEffect(() => {
    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "hidden";
    }
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [isOpen, handleKeyDown]);

  return (
    <AnimatePresence>
      {isOpen && currentIndex !== null && (
        <motion.div
          className="fixed inset-0 z-50 flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
        >
          {/* Backdrop */}
          <motion.div
            className="absolute inset-0 bg-ink/80 backdrop-blur-md"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          />

          {/* Close button */}
          <button
            onClick={onClose}
            className="absolute top-4 right-4 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors cursor-pointer"
            aria-label="Close lightbox"
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 20 20"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <line x1="4" y1="4" x2="16" y2="16" />
              <line x1="16" y1="4" x2="4" y2="16" />
            </svg>
          </button>

          {/* Image */}
          <AnimatePresence mode="wait">
            <motion.div
              key={currentIndex}
              className="relative z-10 w-[90vw] h-[80vh] max-w-5xl"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              transition={{ duration: 0.3 }}
            >
              <Image
                src={images[currentIndex]}
                alt={`${title} - image ${currentIndex + 1}`}
                fill
                className="object-contain"
                sizes="90vw"
              />
            </motion.div>
          </AnimatePresence>

          {/* Navigation */}
          {images.length > 1 && (
            <>
              <button
                onClick={() =>
                  onNavigate(
                    (currentIndex - 1 + images.length) % images.length
                  )
                }
                className="absolute left-4 top-1/2 -translate-y-1/2 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors cursor-pointer"
                aria-label="Previous image"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <polyline points="12,4 6,10 12,16" />
                </svg>
              </button>
              <button
                onClick={() =>
                  onNavigate((currentIndex + 1) % images.length)
                }
                className="absolute right-4 top-1/2 -translate-y-1/2 z-10 w-10 h-10 flex items-center justify-center rounded-full bg-white/10 text-white hover:bg-white/20 transition-colors cursor-pointer"
                aria-label="Next image"
              >
                <svg
                  width="20"
                  height="20"
                  viewBox="0 0 20 20"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <polyline points="8,4 14,10 8,16" />
                </svg>
              </button>
            </>
          )}

          {/* Counter */}
          <div
            className="absolute bottom-6 left-1/2 -translate-x-1/2 z-10 text-white/60 text-sm"
            style={{ fontFamily: "var(--font-inter)" }}
          >
            {currentIndex + 1} / {images.length}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
