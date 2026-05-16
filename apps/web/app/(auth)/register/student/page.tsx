"use client";

import { useState } from "react";
import { AuthShell } from "@/components/shared/auth-shell";
import { authApi, setAuthToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function StudentRegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    phone: "",
    password: "",
    confirm_password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await authApi.registerStudent(form);
      const token = response.data?.data?.access_token || response.data?.access_token;
      if (token) setAuthToken(token);
      router.push("/student");
    } catch (error: unknown) {
      if (typeof error === "object" && error !== null && "response" in error) {
        const responseError = error as { response?: { data?: { message?: string; detail?: string } } };
        setError(responseError.response?.data?.message || responseError.response?.data?.detail || "Student registration failed.");
      } else if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Student registration failed.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell title="Student registration" description="Create your student profile and start the online application flow.">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error ? <div className="rounded-2xl border border-danger/30 bg-danger/10 p-4 text-sm text-danger">{error}</div> : null}
        {(["full_name", "email", "phone", "password", "confirm_password"] as const).map((field) => (
          <label key={field} className="block space-y-2">
            <span className="text-sm font-medium">{field.replaceAll("_", " ")}</span>
            <input
              type={field.includes("password") ? "password" : field === "email" ? "email" : "text"}
              value={form[field]}
              onChange={(e) => setForm((curr) => ({ ...curr, [field]: e.target.value }))}
              className="w-full rounded-2xl border border-border bg-background/60 px-4 py-3"
              required
            />
          </label>
        ))}
        <button type="submit" disabled={loading} className="premium-button w-full">
          {loading ? "Creating account..." : "Create student account"}
        </button>
      </form>
    </AuthShell>
  );
}
