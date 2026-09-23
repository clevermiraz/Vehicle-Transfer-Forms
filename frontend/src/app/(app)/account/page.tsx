"use client";

import { useState, type FormEvent } from "react";

import { buttonClass, ErrorBox, Section, TextInput } from "@/components/ui";
import { api, ApiError } from "@/lib/api";

export default function AccountPage() {
  const [current, setCurrent] = useState("");
  const [next, setNext] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [done, setDone] = useState(false);

  async function submit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setDone(false);
    try {
      await api("/api/auth/change-password", { method: "POST", body: { current_password: current, new_password: next } });
      setDone(true);
      setCurrent("");
      setNext("");
    } catch (err) {
      setError(err instanceof ApiError ? Object.values(err.fields)[0] ?? err.message : "Request failed");
    }
  }

  return (
    <div className="max-w-md">
      <Section title="Change my password">
        <form onSubmit={submit} className="space-y-3">
          <TextInput label="Current password" type="password" value={current} onChange={setCurrent} autoComplete="current-password" required />
          <TextInput label="New password" type="password" value={next} onChange={setNext} hint="min 8 characters" autoComplete="new-password" required />
          <ErrorBox message={error} />
          {done && <p className="text-sm text-green-700">Password changed.</p>}
          <button type="submit" className={buttonClass.primary}>
            Change password
          </button>
        </form>
      </Section>
    </div>
  );
}
