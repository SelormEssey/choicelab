import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  agentRules: false,
  reactStrictMode: true,
  async rewrites() {
    const apiOrigin = process.env.CHOICELAB_API_URL ?? "http://127.0.0.1:8000";
    return [{ source: "/api/:path*", destination: `${apiOrigin}/v1/:path*` }];
  },
};

export default nextConfig;
