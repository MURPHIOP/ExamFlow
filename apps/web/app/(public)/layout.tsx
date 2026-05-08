"use client";

import Link from "next/link";
import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { ThemeToggle } from "@/components/shared/theme-toggle";
import { Footer } from "@/components/landing/footer";
import { ScrollProgress } from "@/components/effects/scroll-progress";

export default function PublicLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen dashboard-shell-bg">
      <ScrollProgress />

      <header className="sticky top-0 z-40 border-b border-border/20 bg-card/50 backdrop-blur-xl">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 md:px-6">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Link href="/" className="glass-card px-4 py-2 hover:border-primary/50">
              <p className="text-lg font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                ExamFlow
              </p>
              <p className="text-xs text-muted-foreground">M.B. Technosoft</p>
            </Link>
          </motion.div>

          {/* Navigation */}
          <nav className="flex items-center gap-4">
            <Link
              href="/login"
              className="rounded-lg px-4 py-2 text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
            >
              Login
            </Link>
            <Link
              href="/register/student"
              className="premium-button text-sm"
            >
              Apply Now
            </Link>
            <ThemeToggle />
          </nav>
        </div>
      </header>

      <main className="min-h-screen">{children}</main>

      <Footer />
    </div>
  );
}
