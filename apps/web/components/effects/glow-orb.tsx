"use client";

import { motion } from "framer-motion";

export function GlowOrb() {
  return (
    <motion.div
      className="absolute inset-0 -z-10"
      animate={{
        scale: [1, 1.1, 1],
        opacity: [0.3, 0.5, 0.3],
      }}
      transition={{
        duration: 4,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    >
      <div className="absolute inset-1/4 rounded-full bg-gradient-to-r from-primary/30 to-secondary/30 blur-3xl" />
    </motion.div>
  );
}

interface FloatingOrbProps {
  delay?: number;
  size?: "sm" | "md" | "lg";
  position?: {
    top?: string;
    right?: string;
    bottom?: string;
    left?: string;
  };
}

export function FloatingOrb({
  delay = 0,
  size = "md",
  position = {},
}: FloatingOrbProps) {
  const sizeClass = {
    sm: "h-24 w-24",
    md: "h-40 w-40",
    lg: "h-64 w-64",
  };

  return (
    <motion.div
      className={`absolute rounded-full blur-3xl ${sizeClass[size]}`}
      style={position}
      animate={{
        y: [0, -20, 0],
        x: [0, 10, 0],
      }}
      transition={{
        duration: 6,
        delay,
        repeat: Infinity,
        ease: "easeInOut",
      }}
    >
      <div className="h-full w-full rounded-full bg-gradient-to-br from-primary/20 to-secondary/20" />
    </motion.div>
  );
}
