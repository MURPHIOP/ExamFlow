import { Bell, Search } from "lucide-react";

import { ThemeToggle } from "@/components/theme-toggle";

export function TopNavbar() {
  return (
    <header className="sticky top-0 z-20 flex h-16 items-center justify-between rounded-2xl border border-border/80 bg-card/80 px-4 shadow-soft backdrop-blur-xl md:px-6">
      <div className="flex items-center gap-3 rounded-xl border border-border bg-background px-3 py-2 text-sm text-muted-foreground md:min-w-80">
        <Search size={16} />
        <span>Search applications, students, payments...</span>
      </div>

      <div className="flex items-center gap-2 md:gap-3">
        <button
          type="button"
          className="hidden rounded-xl border border-border bg-secondary px-3 py-2 text-sm font-medium text-secondary-foreground transition hover:opacity-90 md:inline-flex"
        >
          Quick Action
        </button>

        <button
          type="button"
          className="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-border bg-card text-foreground transition hover:bg-secondary"
          aria-label="Notifications"
        >
          <Bell size={18} />
        </button>

        <ThemeToggle />
      </div>
    </header>
  );
}
