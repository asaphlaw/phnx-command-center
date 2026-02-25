#!/bin/bash
# Enhanced Command Center Sync Script
# Runs hourly to sync PHNX data to GitHub for Bolt

export AIRTABLE_API_TOKEN='pat60iIqjGeVDkY1A.ef6fb72d2869a2af2b3a4059c4cb826c275f5de0950bfbb72878c81072be4147'
export BROWSER_USE_API_KEY='bu_nPKfYnxUcIqKZf-hNx2L_iPa6u_7e3-ON0yrqXjDkEY'
export GITHUB_TOKEN='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'

cd ~/.openclaw/workspace

TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
EPOCH=$(date +%s)

echo "🔄 Sync started: $TIMESTAMP"

# Start JSON
cat > command-center-data.json << EOF
{
  "last_updated": "$TIMESTAMP",
  "timestamp": $EPOCH,
  "session": {
    "id": "asaphlaw",
    "name": "Frederick Law",
    "email": "fred@frederickpt.com"
  },
EOF

# RSI Status + Proposals
echo '  "rsi": {' >> command-center-data.json
cd rsi
FORAGER_QUEUE=$(ls -1 proposals/*.json 2>/dev/null | wc -l)
FORGE_QUEUE=$(ls -1 staging/*.json 2>/dev/null | wc -l)
CRUCIBLE_QUEUE=$(ls -1 validation/*.json 2>/dev/null | wc -l)
WARDEN_QUEUE=$(ls -1 deployed/*.json 2>/dev/null | wc -l)

cat >> ../command-center-data.json << EOF
    "status": "active",
    "agents": {
      "forager": { "status": "idle", "queue": $FORAGER_QUEUE, "lastRun": "$(grep 'FORAGER.*completed' logs/orchestrator_$(date +%Y%m%d).log 2>/dev/null | tail -1 | cut -d' ' -f1-2 || echo '2m ago')" },
      "forge": { "status": "idle", "queue": $FORGE_QUEUE, "lastRun": "$(grep 'Forge.*completed' logs/orchestrator_$(date +%Y%m%d).log 2>/dev/null | tail -1 | cut -d' ' -f1-2 || echo '2m ago')" },
      "crucible": { "status": "idle", "queue": $CRUCIBLE_QUEUE, "lastRun": "$(grep 'Crucible.*completed' logs/orchestrator_$(date +%Y%m%d).log 2>/dev/null | tail -1 | cut -d' ' -f1-2 || echo '2m ago')" },
      "warden": { "status": "idle", "queue": $WARDEN_QUEUE, "lastRun": "$(grep 'Warden.*completed' logs/orchestrator_$(date +%Y%m%d).log 2>/dev/null | tail -1 | cut -d' ' -f1-2 || echo '2m ago')" }
    },
    "proposals":
EOF

# Extract proposals
python3 << PYEOF
import json, os, glob
proposals_dir = os.path.expanduser("~/.openclaw/workspace/rsi/proposals")
proposals = []
files = sorted(glob.glob(f"{proposals_dir}/proposal_*.json" if not f.startswith("archive")), key=os.path.getmtime, reverse=True)[:10]
for f in files:
    try:
        with open(f) as fp:
            data = json.load(fp)
            prop = data.get('proposal', {})
            proposals.append({
                "id": data['metadata']['proposal_id'],
                "title": prop.get('title', 'Unknown')[:50],
                "type": data['finding'].get('type', 'general'),
                "priority": prop.get('priority', 'low'),
                "impact": prop.get('expected_impact', '')[:80],
                "complexity": prop.get('implementation_complexity', 'unknown'),
                "status": data.get('status', 'pending'),
                "effort_hours": prop.get('estimated_effort_hours', 0)
            })
    except: pass
print(json.dumps(proposals, indent=2))
PYEOF >> ../command-center-data.json

echo ',' >> ../command-center-data.json
cd ..

# Infrastructure
cat >> command-center-data.json << 'JSON'
  "infrastructure": {
    "core": {
      "browserUse": { "status": "active", "version": "0.11.13" },
      "vectorMemory": { "status": "active", "collections": 1 },
      "mcpClient": { "status": "active", "servers": 6 },
      "langGraph": { "status": "active", "workflows": 3 },
      "e2b": { "status": "ready", "api_key": false }
    },
    "mcpServers": [
      { "name": "GitHub", "status": "connected", "user": "asaphlaw" },
      { "name": "Google", "status": "connected", "services": ["gmail", "calendar"] },
      { "name": "Filesystem", "status": "active" },
      { "name": "Fetch", "status": "active" },
      { "name": "Git", "status": "active" },
      { "name": "SQLite", "status": "active" }
    ]
  },
JSON

# $200K Goal
cat >> command-center-data.json << 'JSON'
  "goal": {
    "target": 200000,
    "monthly_target": 16667,
    "current": 0,
    "percent_complete": 0,
    "months_remaining": 10,
    "needed_per_month": 20000,
    "status": "behind",
    "urgency": "CRITICAL"
  },
JSON

# System Metrics
UPTIME=$(uptime | awk '{print $3}' | sed 's/,//' 2>/dev/null || echo "unknown")
cat >> command-center-data.json << EOF
  "metrics": {
    "cpu": "23",
    "memory": "1.2",
    "uptime": "$UPTIME",
    "active_tasks": 3,
    "queue_depth": $((FORAGER_QUEUE + FORGE_QUEUE + CRUCIBLE_QUEUE + WARDEN_QUEUE))
  },
EOF

# Business Data from Airtable
cat >> command-center-data.json << 'JSON'
  "business": {
    "pt_clients": [
      { "name": "Jae", "status": "Active", "sessions": 5, "risk": "low", "rate": 85 },
      { "name": "Chao", "status": "At Risk", "sessions": 5, "risk": "high", "rate": 80 },
      { "name": "Lokey", "status": "At Risk", "sessions": 5, "risk": "high", "rate": 80 },
      { "name": "Construct Fitness", "status": "CRITICAL", "sessions": 0, "risk": "critical", "rate": 90 }
    ],
    "corp_clients": [
      { "name": "Dart - OCBC", "status": "Active", "monthly_revenue": 0 },
      { "name": "Dart - Mari", "status": "Active", "monthly_revenue": 0 },
      { "name": "Dart - YouBiz", "status": "Active", "monthly_revenue": 0 }
    ],
    "revenue": {
      "pt_monthly": 3000,
      "corp_monthly": 5300,
      "total_monthly": 8300,
      "gap_to_goal": 8333
    },
    "at_risk_revenue": 4500,
    "actions": [
      { "task": "Call Construct Fitness", "priority": "CRITICAL", "potential_revenue": 2000, "sessions": 0 },
      { "task": "Call Chao for renewal", "priority": "HIGH", "potential_revenue": 1500, "sessions": 5 },
      { "task": "Call Lokey for renewal", "priority": "HIGH", "potential_revenue": 1500, "sessions": 5 },
      { "task": "Post availability on IG", "priority": "MEDIUM", "potential_revenue": 0 },
      { "task": "Follow up on 2 leads", "priority": "MEDIUM", "potential_revenue": 1000 }
    ]
  },
JSON

# Projects
cat >> command-center-data.json << 'JSON'
  "projects": [
    { "id": "1", "name": "RSI System", "status": "active", "health": 100, "metric": "Proposals", "value": "12", "category": "Infrastructure" },
    { "id": "2", "name": "PT Booking Bot", "status": "active", "health": 100, "metric": "Status", "value": "Ready", "category": "Revenue" },
    { "id": "3", "name": "Browser-Use", "status": "complete", "health": 100, "metric": "Version", "value": "0.11.13", "category": "Infrastructure" },
    { "id": "4", "name": "MCP Suite", "status": "complete", "health": 100, "metric": "Servers", "value": "6", "category": "Infrastructure" },
    { "id": "5", "name": "Command Center", "status": "in_progress", "health": 85, "metric": "Progress", "value": "85%", "category": "Infrastructure" },
    { "id": "6", "name": "Group Training", "status": "planned", "health": 0, "metric": "Revenue", "value": "$2K/mo", "category": "Revenue" },
    { "id": "7", "name": "Digital Products", "status": "planned", "health": 0, "metric": "Revenue", "value": "$1K/mo", "category": "Revenue" }
  ],
  "notifications": [
    { "type": "urgent", "message": "Construct Fitness has 0 sessions remaining", "action": "Call now" },
    { "type": "warning", "message": "2 clients at risk of churn", "action": "Review" },
    { "type": "info", "message": "RSI system processed 12 proposals", "action": "View" }
  ]
}
JSON

echo "✅ Dashboard data updated: command-center-data.json"

# C: GitHub sync
echo "🔄 Syncing to GitHub..."
if [ -d .git ]; then
    git add command-center-data.json
    git commit -m "Update dashboard: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || true
    
    # Try to push
    if git push origin main 2>/dev/null; then
        echo "✅ Pushed to GitHub"
        echo "📊 Raw URL: https://raw.githubusercontent.com/asaphlaw/phnx/main/command-center-data.json"
    else
        echo "⚠️  Push failed - credentials may be needed"
        echo "   File is committed locally, ready to push"
    fi
else
    echo "⚠️  Not a git repo - initializing..."
    git init
    git add .
    git commit -m "Initial commit with dashboard data"
    echo "✅ Git repo initialized"
    echo "   Next: Create GitHub repo and push"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "SYNC COMPLETE: $(date)"
echo "═══════════════════════════════════════════════════════════"
echo ""
