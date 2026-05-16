import { PageFrame } from "@/components/shared/page-frame";

export default function StudentCertificatesPage() {
  return (
    <PageFrame
      eyebrow="Certificates"
      title="Download certificates"
      description="Certificates will be available once issued by the backend certificate workflow."
    >
      <div className="glass-card p-5 text-sm text-muted-foreground">Certificate list placeholder.</div>
    </PageFrame>
  );
}
