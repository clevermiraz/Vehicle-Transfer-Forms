export class ApiError extends Error {
  status: number;
  /** Validation errors keyed like "seller.nid" or "vehicle.registration_number". */
  fields: Record<string, string>;

  constructor(status: number, message: string, fields: Record<string, string> = {}) {
    super(message);
    this.status = status;
    this.fields = fields;
  }
}

interface ValidationIssue {
  loc: (string | number)[];
  msg: string;
}

function parseError(status: number, body: unknown): ApiError {
  const detail = (body as { detail?: unknown })?.detail;
  if (Array.isArray(detail)) {
    const fields: Record<string, string> = {};
    for (const issue of detail as ValidationIssue[]) {
      const key = issue.loc.filter((part) => part !== "body").join(".");
      fields[key || "form"] = issue.msg.replace(/^Value error, /, "");
    }
    return new ApiError(status, "Please fix the highlighted fields.", fields);
  }
  if (typeof detail === "string") return new ApiError(status, detail);
  return new ApiError(status, `Request failed (${status})`);
}

export async function api<T>(path: string, options: { method?: string; body?: unknown } = {}): Promise<T> {
  const res = await fetch(path, {
    method: options.method ?? "GET",
    headers: options.body === undefined ? undefined : { "Content-Type": "application/json" },
    body: options.body === undefined ? undefined : JSON.stringify(options.body),
    credentials: "same-origin",
  });
  if (res.status === 401 && !path.startsWith("/api/auth/login")) {
    // Full page load on purpose: session expired, drop all in-memory state.
    // eslint-disable-next-line @next/next/no-location-assign-relative-destination
    window.location.href = `/login?next=${encodeURIComponent(window.location.pathname)}`;
    throw new ApiError(401, "Please log in");
  }
  if (!res.ok) {
    throw parseError(res.status, await res.json().catch(() => null));
  }
  return res.status === 204 ? (undefined as T) : ((await res.json()) as T);
}

export function formatDate(iso: string | null): string {
  if (!iso) return "";
  const [y, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${y}`;
}

export function formatTaka(amount: number | null): string {
  if (amount == null) return "";
  const digits = String(amount);
  let head = digits.slice(0, -3);
  const groups: string[] = [];
  while (head.length > 2) {
    groups.unshift(head.slice(-2));
    head = head.slice(0, -2);
  }
  if (head) groups.unshift(head);
  return [...groups, digits.slice(-3)].join(",") + "/-";
}
