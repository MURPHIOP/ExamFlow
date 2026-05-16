import { PageFrame } from "@/components/shared/page-frame";

export default function ExamSessionsPage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="Exam Sessions"
        title="View active exam sessions"
        description="This page is ready to connect to the backend exam session list. It currently shows a premium empty-state layout until live data is wired."
      >
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {[
            "Summer 2026",
            "Annual 2026",
            "Special Session",
          ].map((session) => (
            <div key={session} className="glass-card p-5">
              <p className="font-semibold">{session}</p>
              <p className="mt-2 text-sm text-muted-foreground">Backend data hook pending.</p>
            </div>
          ))}
        </div>
      </PageFrame>
    </div>
  );
}
