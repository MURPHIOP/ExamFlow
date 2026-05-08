import Link from "next/link";

export default function HomePage() {
  return (
    <section className="grid gap-8 py-10 md:grid-cols-2 md:py-16">
      <div className="space-y-5">
        <span className="inline-flex rounded-full bg-accent px-3 py-1 text-xs font-semibold text-accent-foreground">
          Examination Automation Platform
        </span>
        <h1 className="text-4xl font-semibold tracking-tight md:text-5xl">
          Modern exam operations for cultural and skill-based boards.
        </h1>
        <p className="max-w-xl text-base text-muted-foreground md:text-lg">
          ExamFlow helps organizations digitize applications, streamline verification, and manage the
          complete examination lifecycle with speed and precision.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/register"
            className="rounded-xl bg-primary px-5 py-2.5 text-sm font-medium text-primary-foreground"
          >
            Start Application
          </Link>
          <Link href="/admin" className="rounded-xl border border-border px-5 py-2.5 text-sm font-medium">
            View Dashboard Foundation
          </Link>
        </div>
      </div>

      <div className="rounded-3xl border border-border/70 bg-card/90 p-6 shadow-soft">
        <h2 className="text-lg font-semibold">Foundation Preview</h2>
        <div className="mt-4 grid grid-cols-2 gap-3">
          {[
            "Student Applications",
            "Payment Tracking",
            "Verification Queue",
            "Admit Cards",
            "Result Publishing",
            "Certificates",
          ].map((item) => (
            <div key={item} className="rounded-2xl bg-secondary p-4 text-sm text-secondary-foreground">
              {item}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
