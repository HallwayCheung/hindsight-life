#!/bin/bash
cd "$(dirname "$0")/apps/web" || exit 1
echo "Starting Next.js from $(pwd)"
exec npx next dev -p 3000
