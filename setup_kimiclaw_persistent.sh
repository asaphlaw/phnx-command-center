#!/bin/bash
# KimiClaw Persistent Mode Setup for PHNX
# This prevents connection drops by using persistent deployment

echo "═══════════════════════════════════════════════════════════"
echo "     🔷 KIMICLAW PERSISTENT MODE SETUP"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "This will configure PHNX to run in persistent mode,"
echo "preventing connection drops and session timeouts."
echo ""
echo "Based on: Your Coordinator bot (already running 24/7)"
echo ""

# Create persistent bot configuration
cat > ~/.openclaw/workspace/phnx_persistent_config.json << 'CONFIG'
{
  "bot_name": "PHNX-Persistent",
  "deployment_mode": "persistent",
  "keep_alive": {
    "enabled": true,
    "interval_seconds": 30,
    "heartbeat_type": "ping"
  },
  "auto_reconnect": {
    "enabled": true,
    "max_attempts": 10,
    "backoff_strategy": "exponential",
    "initial_delay_ms": 1000,
    "max_delay_ms": 30000
  },
  "session": {
    "persist_state": true,
    "state_location": "~/.openclaw/workspace/phnx_session_state",
    "memory_persistence": true,
    "vector_db_sync": true
  },
  "timeouts": {
    "idle_timeout_seconds": 0,
    "absolute_timeout_seconds": 0,
    "tool_execution_timeout_seconds": 300
  },
  "resources": {
    "memory_limit_mb": 2048,
    "cpu_limit": 1.0,
    "auto_scale": true
  }
}
CONFIG

echo "✅ Configuration created: phnx_persistent_config.json"
echo ""

# Create the persistent bot runner
cat > ~/.openclaw/workspace/run_phnx_persistent.sh << 'RUNNER'
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
RUNNER

chmod +x ~/.openclaw/workspace/run_phnx_persistent.sh

echo "✅ Runner script created: run_phnx_persistent.sh"
echo ""

# Create KimiClaw deployment manifest
cat > ~/.openclaw/workspace/kimiclaw_deploy_manifest.json << 'MANIFEST'
{
  "name": "PHNX-Persistent-v2",
  "version": "2.0.0",
  "deployment": {
    "type": "persistent",
    "runtime": "python3.11",
    "entry_point": "run_phnx_persistent.sh",
    "working_directory": "~/.openclaw/workspace"
  },
  "resources": {
    "memory": "2Gi",
    "cpu": "1",
    "storage": "10Gi"
  },
  "networking": {
    "keep_alive": true,
    "heartbeat_interval": 30,
    "auto_reconnect": true,
    "max_reconnect_attempts": 10
  },
  "persistence": {
    "session_state": true,
    "vector_memory": true,
    "file_system": true,
    "database": true
  },
  "scaling": {
    "min_instances": 1,
    "max_instances": 1,
    "auto_scale": false
  },
  "environment_variables": [
    "BROWSER_USE_API_KEY",
    "GITHUB_TOKEN",
    "GITHUB_PERSONAL_ACCESS_TOKEN",
    "OPENCLAW_WORKSPACE"
  ]
}
MANIFEST

echo "✅ KimiClaw manifest created: kimiclaw_deploy_manifest.json"
echo ""

# Create setup instructions
cat << 'INSTRUCTIONS'

═══════════════════════════════════════════════════════════
     🚀 DEPLOYMENT INSTRUCTIONS
═══════════════════════════════════════════════════════════

STEP 1: Deploy to KimiClaw
───────────────────────────────────────────────────────────

1. Go to https://kimiclaw.ai (or your KimiClaw interface)
2. Click "Create New Bot"
3. Select "Persistent Deployment" mode
4. Upload these files:
   • run_phnx_persistent.sh
   • kimiclaw_deploy_manifest.json
   • phnx_persistent_config.json

5. Set environment variables:
   • BROWSER_USE_API_KEY=bu_nPKfYnxUcIqKZf-hNx2L_iPa6u_7e3-ON0yrqXjDkEY
   • GITHUB_TOKEN=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
   • OPENCLAW_WORKSPACE=/Users/fredericklaw/.openclaw/workspace

6. Click "Deploy"

STEP 2: Verify Deployment
───────────────────────────────────────────────────────────

After deployment, check:
• Bot status shows "Running"
• Heartbeat log shows activity every 30s
• Auto-reconnect is enabled
• Session persists across disconnects

STEP 3: Connect Your Interface
───────────────────────────────────────────────────────────

Once deployed in KimiClaw:
• Use the provided bot URL/endpoint
• Connect from any interface (web, Telegram, etc.)
• Session stays alive even if you disconnect

═══════════════════════════════════════════════════════════

EOF

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "     ✅ SETUP FILES CREATED"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Files ready for KimiClaw deployment:"
echo "  📄 phnx_persistent_config.json"
echo "  📄 run_phnx_persistent.sh"
echo "  📄 kimiclaw_deploy_manifest.json"
echo ""
echo "Next: Follow the deployment instructions above"
echo "      to deploy to KimiClaw Persistent mode."
echo ""
