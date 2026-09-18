"use client";

import { useRef } from "react";
import Image from "next/image";
import { motion, useScroll, useTransform } from "framer-motion";
import { cn } from "@/lib/utils";

interface PolaroidProps {
  src: string;
  alt: string;
  rotation?: number;
  onClick?: () => void;
  parallax?: boolean;
  priority?: boolean;
}

export default function Polaroid({
  src,
  alt,
  rotation = 0,
  onClick,
  parallax = true,
  priority = false,
}: PolaroidProps) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], ["-8%", "8%"]);

  return (
    <motion.div
      ref={ref}
      className={cn(
        "relative cursor-pointer group",
        "p-2.5 sm:p-3 bg-white rounded-sm shadow-lg",
        "hover:shadow-2xl transition-shadow duration-300"
      )}
      style={{
        rotate: rotation,
        transformOrigin: "center center",
      }}
      whileHover={{
        y: -6,
        rotate: 0,
        transition: { duration: 0.3, ease: [0.22, 1, 0.36, 1] },
      }}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={
        onClick
          ? (e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onClick();
              }
            }
          : undefined
      }
      aria-label={onClick ? `View ${alt}` : undefined}
    >
      <div className="relative overflow-hidden bg-paper-dark aspect-[4/3]">
        {parallax ? (
          <motion.div className="absolute inset-0" style={{ y }}>
            <Image
              src={src}
              alt={alt}
              fill
              className="object-cover scale-110"
              sizes="(max-width: 768px) 90vw, 40vw"
              priority={priority}
            />
          </motion.div>
        ) : (
          <Image
            src={src}
            alt={alt}
            fill
            className="object-cover"
            sizes="(max-width: 768px) 90vw, 40vw"
            priority={priority}
          />
        )}
      </div>
      {/* Tape strip accent */}
      <div className="absolute -top-1.5 left-1/2 -translate-x-1/2 w-12 h-3 bg-gold/20 rounded-sm rotate-1" />
    </motion.div>
  );
}
