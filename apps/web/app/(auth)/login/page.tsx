export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <section className="w-full max-w-md rounded-3xl border border-border/70 bg-card p-6 shadow-soft">
        <h1 className="text-2xl font-semibold">Login</h1>
        <p className="mt-1 text-sm text-muted-foreground">Foundation page only. Auth logic is not implemented yet.</p>
        <form className="mt-6 space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium">Email</label>
            <input
              type="email"
              className="w-full rounded-xl border border-input bg-background px-3 py-2 text-sm"
              placeholder="name@example.com"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Password</label>
            <input
              type="password"
              className="w-full rounded-xl border border-input bg-background px-3 py-2 text-sm"
              placeholder="********"
            />
          </div>
          <button
            type="button"
            className="w-full rounded-xl bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground"
          >
            Continue
          </button>
        </form>
      </section>
    </main>
  );
}
