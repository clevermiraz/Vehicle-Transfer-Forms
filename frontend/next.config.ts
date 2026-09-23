import type { NextConfig } from "next";

// The browser only talks to Next.js; /api/* is proxied to FastAPI. Same origin means the
// httpOnly session cookie just works and PDFs open in the browser's own viewer.
const BACKEND_URL = process.env.BACKEND_URL ?? "http://127.0.0.1:8010";

const nextConfig: NextConfig = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${BACKEND_URL}/api/:path*` }];
  },
};

export default nextConfig;
