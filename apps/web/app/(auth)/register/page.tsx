import Link from "next/link";
import { AuthShell } from "@/components/shared/auth-shell";

export default function RegisterPage() {
  return (
    <AuthShell
      title="Create your ExamFlow account"
      description="Choose the correct registration path to continue as a student or institution."
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <Link href="/register/student" className="glow-card p-6 transition-transform hover:-translate-y-1">
          <p className="text-lg font-semibold">Student registration</p>
          <p className="mt-2 text-sm text-muted-foreground">Apply for exams, pay fees, and track documents.</p>
        </Link>
        <Link href="/register/institution" className="glow-card p-6 transition-transform hover:-translate-y-1">
          <p className="text-lg font-semibold">Institution registration</p>
          <p className="mt-2 text-sm text-muted-foreground">Submit candidates in bulk and manage applications.</p>
        </Link>
      </div>
    </AuthShell>
  );
}
