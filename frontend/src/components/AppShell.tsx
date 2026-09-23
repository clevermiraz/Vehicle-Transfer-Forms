"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import { api } from "@/lib/api";
import type { User } from "@/lib/types";

const UserContext = createContext<User | null>(null);

export function useUser(): User | null {
  return useContext(UserContext);
}

export function AppShell({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    api<User>("/api/auth/me").then(setUser).catch(() => undefined); // 401 redirects to /login
  }, []);

  // Alt+N anywhere: start a new transfer.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.altKey && e.key.toLowerCase() === "n") {
        e.preventDefault();
        router.push("/transfers/new");
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [router]);

  async function logout() {
    await api("/api/auth/logout", { method: "POST" });
    router.replace("/login");
  }

  if (!user) {
    return <div className="p-8 text-sm text-slate-500">Loading…</div>;
  }

  const navLink = (href: string, label: string) => (
    <Link
      href={href}
      className={`rounded-md px-3 py-1.5 text-sm font-medium ${
        pathname === href ? "bg-white/15 text-white" : "text-blue-100 hover:bg-white/10 hover:text-white"
      }`}
    >
      {label}
    </Link>
  );

  return (
    <UserContext.Provider value={user}>
      <header className="bg-blue-900 print:hidden">
        <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-2 px-4 py-2">
          <Link href="/" className="mr-4 text-base font-bold text-white">
            Vehicle Transfer Forms
          </Link>
          {navLink("/", "Transfers")}
          {navLink("/transfers/new", "New Transfer (Alt+N)")}
          {user.is_admin && navLink("/users", "Users")}
          <div className="ml-auto flex items-center gap-3 text-sm text-blue-100">
            <Link href="/account" className="hover:text-white">
              {user.name}
            </Link>
            <button onClick={logout} className="rounded-md px-2 py-1 hover:bg-white/10 hover:text-white">
              Log out
            </button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-5">{children}</main>
    </UserContext.Provider>
  );
}
