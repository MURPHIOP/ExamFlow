import { PageFrame } from "@/components/shared/page-frame";

export default function VerifyAdmitCardPage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="Verification"
        title="Verify an admit card"
        description="A secure admit-card verification surface ready for QR and application-number based validation."
      >
        <div className="glass-card p-5 text-sm text-muted-foreground">
          Admit card verification form placeholder.
        </div>
      </PageFrame>
    </div>
  );
}
