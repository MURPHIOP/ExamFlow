import { PageFrame } from "@/components/shared/page-frame";

export default function StudentApplicationsPage() {
  return (
    <PageFrame
      eyebrow="Student Applications"
      title="All your submitted applications"
      description="This page is ready for live application data once the backend list endpoint is confirmed."
    >
      <div className="glass-card p-5 text-sm text-muted-foreground">Application table placeholder.</div>
    </PageFrame>
  );
}
