import { PageFrame } from "@/components/shared/page-frame";

export default function NewStudentApplicationPage() {
  return (
    <PageFrame
      eyebrow="New Application"
      title="Start a fresh exam application"
      description="The wizard UI is ready for session, subject, grade, centre selection, and fee preview once those APIs are connected."
    >
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="glass-card p-5">Stepper wizard placeholder.</div>
        <div className="glass-card p-5">Fee preview and declaration placeholder.</div>
      </div>
    </PageFrame>
  );
}
