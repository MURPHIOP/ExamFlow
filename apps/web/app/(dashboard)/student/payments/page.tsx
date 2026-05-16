import { PageFrame } from "@/components/shared/page-frame";

export default function StudentPaymentsPage() {
  return (
    <PageFrame
      eyebrow="Payments"
      title="Track payment status"
      description="Razorpay checkout will connect here only after the backend payment workflow is verified."
    >
      <div className="glass-card p-5 text-sm text-muted-foreground">Payment timeline placeholder.</div>
    </PageFrame>
  );
}
