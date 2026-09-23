"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useState, type FormEvent } from "react";

import { buttonClass, ErrorBox, TextInput } from "@/components/ui";
import { api, ApiError } from "@/lib/api";

function LoginForm() {
  const router = useRouter();
  const next = useSearchParams().get("next");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      await api("/api/auth/login", { method: "POST", body: { username, password } });
      // Only allow internal redirects.
      router.replace(next?.startsWith("/") && !next.startsWith("//") ? next : "/");
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Cannot reach the server");
      setBusy(false);
    }
  }

  return (
    <form onSubmit={submit} className="w-full max-w-sm space-y-4 rounded-lg bg-white p-6 shadow">
      <h1 className="text-lg font-bold">Vehicle Transfer Forms</h1>
      <TextInput label="Username" value={username} onChange={setUsername} autoFocus autoComplete="username" required />
      <TextInput label="Password" type="password" value={password} onChange={setPassword} autoComplete="current-password" required />
      <ErrorBox message={error} />
      <button type="submit" disabled={busy || !username || !password} className={`${buttonClass.primary} w-full justify-center`}>
        {busy ? "Logging in…" : "Log in"}
      </button>
    </form>
  );
}

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center p-4">
      <Suspense>
        <LoginForm />
      </Suspense>
    </main>
  );
}
