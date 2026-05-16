import { PageFrame } from "@/components/shared/page-frame";

export default function AboutPage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="About ExamFlow"
        title="Built for serious examination boards"
        description="ExamFlow is designed to digitize admissions, payments, admit cards, results, certificates, and verification flows for cultural, academic, and skill-based boards."
      >
        <div className="grid gap-4 md:grid-cols-3">
          {[
            "Secure application workflows",
            "Role-based admin operations",
            "Receipt, admit card, and certificate readiness",
          ].map((item) => (
            <div key={item} className="glass-card p-5 text-sm text-muted-foreground">
              {item}
            </div>
          ))}
        </div>
      </PageFrame>
    </div>
  );
}
