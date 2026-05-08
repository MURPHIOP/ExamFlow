type ErrorStateProps = {
  title: string;
  description: string;
};

export function ErrorState({ title, description }: ErrorStateProps) {
  return (
    <div className="rounded-2xl border border-rose-500/30 bg-rose-500/10 p-6">
      <h3 className="text-lg font-semibold text-rose-700 dark:text-rose-300">{title}</h3>
      <p className="mt-1 text-sm text-rose-700/80 dark:text-rose-300/90">{description}</p>
    </div>
  );
}
