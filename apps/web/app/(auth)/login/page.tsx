"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, Lock, Mail } from "lucide-react";
import { AuthShell } from "@/components/shared/auth-shell";
import { authApi, setAuthToken } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await authApi.login(email, password);
      const result = response.data;
      const token = result?.data?.access_token || result?.access_token;
      const role = (result?.data?.user?.role || result?.user?.role || "student").toLowerCase();

      if (!token) {
        throw new Error("Login succeeded but no access token was returned.");
      }

      setAuthToken(token);
      if (role === "student") router.push("/student");
      else if (role === "institution") router.push("/institution");
      else if (role === "super_admin") router.push("/super-admin");
      else router.push("/admin");
    } catch (error: unknown) {
      if (typeof error === "object" && error !== null && "response" in error) {
        const responseError = error as {
          response?: { data?: { message?: string; detail?: string } };
          message?: string;
        };
        setError(
          responseError.response?.data?.message ||
            responseError.response?.data?.detail ||
            responseError.message ||
            "Login failed."
        );
      } else if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Login failed.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell
      title="Welcome back"
      description="Sign in to manage applications, approvals, payments, and documents from a premium secure dashboard."
    >
      <form onSubmit={handleLogin} className="space-y-4">
        {error ? (
          <div className="rounded-2xl border border-danger/30 bg-danger/10 p-4 text-sm text-danger">
            {error}
          </div>
        ) : null}

        <label className="block space-y-2">
          <span className="text-sm font-medium">Email</span>
          <div className="flex items-center gap-3 rounded-2xl border border-border bg-background/60 px-4 py-3">
            <Mail className="h-4 w-4 text-muted-foreground" />
            <input
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              className="w-full border-0 bg-transparent p-0 outline-none ring-0"
              placeholder="name@example.com"
              required
            />
          </div>
        </label>

        <label className="block space-y-2">
          <span className="text-sm font-medium">Password</span>
          <div className="flex items-center gap-3 rounded-2xl border border-border bg-background/60 px-4 py-3">
            <Lock className="h-4 w-4 text-muted-foreground" />
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              className="w-full border-0 bg-transparent p-0 outline-none ring-0"
              placeholder="••••••••"
              required
            />
            <button type="button" onClick={() => setShowPassword((current) => !current)} className="text-muted-foreground">
              {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            </button>
          </div>
        </label>

        <button type="submit" className="premium-button w-full" disabled={loading}>
          {loading ? "Signing in..." : "Continue to dashboard"}
        </button>
      </form>
    </AuthShell>
  );
}