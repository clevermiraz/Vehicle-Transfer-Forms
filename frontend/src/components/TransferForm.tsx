"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react";

import { api, ApiError, formatTaka } from "@/lib/api";
import type { FatherOrHusband, Person, Transfer, Vehicle } from "@/lib/types";
import { SearchBox } from "./SearchBox";
import { buttonClass, ErrorBox, Field, inputClass, Section, TextArea, TextInput } from "./ui";

// ---------- form state (everything is a string while typing) ----------

const PERSON_KEYS = [
  "name", "father_name", "mother_name", "spouse_name", "guardian_name", "gender", "date_of_birth",
  "nationality", "nid", "tin", "phone", "present_address", "permanent_address",
] as const;
type PersonForm = { id: number | null; father_or_husband_pref: FatherOrHusband } & Record<(typeof PERSON_KEYS)[number], string>;

const VEHICLE_KEYS = [
  "registration_number", "vehicle_type", "chassis_number", "engine_number", "manufacturer",
  "manufacturing_year", "previous_registration_number",
] as const;
type VehicleForm = { id: number | null } & Record<(typeof VEHICLE_KEYS)[number], string>;

interface WitnessForm {
  name: string;
  address: string;
  phone: string;
}

interface SaleForm {
  registration_authority: string;
  sale_price: string;
  sale_price_words: string;
  sale_date: string;
  fee_bank_name: string;
  notes: string;
}

interface FormState {
  seller: PersonForm;
  buyer: PersonForm;
  vehicle: VehicleForm;
  sale: SaleForm;
  witnesses: WitnessForm[];
}

const str = (v: string | number | null | undefined) => (v == null ? "" : String(v));
const orNull = (v: string) => (v.trim() === "" ? null : v.trim());

function toPersonForm(p: Partial<Person> | null, defaults: Partial<PersonForm> = {}): PersonForm {
  const form = { id: p?.id ?? null, father_or_husband_pref: p?.father_or_husband_pref ?? "father" } as PersonForm;
  for (const key of PERSON_KEYS) form[key] = str(p?.[key]);
  return { ...form, ...(p ? {} : defaults) };
}

function toVehicleForm(v: Partial<Vehicle> | null): VehicleForm {
  const form = { id: v?.id ?? null } as VehicleForm;
  for (const key of VEHICLE_KEYS) form[key] = str(v?.[key]);
  return form;
}

function personPayload(f: PersonForm) {
  const out: Record<string, unknown> = { id: f.id, father_or_husband_pref: f.father_or_husband_pref };
  for (const key of PERSON_KEYS) out[key] = orNull(f[key]);
  return out;
}

function vehiclePayload(f: VehicleForm) {
  const out: Record<string, unknown> = { id: f.id };
  for (const key of VEHICLE_KEYS) out[key] = orNull(f[key]);
  out.manufacturing_year = f.manufacturing_year.trim() ? Number(f.manufacturing_year) : null;
  return out;
}

