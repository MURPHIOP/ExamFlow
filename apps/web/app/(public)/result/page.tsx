import { PageFrame } from "@/components/shared/page-frame";

export default function PublicResultPage() {
  return (
    <div className="py-10 md:py-16">
      <PageFrame
        eyebrow="Public Result Lookup"
        title="Search results safely"
        description="This route is prepared for verified result lookup flows. It will only show live data after the backend search endpoint is confirmed."
      >
        <div className="glass-card p-5 text-sm text-muted-foreground">
          Public verification UI scaffold ready.
        </div>
      </PageFrame>
    </div>
  );
}
