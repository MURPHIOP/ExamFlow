import { PageFrame } from "@/components/shared/page-frame";

export default function StudentResultsPage() {
  return (
    <PageFrame
      eyebrow="Results"
      title="Your published results"
      description="Result data will be fetched from the backend when the results module is available."
    >
      <div className="glass-card p-5 text-sm text-muted-foreground">Results placeholder.</div>
    </PageFrame>
  );
}
