"use client";

import { motion } from "framer-motion";
import {
  FileText,
  CreditCard,
  CheckCircle,
  MapPin,
  Ticket,
  BarChart3,
  Award,
  Sparkles,
  Lock,
  TrendingUp,
} from "lucide-react";
import { RevealContainer, RevealItem } from "@/components/effects/reveal";

const features = [
  {
    icon: FileText,
    title: "Online Applications",
    description: "Simple, guided application process with form validation",
  },
  {
    icon: CreditCard,
    title: "Razorpay Payments",
    description: "Secure payment processing with receipt generation",
  },
  {
    icon: CheckCircle,
    title: "Admin Verification",
    description: "Queue-based verification workflow with status tracking",
  },
  {
    icon: MapPin,
    title: "Centre Allocation",
    description: "Intelligent exam centre assignment with capacity management",
  },
  {
    icon: Ticket,
    title: "Admit Cards",
    description: "Automated admit card generation with QR codes",
  },
  {
    icon: BarChart3,
    title: "Results Publishing",
    description: "Secure result portal with analytics dashboard",
  },
  {
    icon: Award,
    title: "QR Certificates",
    description: "Digital certificates with QR verification",
  },
  {
    icon: Sparkles,
    title: "AI Admin Tools",
    description: "OCR, duplicate detection, spelling suggestions",
  },
  {
    icon: Lock,
    title: "Role-Based Access",
    description: "Students, institutions, admins - secure access control",
  },
  {
    icon: TrendingUp,
    title: "Reports & Analytics",
    description: "Comprehensive dashboards and export capabilities",
  },
];

export function FeaturesSection() {
  return (
    <section className="py-20 md:py-32">
      <div className="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <RevealContainer className="mb-16 text-center md:mb-20">
          <RevealItem>
            <h2 className="text-4xl font-bold md:text-5xl">
              Complete Exam Platform
            </h2>
          </RevealItem>
          <RevealItem>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-muted-foreground">
              Everything you need to digitize and automate your examination board
            </p>
          </RevealItem>
        </RevealContainer>

        {/* Features grid */}
        <RevealContainer className="grid gap-6 md:grid-cols-2 lg:grid-cols-5">
          {features.map((feature, i) => (
            <RevealItem key={i}>
              <motion.div
                className="glow-card group p-6 h-full"
                whileHover={{ y: -5, scale: 1.02 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <motion.div
                  className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary"
                  whileHover={{ scale: 1.2, rotate: 5 }}
                >
                  <feature.icon className="h-6 w-6" />
                </motion.div>

                <h3 className="mb-2 font-semibold text-foreground">
                  {feature.title}
                </h3>
                <p className="text-sm text-muted-foreground">
                  {feature.description}
                </p>
              </motion.div>
            </RevealItem>
          ))}
        </RevealContainer>
      </div>
    </section>
  );
}
