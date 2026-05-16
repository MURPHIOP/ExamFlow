import type { ReactNode } from "react";

type PageFrameProps = {
  eyebrow?: string;
  title: string;
  description?: string;
  children?: ReactNode;
  actions?: ReactNode;
};

export function PageFrame({
  eyebrow,
  title,
  description,
  children,
  actions,
}: PageFrameProps) {
  return (
    <section className="relative overflow-hidden rounded-[2rem] border border-border/40 bg-card/70 p-6 shadow-[0_20px_60px_-30px_rgb(0_0_0/0.45)] backdrop-blur-xl md:p-8">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,hsl(var(--primary))/0.15,transparent_30%),radial-gradient(circle_at_bottom_left,hsl(var(--secondary))/0.12,transparent_35%)]" />
      <div className="relative z-10">
        {eyebrow ? (
          <p className="mb-3 text-xs font-semibold uppercase tracking-[0.32em] text-primary">
            {eyebrow}
          </p>
        ) : null}
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <h1 className="text-3xl font-bold md:text-4xl">{title}</h1>
            {description ? (
              <p className="mt-3 max-w-3xl text-sm text-muted-foreground md:text-base">
                {description}
              </p>
            ) : null}
          </div>
          {actions ? <div className="flex flex-wrap gap-3">{actions}</div> : null}
        </div>
        {children ? <div className="relative z-10 mt-8">{children}</div> : null}
      </div>
    </section>
  );
}
