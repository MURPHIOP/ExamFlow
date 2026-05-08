export function LoadingSkeleton() {
  return (
    <div className="space-y-3 rounded-2xl border border-border/70 bg-card p-5 shadow-soft">
      <div className="h-5 w-40 animate-pulse rounded-md bg-muted" />
      <div className="h-12 w-full animate-pulse rounded-xl bg-muted" />
      <div className="h-12 w-full animate-pulse rounded-xl bg-muted" />
      <div className="h-12 w-2/3 animate-pulse rounded-xl bg-muted" />
    </div>
  );
}