function today(): string {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

const NEW_BUYER_DEFAULTS: Partial<PersonForm> = { nationality: "BANGLADESHI" };

function initialState(t: Transfer | null): FormState {
  const witnesses: WitnessForm[] = [0, 1, 2].map((i) => {
    const w = t?.witnesses[i];
    return { name: str(w?.name), address: str(w?.address), phone: str(w?.phone) };
  });
  return {
    seller: toPersonForm(t?.seller ?? null),
    buyer: toPersonForm(t?.buyer ?? null, NEW_BUYER_DEFAULTS),
    vehicle: toVehicleForm(t?.vehicle ?? null),
    sale: {
      registration_authority: str(t?.registration_authority),
      sale_price: str(t?.sale_price),
      sale_price_words: str(t?.sale_price_words),
      sale_date: t?.sale_date ?? today(),
      fee_bank_name: str(t?.fee_bank_name),
      notes: str(t?.notes),
    },
    witnesses,
  };
}

// ---------- sections ----------

type Errors = Record<string, string>;

function PersonSection({
  role, title, value, onChange, errors, full,
}: {
  role: "seller" | "buyer";
  title: string;
  value: PersonForm;
  onChange: (v: PersonForm) => void;
  errors: Errors;
  full: boolean; // buyer: fields needed by Owner's Particulars
}) {
  const set = (key: keyof PersonForm) => (v: string) => onChange({ ...value, [key]: v });
  const err = (key: string) => errors[`${role}.${key}`];

  return (
    <Section
      title={title}
      action={
        <div className="w-full sm:w-96">
          <SearchBox<Person>
            endpoint="/api/people/search"
            placeholder={`Search saved ${role}: name, NID or mobile`}
            autoFocus={role === "seller"}
            onSelect={(p) => onChange(toPersonForm(p))}
            renderItem={(p) => (
              <div>
                <div className="font-semibold">{p.name}</div>
                <div className="text-xs text-slate-500">
                  {[p.nid && `NID ${p.nid}`, p.phone, p.father_name && `Father: ${p.father_name}`].filter(Boolean).join(" · ")}
                </div>
              </div>
            )}
          />
        </div>
      }
    >
      {value.id && (
        <div className="mb-3 flex items-center justify-between rounded-md bg-green-50 px-3 py-1.5 text-xs text-green-800">
          <span>Saved customer loaded. Your changes will also update their saved record.</span>
          <button type="button" className={buttonClass.link} onClick={() => onChange(toPersonForm(null, role === "buyer" ? NEW_BUYER_DEFAULTS : {}))}>
            Clear &amp; enter a different person
          </button>
        </div>
      )}
      <div className="grid grid-cols-1 gap-3 md:grid-cols-6">
        <TextInput label="Name" required caps value={value.name} onChange={set("name")} error={err("name")} wrapperClass="md:col-span-3" />
        <TextInput label="NID" inputMode="numeric" value={value.nid} onChange={set("nid")} error={err("nid")} hint="10, 13 or 17 digits" wrapperClass="md:col-span-2" />
        <TextInput label="TIN" inputMode="numeric" value={value.tin} onChange={set("tin")} error={err("tin")} wrapperClass="md:col-span-1" />
        <TextInput label="Father's name" caps value={value.father_name} onChange={set("father_name")} error={err("father_name")} wrapperClass="md:col-span-2" />
        <TextInput label="Mother's name" caps value={value.mother_name} onChange={set("mother_name")} error={err("mother_name")} wrapperClass="md:col-span-2" />
        <TextInput label="Husband / Wife name" caps value={value.spouse_name} onChange={set("spouse_name")} error={err("spouse_name")} wrapperClass="md:col-span-2" />
        <div className="md:col-span-2" role="radiogroup" aria-label="Print on পিতা/স্বামী line">
          <span className="mb-1 block text-xs font-semibold text-slate-600">Print on &lsquo;পিতা/স্বামী&rsquo; line</span>
          <div className="flex gap-4 py-1.5 text-sm">
            {(["father", "husband"] as const).map((opt) => (
              <label key={opt} className="flex items-center gap-1.5">
                <input
                  type="radio"
                  name={`${role}-pref`}
                  checked={value.father_or_husband_pref === opt}
                  onChange={() => onChange({ ...value, father_or_husband_pref: opt })}
                />
                {opt === "father" ? "Father" : "Husband"}
              </label>
            ))}
          </div>
        </div>
        <TextInput label="Mobile" inputMode="tel" value={value.phone} onChange={set("phone")} error={err("phone")} placeholder="01XXXXXXXXX" wrapperClass="md:col-span-2" />
        {full && (
          <>
            <Field label="Sex" error={err("gender")} className="md:col-span-1">
              <select value={value.gender} onChange={(e) => set("gender")(e.target.value)} className={inputClass}>
                <option value="">—</option>
                <option value="MALE">Male</option>
                <option value="FEMALE">Female</option>
                <option value="OTHER">Other</option>
              </select>
            </Field>
            <TextInput label="Date of birth" type="date" value={value.date_of_birth} onChange={set("date_of_birth")} error={err("date_of_birth")} wrapperClass="md:col-span-1" />
          </>
        )}
        <TextArea label="Present address (printed on Forms 20, 21, 22)" value={value.present_address} onChange={set("present_address")} error={err("present_address")} wrapperClass="md:col-span-3" />
        <div className="md:col-span-3">
          <TextArea label="Permanent address" value={value.permanent_address} onChange={set("permanent_address")} error={err("permanent_address")} />
          <button type="button" className={`${buttonClass.link} mt-1 text-xs`} onClick={() => set("permanent_address")(value.present_address)}>
            Same as present address
          </button>
        </div>
        {full && (
          <>
            <TextInput label="Nationality" caps value={value.nationality} onChange={set("nationality")} error={err("nationality")} wrapperClass="md:col-span-2" />
            <TextInput label="Guardian's name (only if minor)" caps value={value.guardian_name} onChange={set("guardian_name")} error={err("guardian_name")} wrapperClass="md:col-span-4" />
          </>
        )}
      </div>
    </Section>
  );
}

function VehicleSection({ value, onChange, errors }: { value: VehicleForm; onChange: (v: VehicleForm) => void; errors: Errors }) {
  const set = (key: keyof VehicleForm) => (v: string) => onChange({ ...value, [key]: v });
  const err = (key: string) => errors[`vehicle.${key}`];
  return (
    <Section
      title="Vehicle"
      action={
        <div className="w-full sm:w-96">
          <SearchBox<Vehicle>
            endpoint="/api/vehicles/search"
            placeholder="Search saved vehicle: registration, chassis, engine"
            onSelect={(v) => onChange(toVehicleForm(v))}
            renderItem={(v) => (
              <div>
                <div className="font-semibold">{v.registration_number}</div>
                <div className="text-xs text-slate-500">
                  {[v.manufacturer, v.vehicle_type, v.manufacturing_year, v.chassis_number && `Chassis ${v.chassis_number}`].filter(Boolean).join(" · ")}
                </div>
              </div>
            )}
          />
        </div>
      }
    >
      {value.id && (
        <div className="mb-3 flex items-center justify-between rounded-md bg-green-50 px-3 py-1.5 text-xs text-green-800">
          <span>Saved vehicle loaded. Update only what changed.</span>
          <button type="button" className={buttonClass.link} onClick={() => onChange(toVehicleForm(null))}>
            Clear
          </button>
        </div>
      )}
      <div className="grid grid-cols-1 gap-3 md:grid-cols-6">
        <TextInput label="Registration number" required caps value={value.registration_number} onChange={set("registration_number")} error={err("registration_number")} placeholder="DHAKA METRO-GA-12-3456" wrapperClass="md:col-span-3" />
        <TextInput label="Vehicle type (ধরন)" caps value={value.vehicle_type} onChange={set("vehicle_type")} error={err("vehicle_type")} placeholder="CAR (HATCH BACK)" wrapperClass="md:col-span-3" />
        <TextInput label="Chassis number" caps value={value.chassis_number} onChange={set("chassis_number")} error={err("chassis_number")} wrapperClass="md:col-span-2" />
        <TextInput label="Engine number" caps value={value.engine_number} onChange={set("engine_number")} error={err("engine_number")} wrapperClass="md:col-span-2" />
        <TextInput label="Manufacturer" caps value={value.manufacturer} onChange={set("manufacturer")} error={err("manufacturer")} placeholder="TOYOTA" wrapperClass="md:col-span-2" />
        <TextInput label="Manufacturing year" inputMode="numeric" maxLength={4} value={value.manufacturing_year} onChange={set("manufacturing_year")} error={err("manufacturing_year")} wrapperClass="md:col-span-2" />
        <TextInput label="Previous registration no. (if any)" caps value={value.previous_registration_number} onChange={set("previous_registration_number")} error={err("previous_registration_number")} wrapperClass="md:col-span-4" />
      </div>
    </Section>
  );
}

// ---------- main form ----------

export function TransferForm({ transfer }: { transfer: Transfer | null }) {
  const router = useRouter();
  const [form, setForm] = useState<FormState>(() => initialState(transfer));
  const [errors, setErrors] = useState<Errors>({});
  const [message, setMessage] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);
  const wordsTouched = useRef(!!transfer?.sale_price_words);
  const formRef = useRef<HTMLFormElement>(null);

  // New transfer: pre-fill registration authority and bank from the last transfer.
  useEffect(() => {
    if (transfer) return;
    api<{ registration_authority: string | null; fee_bank_name: string | null }>("/api/transfers/defaults")
      .then((d) =>
        setForm((f) => ({
          ...f,
          sale: {
            ...f.sale,
            registration_authority: f.sale.registration_authority || str(d.registration_authority),
            fee_bank_name: f.sale.fee_bank_name || str(d.fee_bank_name),
          },
        })),
      )
      .catch(() => undefined);
  }, [transfer]);

  const setSale = (key: keyof SaleForm) => (v: string) => setForm((f) => ({ ...f, sale: { ...f.sale, [key]: v } }));

  async function fillWords() {
    const amount = Number(form.sale.sale_price.replace(/[,\s/-]/g, ""));
    if (!amount || wordsTouched.current) return;
    try {
      const r = await api<{ words: string }>(`/api/transfers/amount-in-words?amount=${amount}`);
      setForm((f) => ({ ...f, sale: { ...f.sale, sale_price_words: r.words } }));
    } catch {
      /* words stay editable by hand */
    }
  }

  function clientErrors(): Errors {
    const e: Errors = {};
    if (!form.seller.name.trim()) e["seller.name"] = "Required";
    if (!form.buyer.name.trim()) e["buyer.name"] = "Required";
    if (!form.vehicle.registration_number.trim()) e["vehicle.registration_number"] = "Required";
    if (!form.sale.sale_date) e["sale_date"] = "Required";
    if (form.sale.sale_price && !/^\d+$/.test(form.sale.sale_price.replace(/[,\s]/g, ""))) e["sale_price"] = "Numbers only";
    form.witnesses.forEach((w, i) => {
      if (!w.name.trim() && (w.address.trim() || w.phone.trim())) e[`witnesses.${i}.name`] = "Name is required";
    });
    return e;
  }

  async function save(event?: FormEvent) {
    event?.preventDefault();
    if (saving) return;
    const local = clientErrors();
    setErrors(local);
    if (Object.keys(local).length) {
      setMessage("Please fix the highlighted fields.");
      return;
    }
    // Only filled rows are sent; remember which on-screen row each one came from.
    const witnessRows = form.witnesses.flatMap((w, i) => (w.name.trim() ? [i] : []));
    const witnesses = witnessRows.map((i) => {
      const w = form.witnesses[i];
      return { name: w.name.trim(), address: orNull(w.address), phone: orNull(w.phone) };
    });
    const payload = {
      seller: personPayload(form.seller),
      buyer: personPayload(form.buyer),
      vehicle: vehiclePayload(form.vehicle),
      registration_authority: orNull(form.sale.registration_authority),
      sale_price: form.sale.sale_price.trim() ? Number(form.sale.sale_price.replace(/[,\s]/g, "")) : null,
      sale_price_words: orNull(form.sale.sale_price_words),
      sale_date: form.sale.sale_date,
      fee_bank_name: orNull(form.sale.fee_bank_name),
      notes: orNull(form.sale.notes),
      witnesses,
    };
    setSaving(true);
    setMessage(null);
    try {
      const saved = transfer
        ? await api<Transfer>(`/api/transfers/${transfer.id}`, { method: "PUT", body: payload })
        : await api<Transfer>("/api/transfers", { method: "POST", body: payload });
      router.push(`/transfers/${saved.id}`);
    } catch (err) {
      if (err instanceof ApiError) {
        const fields = Object.fromEntries(
          Object.entries(err.fields).map(([key, msg]) => [
            key.replace(/^witnesses\.(\d+)\./, (_, n) => `witnesses.${witnessRows[Number(n)]}.`),
            msg,
          ]),
        );
        setErrors(fields);
        setMessage(fields.form ?? err.message);
      } else {
        setMessage("Could not save. Check the connection and try again.");
      }
      setSaving(false);
    }
  }

  // Ctrl+S / Ctrl+Enter saves. Enter in a text box moves to the next field instead of submitting.
  function onKeyDown(e: KeyboardEvent<HTMLFormElement>) {
    if ((e.ctrlKey || e.metaKey) && (e.key === "s" || e.key === "Enter")) {
      e.preventDefault();
      save();
      return;
    }
    const target = e.target as HTMLElement;
    if (e.key === "Enter" && target.tagName === "INPUT" && (target as HTMLInputElement).type !== "search") {
      e.preventDefault();
      const fields = Array.from(
        formRef.current?.querySelectorAll<HTMLElement>("input:not([type=search]):not([type=radio]), textarea, select") ?? [],
      );
      fields[fields.indexOf(target) + 1]?.focus();
    }
  }

  useEffect(() => {
    if (Object.keys(errors).length) {
      formRef.current?.querySelector<HTMLElement>("[aria-invalid=true]")?.focus();
    }
  }, [errors]);

  const price = Number(form.sale.sale_price.replace(/[,\s]/g, ""));

  return (
    <form ref={formRef} onSubmit={save} onKeyDown={onKeyDown} className="space-y-4" noValidate>
      <PersonSection role="seller" title="Seller (বিক্রেতা)" value={form.seller} onChange={(seller) => setForm((f) => ({ ...f, seller }))} errors={errors} full={false} />
      <PersonSection role="buyer" title="Buyer (ক্রেতা)" value={form.buyer} onChange={(buyer) => setForm((f) => ({ ...f, buyer }))} errors={errors} full />
      <VehicleSection value={form.vehicle} onChange={(vehicle) => setForm((f) => ({ ...f, vehicle }))} errors={errors} />

      <Section title="Sale">
        <div className="grid grid-cols-1 gap-3 md:grid-cols-6">
          <TextInput label="Sale price (Taka)" inputMode="numeric" value={form.sale.sale_price} onChange={setSale("sale_price")} onBlur={fillWords} error={errors["sale_price"]} hint={price ? formatTaka(price) : undefined} wrapperClass="md:col-span-2" />
          <TextInput
            label="Amount in words"
            value={form.sale.sale_price_words}
            onChange={(v) => {
              wordsTouched.current = v.trim() !== "";
              setSale("sale_price_words")(v);
            }}
            error={errors["sale_price_words"]}
            hint="Filled automatically; you can edit it"
            wrapperClass="md:col-span-3"
          />
          <TextInput label="Sale date" required type="date" value={form.sale.sale_date} onChange={setSale("sale_date")} error={errors["sale_date"]} wrapperClass="md:col-span-1" />
          <TextInput label="Registration authority (Forms 20, 21)" caps value={form.sale.registration_authority} onChange={setSale("registration_authority")} error={errors["registration_authority"]} placeholder="BRTA, DHAKA METRO CIRCLE-1" wrapperClass="md:col-span-3" />
          <TextInput label="Bank for fee/tax deposit (Owner's Particulars)" caps value={form.sale.fee_bank_name} onChange={setSale("fee_bank_name")} error={errors["fee_bank_name"]} wrapperClass="md:col-span-3" />
          <TextArea label="Internal notes (not printed)" value={form.sale.notes} onChange={setSale("notes")} error={errors["notes"]} wrapperClass="md:col-span-6" />
        </div>
      </Section>

      <Section title="Witnesses (Form 22, optional)">
        <div className="space-y-2">
          {form.witnesses.map((w, i) => {
            const setW = (key: keyof WitnessForm) => (v: string) =>
              setForm((f) => ({ ...f, witnesses: f.witnesses.map((x, j) => (j === i ? { ...x, [key]: v } : x)) }));
            return (
              <div key={i} className="grid grid-cols-1 gap-3 md:grid-cols-12">
                <div className="pt-6 text-sm font-semibold text-slate-500 md:col-span-1">{i + 1}.</div>
                <TextInput label="Name" caps value={w.name} onChange={setW("name")} error={errors[`witnesses.${i}.name`]} wrapperClass="md:col-span-3" />
                <TextInput label="Address" caps value={w.address} onChange={setW("address")} error={errors[`witnesses.${i}.address`]} wrapperClass="md:col-span-5" />
                <TextInput label="Mobile" inputMode="tel" value={w.phone} onChange={setW("phone")} error={errors[`witnesses.${i}.phone`]} wrapperClass="md:col-span-3" />
              </div>
            );
          })}
        </div>
      </Section>

      <div className="sticky bottom-0 -mx-4 flex items-center gap-3 border-t border-slate-200 bg-slate-100/95 px-4 py-3 backdrop-blur">
        <button type="submit" disabled={saving} className={buttonClass.primary}>
          {saving ? "Saving…" : transfer ? "Save changes & Review" : "Save & Review"}
        </button>
        <span className="text-xs text-slate-500">Ctrl+S to save · Enter moves to next field</span>
        <div className="ml-auto max-w-lg">
          <ErrorBox message={message} />
        </div>
      </div>
    </form>
  );
}
