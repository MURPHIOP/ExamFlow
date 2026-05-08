"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight, PlayCircle } from "lucide-react";
import { MotionWrapper, StaggerContainer, StaggerItem } from "@/components/effects/motion-wrapper";
import { FloatingOrb } from "@/components/effects/glow-orb";
import { GradientText } from "@/components/effects/animated-gradient";

export function HeroSection() {
  return (
    <section className="relative overflow-hidden py-20 md:py-32 lg:py-40">
      {/* Animated background */}
      <FloatingOrb size="lg" position={{ top: "-10%", left: "-5%" }} />
      <FloatingOrb size="md" position={{ bottom: "10%", right: "-3%" }} delay={2} />

      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <StaggerContainer delay={0.1}>
          {/* Main headline */}
          <StaggerItem>
            <motion.div className="text-center">
              <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/5 px-4 py-2">
                <span className="relative flex h-2 w-2">
                  <span className="absolute inline-flex h-full w-full animate-pulse rounded-full bg-primary opacity-75"></span>
                  <span className="relative inline-flex h-2 w-2 rounded-full bg-primary"></span>
                </span>
                <span className="text-sm font-medium text-primary">Now Live: ExamFlow Platform</span>
              </div>

              <h1 className="mb-6 text-5xl font-bold tracking-tight md:text-6xl lg:text-7xl">
                <GradientText>Automate Exams,</GradientText>
                <br />
                Results & Certificates
              </h1>

              <p className="mx-auto mb-8 max-w-2xl text-lg text-muted-foreground md:text-xl">
                A complete digital examination platform for cultural, art, academic and skill-based exam boards.
                Manage applications, payments, admit cards, results and certificates in one unified dashboard.
              </p>

              {/* CTA Buttons */}
              <motion.div
                className="flex flex-col gap-4 sm:flex-row sm:justify-center sm:gap-4"
                variants={{
                  hidden: { opacity: 0, y: 20 },
                  visible: { opacity: 1, y: 0 },
                }}
                transition={{ delay: 0.3 }}
              >
                <Link
                  href="/register/student"
                  className="premium-button inline-flex items-center justify-center gap-2"
                >
                  Start Application
                  <ArrowRight className="h-4 w-4" />
                </Link>
                <button className="inline-flex items-center justify-center gap-2 rounded-xl border border-primary/30 px-6 py-3 font-semibold text-foreground transition-all hover:bg-primary/5 hover:border-primary/50">
                  <PlayCircle className="h-4 w-4" />
                  View Demo
                </button>
              </motion.div>
            </motion.div>
          </StaggerItem>

          {/* Hero Preview Card */}
          <StaggerItem>
            <motion.div
              className="mt-16 md:mt-20"
              variants={{
                hidden: { opacity: 0, scale: 0.95 },
                visible: { opacity: 1, scale: 1 },
              }}
              transition={{ delay: 0.4 }}
            >
              <div className="glow-card relative overflow-hidden">
                {/* Animated background grid */}
                <div className="absolute inset-0 bg-grid-white/5 [mask-image:linear-gradient(0deg,transparent,rgba(255,255,255,0.1))]" />

                {/* Hero preview content */}
                <div className="relative p-8 md:p-12">
                  <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
                    {[
                      {
                        number: "2.5K+",
                        label: "Applications",
                        icon: "📋",
                      },
                      { number: "₹50L+", label: "Processed", icon: "💳" },
                      { number: "100%", label: "Verified", icon: "✓" },
                      { number: "24/7", label: "Support", icon: "🎧" },
                    ].map((stat, i) => (
                      <motion.div
                        key={i}
                        className="rounded-2xl bg-card/50 p-4 backdrop-blur-md"
                        whileHover={{ scale: 1.05, y: -5 }}
                      >
                        <div className="text-3xl mb-2">{stat.icon}</div>
                        <div className="text-2xl font-bold text-primary">
                          {stat.number}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {stat.label}
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          </StaggerItem>
        </StaggerContainer>
      </div>
    </section>
  );
}
