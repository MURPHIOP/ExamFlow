import type { ReactNode } from "react";

import { AppSidebar } from "@/components/app-sidebar";
import { TopNavbar } from "@/components/top-navbar";

type DashboardShellProps = {
  children: ReactNode;
};

export function DashboardShell({ children }: DashboardShellProps) {
  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,hsl(var(--brand-soft))/0.25,transparent_45%),radial-gradient(circle_at_80%_0,hsl(var(--brand-alt))/0.16,transparent_35%)]">
      <AppSidebar />
      <main className="md:ml-72">
        <div className="mx-auto max-w-[1600px] space-y-4 p-4 md:p-6">
          <TopNavbar />
          {children}
        </div>
      </main>
    </div>
  );
}
