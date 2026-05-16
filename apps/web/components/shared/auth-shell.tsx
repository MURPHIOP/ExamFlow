import type { ReactNode } from "react";

type AuthShellProps = {
  title: string;
  description: string;
  children: ReactNode;
};

export function AuthShell({ title, description, children }: AuthShellProps) {
  return (
    <main className="min-h-screen px-4 py-10 md:px-6 lg:px-8">
      <div className="mx-auto grid min-h-[calc(100vh-5rem)] max-w-7xl gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div className="relative overflow-hidden rounded-[2rem] border border-border/40 bg-card/70 p-8 shadow-[0_20px_60px_-30px_rgb(0_0_0/0.45)] backdrop-blur-xl md:p-10">
          <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_left,hsl(var(--primary))/0.14,transparent_30%),radial-gradient(circle_at_bottom_right,hsl(var(--secondary))/0.12,transparent_35%)]" />
          <div className="relative z-10">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.28em] text-primary">
              ExamFlow Secure Access
            </p>
            <h1 className="text-4xl font-bold md:text-5xl">{title}</h1>
            <p className="mt-4 max-w-xl text-sm text-muted-foreground md:text-base">
              {description}
            </p>
            <div className="mt-8 grid gap-4 sm:grid-cols-3">
              {[
                "Role-based access",
                "Secure authentication",
                "Premium dashboard routing",
              ].map((item) => (
                <div key={item} className="glass-card p-4 text-sm">
                  {item}
                </div>
              ))}
            </div>
          </div>
        </div>
        <div className="relative overflow-hidden rounded-[2rem] border border-border/40 bg-card/85 p-6 shadow-[0_20px_60px_-30px_rgb(0_0_0/0.45)] backdrop-blur-xl md:p-8">
          <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,hsl(var(--accent))/0.12,transparent_30%)]" />
          <div className="relative z-10">{children}</div>
        </div>
      </div>
    </main>
  );
}
