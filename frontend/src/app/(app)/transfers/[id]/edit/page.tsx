"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { TransferForm } from "@/components/TransferForm";
import { buttonClass, ErrorBox } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import type { Transfer } from "@/lib/types";

export default function EditTransferPage() {
  const { id } = useParams<{ id: string }>();
  const [transfer, setTransfer] = useState<Transfer | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api<Transfer>(`/api/transfers/${id}`)
      .then(setTransfer)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load transfer"));
  }, [id]);

  if (error) return <ErrorBox message={error} />;
  if (!transfer) return <p className="text-sm text-slate-500">Loading…</p>;

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-3">
        <h1 className="text-xl font-bold">Edit transfer #{transfer.id}</h1>
        <Link href={`/transfers/${transfer.id}`} className={`${buttonClass.secondary} ml-auto`}>
          Cancel
        </Link>
      </div>
      <TransferForm transfer={transfer} />
    </div>
  );
}
