#!/usr/bin/env bash
# Vexa Intelligence Suite Launcher

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

echo "=========================================================="
echo "          INITIATING VEXA INTELLIGENCE SUITE              "
echo "=========================================================="

# Build production assets if missing
if [ ! -d "dist" ]; then
    echo "[*] Building frontend assets..."
    npm run build
fi

echo "[*] Launching Vexa Unified Server on http://localhost:8080 ..."
echo "[*] Newslinks Registry: $(wc -l < Newslinks.txt) feeds indexed."
python3 server.py
