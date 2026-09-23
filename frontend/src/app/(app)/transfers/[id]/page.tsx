"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useRef, useState, type ReactNode } from "react";

import { buttonClass, ErrorBox, Section } from "@/components/ui";
import { api, ApiError, formatDate, formatTaka } from "@/lib/api";
import type { DocumentInfo, Person, Transfer } from "@/lib/types";

function Row({ label, value }: { label: string; value: ReactNode }) {
  return (
    <div className="grid grid-cols-3 gap-2 py-0.5 text-sm">
      <dt className="text-slate-500">{label}</dt>
      <dd className="col-span-2 font-medium uppercase">{value || <span className="normal-case text-slate-400">—</span>}</dd>
    </div>
  );
}

function PersonSummary({ title, p }: { title: string; p: Person }) {
  const fatherOrHusband = p.father_or_husband_pref === "husband" ? p.spouse_name : p.father_name;
  return (
    <Section title={title}>
      <dl>
        <Row label="Name" value={p.name} />
        <Row label="NID" value={p.nid} />
        <Row label="TIN" value={p.tin} />
        <Row label="Mobile" value={p.phone} />
        <Row label={`পিতা/স্বামী (${p.father_or_husband_pref})`} value={fatherOrHusband} />
        <Row label="Mother" value={p.mother_name} />
        <Row label="Present address" value={p.present_address} />
        <Row label="Permanent address" value={p.permanent_address} />
      </dl>
    </Section>
  );
}

export default function ReviewPage() {
  const { id } = useParams<{ id: string }>();
  const [transfer, setTransfer] = useState<Transfer | null>(null);
  const [docs, setDocs] = useState<DocumentInfo[] | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [printing, setPrinting] = useState(false);
  const printFrame = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    api<Transfer>(`/api/transfers/${id}`)
      .then(setTransfer)
      .catch((e) => setError(e instanceof ApiError ? e.message : "Could not load transfer"));
    api<DocumentInfo[]>(`/api/transfers/${id}/documents`)
      .then((d) => {
        setDocs(d);
        setSelected(d.find((x) => !x.error)?.slug ?? null);
      })
      .catch(() => setError("Could not prepare the documents"));
  }, [id]);

  const base = `/api/transfers/${id}/documents`;
  const hasErrors = docs?.some((d) => d.error);

  // Load the combined PDF in a hidden frame and open the print dialog once for all forms.
  function printAll() {
    const frame = printFrame.current;
    if (!frame) return;
    setPrinting(true);
    frame.onload = () => {
      setPrinting(false);
      try {
        frame.contentWindow?.focus();
        frame.contentWindow?.print();
      } catch {
        window.open(`${base}/all.pdf`, "_blank"); // browser blocked frame printing: print from the tab
      }
    };
    frame.src = `${base}/all.pdf?t=${Date.now()}`;
  }

  if (error) return <ErrorBox message={error} />;
  if (!transfer) return <p className="text-sm text-slate-500">Loading…</p>;

  const v = transfer.vehicle;
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-3">
        <h1 className="text-xl font-bold">Ownership transfer #{transfer.id}</h1>
        <span className="text-xs text-slate-500">
          Created {new Date(transfer.created_at).toLocaleString()} by {transfer.created_by ?? "—"}
          {transfer.updated_at !== transfer.created_at && ` · Last edited by ${transfer.updated_by ?? "—"}`}
        </span>
        <Link href={`/transfers/${transfer.id}/edit`} className={`${buttonClass.secondary} ml-auto`}>
          Edit
        </Link>
      </div>

      <Section
        title="Documents"
        action={
          <div className="flex flex-wrap gap-2">
            <button type="button" onClick={printAll} disabled={!!hasErrors || printing} className={buttonClass.primary}>
              {printing ? "Preparing…" : "Print All"}
            </button>
            <a href={`${base}/all.zip`} className={`${buttonClass.secondary} ${hasErrors ? "pointer-events-none opacity-50" : ""}`}>
              Download All (ZIP)
            </a>
            <a href={`${base}/all.pdf?download=1`} className={`${buttonClass.secondary} ${hasErrors ? "pointer-events-none opacity-50" : ""}`}>
              Download All (one PDF)
            </a>
          </div>
        }
      >
        {docs === null ? (
          <p className="text-sm text-slate-500">Generating forms…</p>
        ) : (
          <div className="grid gap-4 lg:grid-cols-[18rem_1fr]">
            <ul className="space-y-2">
              {docs.map((d) => (
                <li
                  key={d.slug}
                  className={`rounded-md border p-2.5 ${selected === d.slug ? "border-blue-600 bg-blue-50" : "border-slate-200"} ${d.error ? "border-red-300 bg-red-50" : ""}`}
                >
                  <div className="text-sm font-semibold">{d.title}</div>
                  {d.error ? (
                    <p className="mt-1 text-xs text-red-800">
                      {d.error}{" "}
                      <Link href={`/transfers/${transfer.id}/edit`} className={buttonClass.link}>
                        Edit
                      </Link>
                    </p>
                  ) : (
                    <div className="mt-1.5 flex gap-2">
                      <button type="button" onClick={() => setSelected(d.slug)} className={buttonClass.secondary}>
                        Preview
                      </button>
                      <a href={`${base}/${d.slug}?download=1`} className={buttonClass.secondary}>
                        Download
                      </a>
                      <a href={`${base}/${d.slug}`} target="_blank" rel="noreferrer" className={buttonClass.link + " self-center"}>
                        Open
                      </a>
                    </div>
                  )}
                </li>
              ))}
            </ul>
            {selected ? (
              <iframe key={selected} title="Form preview" src={`${base}/${selected}`} className="h-[80vh] w-full rounded-md border border-slate-300 bg-white" />
            ) : (
              <p className="text-sm text-slate-500">Fix the errors to preview the forms.</p>
            )}
          </div>
        )}
        <iframe ref={printFrame} title="Print all" className="hidden" />
      </Section>

      <div className="grid gap-4 md:grid-cols-2">
        <PersonSummary title="Seller" p={transfer.seller} />
        <PersonSummary title="Buyer" p={transfer.buyer} />
        <Section title="Vehicle">
          <dl>
            <Row label="Registration" value={v.registration_number} />
            <Row label="Type" value={v.vehicle_type} />
            <Row label="Chassis" value={v.chassis_number} />
            <Row label="Engine" value={v.engine_number} />
            <Row label="Manufacturer" value={v.manufacturer} />
            <Row label="Year" value={v.manufacturing_year} />
            <Row label="Previous reg." value={v.previous_registration_number} />
          </dl>
        </Section>
        <Section title="Sale">
          <dl>
            <Row label="Sale price" value={transfer.sale_price ? `${formatTaka(transfer.sale_price)} (${transfer.sale_price_words ?? ""})` : null} />
            <Row label="Sale date" value={formatDate(transfer.sale_date)} />
            <Row label="Reg. authority" value={transfer.registration_authority} />
            <Row label="Fee bank" value={transfer.fee_bank_name} />
            <Row label="Witnesses" value={transfer.witnesses.map((w) => w.name).join(", ")} />
            {transfer.notes && <Row label="Notes" value={transfer.notes} />}
          </dl>
        </Section>
      </div>
    </div>
  );
}
