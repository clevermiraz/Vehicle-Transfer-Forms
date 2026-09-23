"use client";

import { useEffect, useState, type FormEvent } from "react";

import { useUser } from "@/components/AppShell";
import { buttonClass, ErrorBox, Section, TextInput } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import type { User } from "@/lib/types";

export default function UsersPage() {
  const me = useUser();
  const [users, setUsers] = useState<User[]>([]);
  const [form, setForm] = useState({ name: "", username: "", password: "", is_admin: false });
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const load = () => api<User[]>("/api/users").then(setUsers).catch((e) => setError(e.message));
  useEffect(() => {
    load();
  }, []);

  async function run(action: () => Promise<unknown>, success: string) {
    setError(null);
    setNotice(null);
    try {
      await action();
      setNotice(success);
      await load();
    } catch (e) {
      setError(e instanceof ApiError ? Object.values(e.fields)[0] ?? e.message : "Request failed");
    }
  }

  function create(e: FormEvent) {
    e.preventDefault();
    run(async () => {
      await api("/api/users", { method: "POST", body: form });
      setForm({ name: "", username: "", password: "", is_admin: false });
    }, "User created");
  }

  function resetPassword(u: User) {
    const password = window.prompt(`New password for ${u.name} (min 8 characters):`);
    if (password) run(() => api(`/api/users/${u.id}`, { method: "PATCH", body: { password } }), "Password changed");
  }

  if (!me?.is_admin) return <ErrorBox message="Admin only" />;

  return (
    <div className="space-y-4">
      <h1 className="text-xl font-bold">Users</h1>
      <ErrorBox message={error} />
      {notice && <p className="text-sm text-green-700">{notice}</p>}
      <Section title="Staff accounts">
        <table className="w-full text-sm">
          <thead className="text-left text-xs uppercase text-slate-500">
            <tr>
              <th className="py-1">Name</th>
              <th>Username</th>
              <th>Role</th>
              <th>Status</th>
              <th />
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id} className="border-t border-slate-100">
                <td className="py-2">{u.name}</td>
                <td>{u.username}</td>
                <td>{u.is_admin ? "Admin" : "Staff"}</td>
                <td className={u.is_active ? "text-green-700" : "text-slate-400"}>{u.is_active ? "Active" : "Disabled"}</td>
                <td className="space-x-3 text-right">
                  <button className={buttonClass.link} onClick={() => resetPassword(u)}>
                    Reset password
                  </button>
                  {u.id !== me.id && (
                    <button
                      className={buttonClass.link}
                      onClick={() => run(() => api(`/api/users/${u.id}`, { method: "PATCH", body: { is_active: !u.is_active } }), "Saved")}
                    >
                      {u.is_active ? "Disable" : "Enable"}
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Section>
      <Section title="Add user">
        <form onSubmit={create} className="grid gap-3 md:grid-cols-4">
          <TextInput label="Full name" value={form.name} onChange={(name) => setForm({ ...form, name })} required />
          <TextInput label="Username" value={form.username} onChange={(username) => setForm({ ...form, username })} hint="lowercase letters, digits, . _ -" required />
          <TextInput label="Password" type="password" value={form.password} onChange={(password) => setForm({ ...form, password })} hint="min 8 characters" required />
          <div className="flex items-end gap-3">
            <label className="flex items-center gap-1.5 pb-2 text-sm">
              <input type="checkbox" checked={form.is_admin} onChange={(e) => setForm({ ...form, is_admin: e.target.checked })} />
              Admin
            </label>
            <button type="submit" className={buttonClass.primary}>
              Add
            </button>
          </div>
        </form>
      </Section>
    </div>
  );
}
