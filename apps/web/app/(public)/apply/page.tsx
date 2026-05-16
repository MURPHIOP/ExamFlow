import Link from "next/link";
import { PageFrame } from "@/components/shared/page-frame";

export default function ApplyPage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="Application Entry"
        title="Start your application"
        description="Applicants can begin here and move into the authenticated flow once the backend application creation endpoint is connected."
        actions={
          <Link className="premium-button text-sm" href="/register/student">
            Register to apply
          </Link>
        }
      >
        <div className="grid gap-4 lg:grid-cols-2">
          <div className="glass-card p-5">
            <p className="text-sm font-semibold text-primary">What is supported</p>
            <p className="mt-2 text-sm text-muted-foreground">
              Student onboarding, institution onboarding, and role-based dashboard routing are ready.
            </p>
          </div>
          <div className="glass-card p-5">
            <p className="text-sm font-semibold text-primary">What is next</p>
            <p className="mt-2 text-sm text-muted-foreground">
              Live application creation will connect to backend APIs only after those routes are verified.
            </p>
          </div>
        </div>
      </PageFrame>
    </div>
  );
}
