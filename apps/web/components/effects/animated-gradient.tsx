"use client";

export function AnimatedGradient() {
  return (
    <div className="absolute inset-0 -z-10">
      <div className="animated-gradient-bg absolute h-96 w-96 rounded-full blur-3xl opacity-20" />
      <div className="animated-gradient-bg absolute -bottom-40 -right-40 h-96 w-96 rounded-full blur-3xl opacity-20" />
    </div>
  );
}

export function GradientText({ children }: { children: React.ReactNode }) {
  return (
    <span className="neon-text font-bold bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent">
      {children}
    </span>
  );
}
