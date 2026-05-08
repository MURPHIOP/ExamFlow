import { SectionCard } from "@/components/section-card";
import { StatCard } from "@/components/stat-card";
import { Building2, FileSpreadsheet, ReceiptText } from "lucide-react";

export default function InstitutionDashboardPage() {
  return (
    <div className="space-y-5">
      <div>
        <h1 className="text-2xl font-semibold">Institution Dashboard</h1>
        <p className="text-sm text-muted-foreground">
          Foundation view only. Bulk upload and bulk payment flows are not implemented in this step.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <StatCard title="Registered Students" value="56" trend="+4 this session" icon={Building2} tone="violet" />
        <StatCard title="Submitted Forms" value="41" trend="15 drafts pending" icon={FileSpreadsheet} tone="cyan" />
        <StatCard title="Bulk Payments" value="29 Paid" trend="3 pending batches" icon={ReceiptText} tone="amber" />
      </div>

      <SectionCard title="Institution Activity" description="Placeholder section for institution-level reports.">
        <div className="h-52 rounded-2xl border border-dashed border-border bg-secondary/40" />
      </SectionCard>
    </div>
  );
}
