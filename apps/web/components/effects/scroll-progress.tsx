"use client";

import { motion, useScroll, useTransform } from "framer-motion";

export function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <motion.div
      className="fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-primary via-secondary to-accent origin-left"
      style={{ scaleX }}
      initial={{ scaleX: 0 }}
    />
  );
}

interface ScrolledParallaxProps {
  children: React.ReactNode;
  offset?: number;
  className?: string;
}

export function ScrollParallax({
  children,
  offset = 50,
  className = "",
}: ScrolledParallaxProps) {
  const { scrollY } = useScroll();
  const y = useTransform(scrollY, [0, 300], [0, offset]);

  return (
    <motion.div className={className} style={{ y }}>
      {children}
    </motion.div>
  );
}

interface CounterProps {
  from?: number;
  to: number;
  duration?: number;
}

export function AnimatedCounter({
  from = 0,
  to,
  duration = 2,
}: CounterProps) {
  return (
    <motion.span>
      {to}
    </motion.span>
  );
}
