"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { buttonClass, inputClass } from "@/components/ui";
import { api, formatDate } from "@/lib/api";
import type { TransferListItem } from "@/lib/types";

export default function TransfersPage() {
  const router = useRouter();
  const [query, setQuery] = useState("");
  const [items, setItems] = useState<TransferListItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      api<TransferListItem[]>(`/api/transfers?q=${encodeURIComponent(query.trim())}`)
        .then((rows) => {
          setItems(rows);
          setError(null);
        })
        .catch(() => setError("Could not load transfers"));
    }, 200);
    return () => clearTimeout(timer);
  }, [query]);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-bold">Ownership transfers</h1>
        <Link href="/transfers/new" className={`${buttonClass.primary} ml-auto`}>
          + New Transfer
        </Link>
      </div>

      <input
        type="search"
        autoFocus
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter" && items?.length === 1) router.push(`/transfers/${items[0].id}`);
        }}
        placeholder="Search: registration number, NID, mobile, seller or buyer name, transfer #"
        className={`${inputClass} py-2.5 text-base`}
      />

      {error && <p className="text-sm text-red-700">{error}</p>}

      <div className="overflow-x-auto rounded-lg border border-slate-200 bg-white shadow-sm">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
            <tr>
              <th className="px-3 py-2">#</th>
              <th className="px-3 py-2">Vehicle</th>
              <th className="px-3 py-2">Seller</th>
              <th className="px-3 py-2">Buyer</th>
              <th className="px-3 py-2">Sale date</th>
              <th className="px-3 py-2" />
            </tr>
          </thead>
          <tbody>
            {items?.map((t) => (
              <tr key={t.id} className="cursor-pointer border-t border-slate-100 hover:bg-blue-50" onClick={() => router.push(`/transfers/${t.id}`)}>
                <td className="px-3 py-2 text-slate-500">{t.id}</td>
                <td className="px-3 py-2 font-semibold">{t.registration_number}</td>
                <td className="px-3 py-2">{t.seller_name}</td>
                <td className="px-3 py-2">{t.buyer_name}</td>
                <td className="px-3 py-2">{formatDate(t.sale_date)}</td>
                <td className="px-3 py-2 text-right">
                  <Link href={`/transfers/${t.id}`} className={buttonClass.link} onClick={(e) => e.stopPropagation()}>
                    Open
                  </Link>
                </td>
              </tr>
            ))}
            {items?.length === 0 && (
              <tr>
                <td colSpan={6} className="px-3 py-6 text-center text-slate-500">
                  {query ? "No transfers match your search." : "No transfers yet. Click “New Transfer” to start."}
                </td>
              </tr>
            )}
            {items === null && !error && (
              <tr>
                <td colSpan={6} className="px-3 py-6 text-center text-slate-400">
                  Loading…
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
