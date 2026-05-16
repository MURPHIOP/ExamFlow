import { PageFrame } from "@/components/shared/page-frame";

export default function VerifyCertificatePage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="Verification"
        title="Verify a certificate"
        description="Enter a QR code or certificate number to verify authenticity. Backend verification can be connected without changing this page layout."
      >
        <div className="glass-card p-5 text-sm text-muted-foreground">
          Certificate verification form placeholder.
        </div>
      </PageFrame>
    </div>
  );
}
