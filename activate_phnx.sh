#!/bin/bash
# Activate PHNX Environment

echo "🔥 Activating PHNX Core..."

# Set API keys
export BROWSER_USE_API_KEY='bu_nPKfYnxUcIqKZf-hNx2L_iPa6u_7e3-ON0yrqXjDkEY'

# Activate Python environment
cd ~/.openclaw/workspace/browser-use-setup
source .venv/bin/activate

# Add PHNX to path
export PYTHONPATH="${PYTHONPATH}:~/.openclaw/workspace"

echo "✅ PHNX activated!"
echo ""
echo "Quick start:"
echo "  python3 -c 'from phnx import PHNXCore; p = PHNXCore()'"
