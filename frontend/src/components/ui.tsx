import type { InputHTMLAttributes, ReactNode, TextareaHTMLAttributes } from "react";

export const inputClass =
  "w-full rounded-md border border-slate-300 bg-white px-2.5 py-1.5 text-sm shadow-sm outline-none " +
  "focus:border-blue-600 focus:ring-2 focus:ring-blue-200 disabled:bg-slate-100";

export const buttonClass = {
  primary:
    "inline-flex items-center gap-2 rounded-md bg-blue-700 px-4 py-2 text-sm font-semibold text-white shadow-sm " +
    "hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-300 disabled:opacity-50",
  secondary:
    "inline-flex items-center gap-2 rounded-md border border-slate-300 bg-white px-3 py-1.5 text-sm font-medium " +
    "text-slate-800 shadow-sm hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-200 disabled:opacity-50",
  link: "text-sm font-medium text-blue-700 hover:underline",
};

interface FieldProps {
  label: string;
  error?: string;
  hint?: string;
  required?: boolean;
  className?: string;
  children: ReactNode;
}

export function Field({ label, error, hint, required, className = "", children }: FieldProps) {
  return (
    <label className={`block ${className}`}>
      <span className="mb-1 block text-xs font-semibold text-slate-600">
        {label}
        {required && <span className="text-red-600"> *</span>}
      </span>
      {children}
      {error ? (
        <span className="mt-1 block text-xs text-red-700">{error}</span>
      ) : (
        hint && <span className="mt-1 block text-xs text-slate-500">{hint}</span>
      )}
    </label>
  );
}

type TextInputProps = Omit<InputHTMLAttributes<HTMLInputElement>, "onChange" | "value"> & {
  label: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  hint?: string;
  caps?: boolean;
  wrapperClass?: string;
};

export function TextInput({ label, value, onChange, error, hint, caps, wrapperClass, required, ...rest }: TextInputProps) {
  return (
    <Field label={label} error={error} hint={hint} required={required} className={wrapperClass}>
      <input
        {...rest}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        aria-invalid={!!error}
        className={`${inputClass} ${caps ? "caps" : ""} ${error ? "border-red-500" : ""}`}
      />
    </Field>
  );
}

type TextAreaProps = Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "onChange" | "value"> & {
  label: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  wrapperClass?: string;
};

export function TextArea({ label, value, onChange, error, wrapperClass, ...rest }: TextAreaProps) {
  return (
    <Field label={label} error={error} className={wrapperClass}>
      <textarea
        rows={2}
        {...rest}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        aria-invalid={!!error}
        className={`${inputClass} caps resize-y ${error ? "border-red-500" : ""}`}
      />
    </Field>
  );
}

export function Section({ title, action, children }: { title: string; action?: ReactNode; children: ReactNode }) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2">
        <h2 className="text-sm font-bold uppercase tracking-wide text-slate-700">{title}</h2>
        {action}
      </div>
      {children}
    </section>
  );
}

export function ErrorBox({ message }: { message: string | null }) {
  if (!message) return null;
  return (
    <div role="alert" className="rounded-md border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-800">
      {message}
    </div>
  );
}
