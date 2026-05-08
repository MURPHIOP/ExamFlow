"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { apiClient } from "@/lib/api-client";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await apiClient.post("/auth/login", { 
        identifier: email, 
        password 
      });

      const result = response.data;

      if (result.success && result.data?.access_token) {
        // Save the real JWT token
        localStorage.setItem("token", result.data.access_token);
        
        // Redirect based on role
        const role = result.data.user?.role;
        if (role === "STUDENT") router.push("/student");
        else if (role === "ADMIN" || role === "SUPER_ADMIN") router.push("/admin");
        else router.push("/dashboard");
      }
    } catch (err: any) {
      setError(err.response?.data?.message || err.response?.data?.detail || "Login failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen items-center justify-center px-4 bg-background">
      <section className="w-full max-w-md rounded-3xl border border-border/70 bg-card p-6 shadow-soft">
        <h1 className="text-2xl font-semibold">Login</h1>
        <p className="mt-1 text-sm text-muted-foreground">Sign in to your ExamFlow account.</p>
        
        {/* Error Banner */}
        {error && (
          <div className="mt-4 p-3 text-sm text-red-600 bg-red-50/50 border border-red-100 rounded-xl">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="mt-6 space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full rounded-xl border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="name@example.com"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full rounded-xl border border-input bg-background px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/50"
              placeholder="********"
            />
          </div>
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-primary px-4 py-2.5 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            {loading ? "Authenticating..." : "Continue"}
          </button>
        </form>
      </section>
    </main>
  );
}