"use client";

import { motion } from "framer-motion";
import { RevealContainer, RevealItem } from "@/components/effects/reveal";
import {
  Users,
  CreditCard,
  FileText,
  CheckCircle,
  Award,
  BarChart3,
} from "lucide-react";

const steps = [
  { icon: Users, label: "Apply", description: "Student submits application" },
  { icon: CreditCard, label: "Pay", description: "Razorpay payment" },
  { icon: FileText, label: "Admit", description: "Admit card generation" },
  { icon: CheckCircle, label: "Exam", description: "Conduct exam" },
  { icon: BarChart3, label: "Result", description: "Publish results" },
  { icon: Award, label: "Verify", description: "QR certificate" },
];

export function WorkflowSection() {
  return (
    <section className="py-20 md:py-32">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        <RevealContainer className="mb-16 text-center md:mb-20">
          <RevealItem>
            <h2 className="text-4xl font-bold md:text-5xl">
              Automated Workflow
            </h2>
          </RevealItem>
          <RevealItem>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-muted-foreground">
              From application to certificate verification
            </p>
          </RevealItem>
        </RevealContainer>

        <div className="grid gap-4 md:gap-6">
          <RevealContainer className="flex flex-col md:flex-row items-center justify-between gap-4">
            {steps.map((step, i) => (
              <div key={i} className="flex items-center gap-4 w-full md:w-auto">
                <RevealItem>
                  <motion.div
                    className="glow-card flex h-20 w-20 flex-shrink-0 flex-col items-center justify-center"
                    whileHover={{ scale: 1.1 }}
                  >
                    <step.icon className="h-8 w-8 text-primary" />
                    <div className="text-xs font-semibold mt-1 text-center">
                      {step.label}
                    </div>
                  </motion.div>
                </RevealItem>

                {i < steps.length - 1 && (
                  <motion.div
                    className="hidden md:block h-1 flex-grow bg-gradient-to-r from-primary/30 to-secondary/30"
                    initial={{ scaleX: 0 }}
                    whileInView={{ scaleX: 1 }}
                    transition={{ delay: i * 0.1 }}
                  />
                )}
              </div>
            ))}
          </RevealContainer>

          <RevealContainer className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-6">
            {steps.map((step, i) => (
              <RevealItem key={i}>
                <div className="glass-card p-4 text-center">
                  <div className="text-sm font-semibold text-primary mb-1">
                    {step.label}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {step.description}
                  </div>
                </div>
              </RevealItem>
            ))}
          </RevealContainer>
        </div>
      </div>
    </section>
  );
}
