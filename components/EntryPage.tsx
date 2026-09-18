"use client";

import { useState, useRef } from "react";
import Image from "next/image";
import { motion, useScroll, useTransform } from "framer-motion";
import Polaroid from "./Polaroid";
import Collage from "./Collage";
import Lightbox from "./Lightbox";
import { formatDate, cn } from "@/lib/utils";
import type { Entry } from "@/lib/types";

interface EntryPageProps {
  entry: Entry;
  index: number;
  priority?: boolean;
}

const ease = [0.22, 1, 0.36, 1] as const;

export default function EntryPage({ entry, index, priority = false }: EntryPageProps) {
  const [lightboxIndex, setLightboxIndex] = useState<number | null>(null);
  const ref = useRef<HTMLElement>(null);

  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const scale = useTransform(scrollYProgress, [0, 0.2, 0.8, 1], [0.98, 1, 1, 0.98]);
  const opacity = useTransform(scrollYProgress, [0, 0.15, 0.85, 1], [0.7, 1, 1, 0.7]);

  const rotation = ((index % 5) - 2) * 1.5;

  const isFullLayout = entry.layout === "full";
  const isCollageLayout = entry.layout === "collage";
  const isLeftLayout = entry.layout === "left";

  const textContent = (
    <motion.div
      className={cn(
        "flex flex-col gap-4",
        isFullLayout && "text-center items-center"
      )}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.6, ease }}
    >
      {/* Date stamp */}
      <motion.div
        className={cn(
          "flex items-center gap-2",
          isFullLayout && "justify-center"
        )}
        initial={{ opacity: 0, x: -10 }}
        whileInView={{ opacity: 1, x: 0 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <time
          dateTime={entry.date}
          className="text-sm text-muted tracking-wider uppercase"
          style={{ fontFamily: "var(--font-inter)" }}
        >
          {formatDate(entry.date)}
        </time>
        {entry.mood && (
          <span className="text-lg" role="img" aria-label="Mood">
            {entry.mood}
          </span>
        )}
      </motion.div>

      {/* Title */}
      <motion.h2
        className={cn(
          "text-3xl sm:text-4xl text-ink",
          isFullLayout ? "text-4xl sm:text-5xl" : ""
        )}
        style={{ fontFamily: "var(--font-caveat)" }}
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.6, delay: 0.15, ease }}
      >
        {entry.title}
      </motion.h2>

      {/* Gold divider */}
      <motion.div
        className={cn("w-12 h-px bg-gold", isFullLayout ? "mx-auto" : "")}
        initial={{ scaleX: 0 }}
        whileInView={{ scaleX: 1 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.6, delay: 0.2, ease }}
        style={{ transformOrigin: "left" }}
      />

      {/* Body paragraphs */}
      {entry.body.split("\n\n").map((para, pi) => (
        <motion.p
          key={pi}
          className="text-lg sm:text-xl leading-relaxed text-ink/85"
          style={{ fontFamily: "var(--font-cormorant)" }}
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, delay: 0.25 + pi * 0.08, ease }}
        >
          {para}
        </motion.p>
      ))}

      {/* Caption */}
      {entry.caption && (
        <motion.p
          className={cn(
            "text-sm text-muted italic mt-2",
            isFullLayout && "text-center"
          )}
          style={{ fontFamily: "var(--font-cormorant)" }}
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          {entry.caption}
        </motion.p>
      )}
    </motion.div>
  );

  const imageContent = (() => {
    if (isCollageLayout) {
      return (
        <Collage
          images={entry.images}
          title={entry.title}
          onImageClick={(i) => setLightboxIndex(i)}
        />
      );
    }

    if (isFullLayout && entry.images[0]) {
      return (
        <motion.div
          className="relative w-full h-[50vh] sm:h-[60vh] overflow-hidden rounded-lg"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.8 }}
        >
          <motion.div
            className="absolute inset-0"
            style={{
              y: useTransform(scrollYProgress, [0, 1], ["-8%", "8%"]),
            }}
          >
            <Image
              src={entry.images[0]}
              alt={entry.caption || entry.title}
              fill
              className="object-cover scale-110"
              sizes="100vw"
              priority={priority}
            />
          </motion.div>
          {/* Gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-ink/60 via-transparent to-transparent" />
        </motion.div>
      );
    }

    if (entry.images[0]) {
      return (
        <Polaroid
          src={entry.images[0]}
          alt={entry.caption || entry.title}
          rotation={rotation}
          onClick={() => setLightboxIndex(0)}
          priority={priority}
        />
      );
    }

    return null;
  })();

  return (
    <>
      <motion.article
        ref={ref}
        id={`entry-${entry.id}`}
        className="min-h-screen flex items-center py-16 sm:py-24 px-4 sm:px-8"
        style={{ scale, opacity }}
      >
        <div className="w-full max-w-5xl mx-auto">
          {isFullLayout ? (
            <div className="flex flex-col gap-8">
              {imageContent}
              <div className="max-w-2xl mx-auto">{textContent}</div>
            </div>
          ) : isCollageLayout ? (
            <div className="flex flex-col lg:flex-row gap-8 lg:gap-12 items-center">
              <div className="w-full lg:w-1/2">{imageContent}</div>
              <div className="w-full lg:w-1/2">{textContent}</div>
            </div>
          ) : (
            <div
              className={cn(
                "flex flex-col lg:flex-row gap-8 lg:gap-12 items-center",
                !isLeftLayout && "lg:flex-row-reverse"
              )}
            >
              <div className="w-full lg:w-1/2 flex justify-center">
                {imageContent}
              </div>
              <div className="w-full lg:w-1/2">{textContent}</div>
            </div>
          )}

          {/* Page number */}
          <motion.div
            className="mt-12 text-center text-xs text-muted/50"
            style={{ fontFamily: "var(--font-inter)" }}
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            — {index + 1} —
          </motion.div>
        </div>
      </motion.article>

      {/* Lightbox */}
      <Lightbox
        images={entry.images}
        currentIndex={lightboxIndex}
        onClose={() => setLightboxIndex(null)}
        onNavigate={setLightboxIndex}
        title={entry.title}
      />
    </>
  );
}
