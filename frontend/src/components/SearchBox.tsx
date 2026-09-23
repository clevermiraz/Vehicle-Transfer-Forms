"use client";

import { useEffect, useId, useRef, useState, type ReactNode } from "react";

import { api } from "@/lib/api";
import { inputClass } from "./ui";

interface SearchBoxProps<T> {
  endpoint: string; // e.g. "/api/people/search"
  placeholder: string;
  renderItem: (item: T) => ReactNode;
  onSelect: (item: T) => void;
  autoFocus?: boolean;
}

/** Type to search saved records; arrow keys + Enter to pick one. */
export function SearchBox<T extends { id: number | null }>({ endpoint, placeholder, renderItem, onSelect, autoFocus }: SearchBoxProps<T>) {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<T[]>([]);
  const [active, setActive] = useState(0);
  const [open, setOpen] = useState(false);
  const boxRef = useRef<HTMLDivElement>(null);
  const listId = useId();

  useEffect(() => {
    const q = query.trim();
    if (q.length < 2) return;
    const timer = setTimeout(async () => {
      try {
        const items = await api<T[]>(`${endpoint}?q=${encodeURIComponent(q)}`);
        setResults(items);
        setActive(0);
        setOpen(true);
      } catch {
        setResults([]);
      }
    }, 200);
    return () => clearTimeout(timer);
  }, [query, endpoint]);

  useEffect(() => {
    const close = (e: MouseEvent) => {
      if (!boxRef.current?.contains(e.target as Node)) setOpen(false);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  function pick(item: T) {
    onSelect(item);
    setQuery("");
    setResults([]);
    setOpen(false);
  }

  function onKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive((i) => Math.min(i + 1, results.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive((i) => Math.max(i - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault(); // never submit the whole form from the search box
      if (open && results[active]) pick(results[active]);
    } else if (e.key === "Escape") {
      setOpen(false);
    }
  }

  const showNoMatch = open && query.trim().length >= 2 && results.length === 0;

  return (
    <div ref={boxRef} className="relative">
      <input
        type="search"
        value={query}
        autoFocus={autoFocus}
        placeholder={placeholder}
        onChange={(e) => {
          setQuery(e.target.value);
          if (e.target.value.trim().length < 2) setOpen(false);
        }}
        onFocus={() => results.length && setOpen(true)}
        onKeyDown={onKeyDown}
        className={`${inputClass} bg-amber-50`}
        role="combobox"
        aria-expanded={open}
        aria-controls={listId}
      />
      {open && results.length > 0 && (
        <ul id={listId} role="listbox" className="absolute z-20 mt-1 max-h-72 w-full overflow-auto rounded-md border border-slate-200 bg-white shadow-lg">
          {results.map((item, i) => (
            <li
              key={item.id}
              role="option"
              aria-selected={i === active}
              onMouseDown={(e) => {
                e.preventDefault();
                pick(item);
              }}
              onMouseEnter={() => setActive(i)}
              className={`cursor-pointer px-3 py-2 text-sm ${i === active ? "bg-blue-50" : ""}`}
            >
              {renderItem(item)}
            </li>
          ))}
        </ul>
      )}
      {showNoMatch && (
        <div className="absolute z-20 mt-1 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm text-slate-500 shadow-lg">
          No saved match. Type the details below.
        </div>
      )}
    </div>
  );
}
