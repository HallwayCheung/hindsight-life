import type { NextConfig } from "next";
import path from "path";

const rootDir = path.resolve(__dirname, "../..");

const nextConfig: NextConfig = {
  turbopack: {
    root: path.resolve(__dirname),
    resolveAlias: {
      // Ensure packages from root node_modules are found
    },
  },
  webpack: (config) => {
    config.resolve.modules.push(path.resolve(rootDir, "node_modules"));
    return config;
  },
};

export default nextConfig;
