"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

export function CTASection() {
  return (
    <section className="py-20 md:py-32">
      <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
        <motion.div
          className="glow-card relative overflow-hidden p-12 md:p-16 text-center"
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="relative z-10">
            <h2 className="text-4xl font-bold md:text-5xl mb-6">
              Ready to digitize your exam board?
            </h2>
            <p className="text-lg text-muted-foreground mb-8">
              Join hundreds of examination boards automating their operations with ExamFlow.
            </p>

            <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
              <Link
                href="/register/student"
                className="premium-button inline-flex items-center justify-center gap-2"
              >
                Start for Free
                <ArrowRight className="h-4 w-4" />
              </Link>
              <button className="inline-flex items-center justify-center rounded-xl border border-primary/30 px-6 py-3 font-semibold text-foreground transition-all hover:bg-primary/5 hover:border-primary/50">
                Contact Sales
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
