"use client";

import { useState } from "react";
import { AuthShell } from "@/components/shared/auth-shell";
import { authApi, setAuthToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function InstitutionRegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    institution_name: "",
    email: "",
    phone: "",
    password: "",
    confirm_password: "",
    address: "",
    district: "",
    state: "",
    pincode: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const response = await authApi.registerInstitution(form);
      const token = response.data?.data?.access_token || response.data?.access_token;
      if (token) setAuthToken(token);
      router.push("/institution");
    } catch (error: unknown) {
      if (typeof error === "object" && error !== null && "response" in error) {
        const responseError = error as { response?: { data?: { message?: string; detail?: string } } };
        setError(responseError.response?.data?.message || responseError.response?.data?.detail || "Institution registration failed.");
      } else if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Institution registration failed.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthShell title="Institution registration" description="Create an institution workspace for bulk candidate operations.">
      <form onSubmit={handleSubmit} className="space-y-4">
        {error ? <div className="rounded-2xl border border-danger/30 bg-danger/10 p-4 text-sm text-danger">{error}</div> : null}
        {(["institution_name", "email", "phone", "password", "confirm_password", "address", "district", "state", "pincode"] as const).map((field) => (
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
          {loading ? "Creating account..." : "Create institution account"}
        </button>
      </form>
    </AuthShell>
  );
}
