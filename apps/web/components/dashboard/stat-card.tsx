import type { LucideIcon } from "lucide-react";

type StatCardProps = {
  title: string;
  value: string;
  trend: string;
  icon: LucideIcon;
  tone?: "violet" | "cyan" | "emerald" | "amber";
};

const toneClassMap = {
  violet: "from-indigo-500 to-violet-600",
  cyan: "from-cyan-500 to-sky-600",
  emerald: "from-emerald-500 to-teal-600",
  amber: "from-amber-500 to-orange-600",
} as const;

export function StatCard({ title, value, trend, icon: Icon, tone = "violet" }: StatCardProps) {
  return (
    <article className="rounded-2xl border border-border/70 bg-card p-5 shadow-soft">
      <div className="mb-4 flex items-center justify-between">
        <p className="text-sm font-medium text-muted-foreground">{title}</p>
        <span
          className={`inline-flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br ${toneClassMap[tone]} text-white`}
        >
          <Icon size={16} />
        </span>
      </div>
      <p className="text-3xl font-semibold tracking-tight text-foreground">{value}</p>
      <p className="mt-1 text-xs text-muted-foreground">{trend}</p>
    </article>
  );
}
