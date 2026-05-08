import {
  Bot,
  FileCheck2,
  FileText,
  IdCard,
  ReceiptText,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import { SectionCard } from "@/components/section-card";
import { StatCard } from "@/components/stat-card";
import { StatusBadge } from "@/components/status-badge";

const stats = [
  { title: "Applications", value: "1,284", trend: "+8.3% this week", icon: FileText, tone: "violet" as const },
  { title: "Payments", value: "1,107", trend: "86% payment success", icon: ReceiptText, tone: "emerald" as const },
  { title: "Admit Cards", value: "943", trend: "Pending generation: 98", icon: IdCard, tone: "cyan" as const },
  { title: "Certificates", value: "612", trend: "Issued this session", icon: ShieldCheck, tone: "amber" as const },
  { title: "AI Review Queue", value: "47", trend: "Needs admin decision", icon: Bot, tone: "violet" as const },
  { title: "Pending Verification", value: "132", trend: "Priority: medium", icon: FileCheck2, tone: "amber" as const },
];

// Temporary mock data for dashboard foundation only.
const recentApplications = [
  { appNo: "APP-2026-0001", name: "Ritwik Sen", artForm: "Vocal", status: "Under Verification" },
  { appNo: "APP-2026-0002", name: "Ananya Dey", artForm: "Classical Dance", status: "Approved" },
  { appNo: "APP-2026-0003", name: "Sourav Mitra", artForm: "Tabla", status: "Correction Required" },
  { appNo: "APP-2026-0004", name: "Ishita Roy", artForm: "Fine Arts", status: "Paid" },
];

const statusTone = {
  Approved: "success",
  "Under Verification": "info",
  "Correction Required": "warning",
  Paid: "neutral",
} as const;

export default function AdminDashboardPage() {
  return (
    <div className="space-y-5">
      <section className="flex items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-semibold">Admin Dashboard</h1>
          <p className="text-sm text-muted-foreground">
            Premium UI foundation with static metrics and placeholders.
          </p>
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {stats.map((item) => (
          <StatCard key={item.title} {...item} />
        ))}
      </section>

      <section className="grid gap-4 xl:grid-cols-3">
        <SectionCard
          title="Application Trend"
          description="Chart-ready section for future Recharts integration with live API data."
          action={<Sparkles size={16} className="text-muted-foreground" />}
        >
          <div className="h-64 rounded-2xl border border-dashed border-border bg-secondary/40" />
        </SectionCard>

        <SectionCard
          title="Payment Distribution"
          description="Placeholder for category-level payment analytics."
        >
          <div className="h-64 rounded-2xl border border-dashed border-border bg-secondary/40" />
        </SectionCard>

        <SectionCard
          title="Verification Load"
          description="Queue pressure snapshot for verification team planning."
        >
          <div className="h-64 rounded-2xl border border-dashed border-border bg-secondary/40" />
        </SectionCard>
      </section>

      <SectionCard title="Recent Applications" description="Temporary static records for layout foundation only.">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px] border-separate border-spacing-y-2 text-sm">
            <thead>
              <tr className="text-left text-muted-foreground">
                <th className="px-2 py-2">Application No</th>
                <th className="px-2 py-2">Student</th>
                <th className="px-2 py-2">Art Form</th>
                <th className="px-2 py-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {recentApplications.map((row) => (
                <tr key={row.appNo} className="rounded-xl bg-secondary/55">
                  <td className="rounded-l-xl px-2 py-3 font-medium">{row.appNo}</td>
                  <td className="px-2 py-3">{row.name}</td>
                  <td className="px-2 py-3">{row.artForm}</td>
                  <td className="rounded-r-xl px-2 py-3">
                    <StatusBadge label={row.status} tone={statusTone[row.status as keyof typeof statusTone]} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </SectionCard>
    </div>
  );
}
