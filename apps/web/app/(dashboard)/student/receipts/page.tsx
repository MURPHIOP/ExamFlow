import { PageFrame } from "@/components/shared/page-frame";

export default function StudentReceiptsPage() {
  return (
    <PageFrame
      eyebrow="Receipts"
      title="Download payment receipts"
      description="Receipt downloads will bind to backend PDF generation when that endpoint is connected."
    >
      <div className="glass-card p-5 text-sm text-muted-foreground">Receipt list placeholder.</div>
    </PageFrame>
  );
}
