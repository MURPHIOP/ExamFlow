import Link from "next/link";
import type { ReactNode } from "react";

import { ThemeToggle } from "@/components/theme-toggle";

export default function PublicLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen">
      <header className="mx-auto flex max-w-7xl items-center justify-between px-4 py-6 md:px-6">
        <Link href="/home" className="rounded-xl bg-card px-4 py-2 shadow-soft">
          <p className="text-lg font-semibold">ExamFlow</p>
          <p className="text-xs text-muted-foreground">by M.B. Technosoft</p>
        </Link>

        <nav className="flex items-center gap-3">
          <Link href="/login" className="rounded-xl px-4 py-2 text-sm font-medium hover:bg-secondary">
            Login
          </Link>
          <Link
            href="/register"
            className="rounded-xl bg-primary px-4 py-2 text-sm font-medium text-primary-foreground"
          >
            Register
          </Link>
          <ThemeToggle />
        </nav>
      </header>

      <main className="mx-auto max-w-7xl px-4 pb-10 md:px-6">{children}</main>
    </div>
  );
}
