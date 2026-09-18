"use client";

import { useRef } from "react";
import Image from "next/image";
import { motion, useScroll, useTransform } from "framer-motion";

interface CollageProps {
  images: string[];
  title: string;
  onImageClick?: (index: number) => void;
}

const rotations = [-3, 2, -1.5, 3];

export default function Collage({ images, title, onImageClick }: CollageProps) {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start end", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], ["-5%", "5%"]);

  return (
    <div ref={ref} className="relative w-full aspect-[4/3] sm:aspect-[16/10]">
      {images.slice(0, 4).map((src, i) => {
        const rotation = rotations[i % rotations.length];
        const positions = [
          { top: "0%", left: "0%", width: "60%", height: "65%", zIndex: 2 },
          { top: "5%", left: "35%", width: "60%", height: "65%", zIndex: 1 },
          { top: "30%", left: "5%", width: "55%", height: "60%", zIndex: 3 },
          { top: "35%", left: "40%", width: "55%", height: "60%", zIndex: 2 },
        ];
        const pos = positions[i];

        return (
          <motion.div
            key={src}
            className="absolute p-2 bg-white rounded-sm shadow-lg cursor-pointer"
            style={{
              top: pos.top,
              left: pos.left,
              width: pos.width,
              height: pos.height,
              zIndex: pos.zIndex,
              rotate: rotation,
            }}
            whileHover={{
              y: -4,
              rotate: 0,
              scale: 1.02,
              zIndex: 10,
              transition: { duration: 0.25 },
            }}
            onClick={() => onImageClick?.(i)}
            role="button"
            tabIndex={0}
            aria-label={`View image ${i + 1} of ${title}`}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onImageClick?.(i);
              }
            }}
          >
            <motion.div className="relative w-full h-full overflow-hidden" style={{ y }}>
              <Image
                src={src}
                alt={`${title} - image ${i + 1}`}
                fill
                className="object-cover"
                sizes="(max-width: 768px) 80vw, 40vw"
              />
            </motion.div>
          </motion.div>
        );
      })}
    </div>
  );
}
