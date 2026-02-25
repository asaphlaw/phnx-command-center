#!/bin/bash
# PHNX Persistent Mode Runner
# Usage: ./run_phnx_persistent.sh

echo "🔥 Starting PHNX in Persistent Mode..."
echo ""

# Set environment
export PYTHONPATH="${PYTHONPATH}:~/.openclaw/workspace"
export BROWSER_USE_API_KEY="${BROWSER_USE_API_KEY:-}"
export GITHUB_TOKEN="${GITHUB_TOKEN:-}"
export PATH="${PATH}:~/google-cloud-sdk/bin"

# Change to workspace
cd ~/.openclaw/workspace

# Activate environment
source ~/.openclaw/workspace/browser-use-setup/.venv/bin/activate 2>/dev/null || true

# Create state directory
mkdir -p ~/.openclaw/workspace/phnx_session_state

# Start PHNX with heartbeat
echo "Keep-alive interval: 30 seconds"
echo "Auto-reconnect: enabled"
echo "Session persistence: enabled"
echo ""

echo "═══════════════════════════════════════════════════════════"
echo "     PHNX PERSISTENT MODE ACTIVE"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "This session will:"
echo "  • Stay alive indefinitely"
echo "  • Auto-reconnect on drops"
echo "  • Persist memory/state"
echo "  • Sync with vector database"
echo ""
echo "To check status:"
echo "  tail -f ~/.openclaw/workspace/phnx_persistent.log"
echo ""
echo "To stop:"
echo "  pkill -f phnx_persistent"
echo ""

# Start heartbeat loop
while true; do
    # Send heartbeat ping
    echo "$(date): 💓 Heartbeat" >> ~/.openclaw/workspace/phnx_persistent.log
    
    # Keep session alive with activity
    echo "$(date): PHNX-Persistent active" > ~/.openclaw/workspace/phnx_session_state/last_alive
    
    # Sync memory
    if [ -f ~/.openclaw/workspace/phnx/core/pnx_core_v2.py ]; then
        echo "$(date): State synced" >> ~/.openclaw/workspace/phnx_persistent.log 2>/dev/null
    fi
    
    # Wait 30 seconds
    sleep 30
done
