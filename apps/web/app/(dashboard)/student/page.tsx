import { SectionCard } from "@/components/dashboard/section-card";
import { StatCard } from "@/components/dashboard/stat-card";
import { BookOpenText, FileText, ReceiptText } from "lucide-react";

export default function StudentDashboardPage() {
  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold">Student Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Foundation view only. Live application and payment data will be integrated later.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <StatCard title="My Applications" value="2" trend="1 under verification" icon={FileText} tone="violet" />
        <StatCard title="Payments" value="1 Paid" trend="No pending dues" icon={ReceiptText} tone="emerald" />
        <StatCard title="Results" value="0 Published" trend="Awaiting exam completion" icon={BookOpenText} tone="cyan" />
      </div>

      <SectionCard title="Quick Overview" description="This page currently provides design and layout foundation.">
        <div className="h-52 rounded-2xl border border-dashed border-border bg-secondary/40" />
      </SectionCard>
    </div>
  );
}
