# Command Center Integration - COMPLETE SETUP
## For Bolt Developer - Ready for Prototype

---

## ✅ STATUS: READY FOR PROTOTYPE

**Date:** 2026-02-26  
**Setup:** A + B + C Complete  
**Data Source:** Live PHNX infrastructure  
**Sync:** Every hour automatically  

---

## 📊 DATA ENDPOINT

**Primary URL (after GitHub push):**
```
https://raw.githubusercontent.com/fredericklaw/phnx-dashboard/main/command-center-data.json
```

**Fallback (local during development):**
```
Use your mock data or the sample below
```

---

## 🔄 AUTO-REFRESH IMPLEMENTATION

### React Hook for Command Center

```typescript
// hooks/usePHNXData.ts
import { useState, useEffect } from 'react';

const GITHUB_RAW_URL = 'https://raw.githubusercontent.com/fredericklaw/phnx-dashboard/main/command-center-data.json';

export const usePHNXData = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(GITHUB_RAW_URL);
        
        if (!response.ok) throw new Error('Failed to fetch');
        
        const json = await response.json();
        setData(json);
        setError(null);
      } catch (err) {
        console.error('PHNX fetch error:', err);
        setError(err);
        // Fallback to mock data if fetch fails
      } finally {
        setLoading(false);
      }
    };

    // Initial fetch
    fetchData();

    // Refresh every hour (3600000ms)
    const interval = setInterval(fetchData, 3600000);

    return () => clearInterval(interval);
  }, []);

  return { data, loading, error, refetch: () => fetchData() };
};
```

### Usage in Components

```typescript
// App.tsx or Dashboard.tsx
import { usePHNXData } from './hooks/usePHNXData';

function Dashboard() {
  const { data, loading, error } = usePHNXData();

  if (loading) return <div>Loading PHNX data...</div>;
  if (error) return <div>Error loading data</div>;
  if (!data) return <div>No data available</div>;

  return (
    <div>
      {/* RSI Agents */}
      <RSIPanel agents={data.rsi.agents} />
      
      {/* Infrastructure */}
      <InfraPanel infrastructure={data.infrastructure} />
      
      {/* $200K Goal */}
      <GoalTracker goal={data.goal} />
      
      {/* Business Data */}
      <BusinessPanel 
        clients={data.business.pt_clients}
        revenue={data.business.revenue}
        actions={data.business.actions}
      />
      
      {/* Projects */}
      <ProjectGrid projects={data.projects} />
      
      {/* Notifications */}
      <NotificationPanel notifications={data.notifications} />
    </div>
  );
}
```

---

## 📋 DATA STRUCTURE

### Session Info
```json
{
  "session": {
    "id": "fredericklaw",
    "name": "Frederick Law",
    "email": "fred@frederickpt.com"
  }
}
```

### RSI Agents
```json
{
  "rsi": {
    "status": "active",
    "agents": {
      "forager": { "status": "idle", "queue": 54, "lastRun": "2m ago" },
      "forge": { "status": "idle", "queue": 0, "lastRun": "2m ago" },
      "crucible": { "status": "idle", "queue": 54, "lastRun": "2m ago" },
      "warden": { "status": "idle", "queue": 20, "lastRun": "2m ago" }
    }
  }
}
```

### Infrastructure
```json
{
  "infrastructure": {
    "core": {
      "browserUse": { "status": "active", "version": "0.11.13" },
      "vectorMemory": { "status": "active", "collections": 1 },
      "mcpClient": { "status": "active", "servers": 6 },
      "langGraph": { "status": "active", "workflows": 3 }
    },
    "mcpServers": [
      { "name": "GitHub", "status": "connected", "user": "fredericklaw" },
      { "name": "Google", "status": "connected", "services": ["gmail", "calendar"] },
      { "name": "Filesystem", "status": "active" },
      { "name": "Fetch", "status": "active" },
      { "name": "Git", "status": "active" },
      { "name": "SQLite", "status": "active" }
    ]
  }
}
```

### $200K Goal
```json
{
  "goal": {
    "target": 200000,
    "monthly_target": 16667,
    "current": 0,
    "percent_complete": 0,
    "months_remaining": 10,
    "needed_per_month": 20000,
    "status": "behind",
    "urgency": "CRITICAL"
  }
}
```

### Business Data
```json
{
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
      { "task": "Call Construct Fitness", "priority": "CRITICAL", "potential_revenue": 2000 },
      { "task": "Call Chao for renewal", "priority": "HIGH", "potential_revenue": 1500 },
      { "task": "Call Lokey for renewal", "priority": "HIGH", "potential_revenue": 1500 },
      { "task": "Post availability on IG", "priority": "MEDIUM", "potential_revenue": 0 },
      { "task": "Follow up on 2 leads", "priority": "MEDIUM", "potential_revenue": 1000 }
    ]
  }
}
```

### Projects
```json
{
  "projects": [
    { "id": "1", "name": "RSI System", "status": "active", "health": 100, "category": "Infrastructure" },
    { "id": "2", "name": "PT Booking Bot", "status": "active", "health": 100, "category": "Revenue" },
    { "id": "3", "name": "Browser-Use", "status": "complete", "health": 100, "category": "Infrastructure" },
    { "id": "4", "name": "MCP Suite", "status": "complete", "health": 100, "category": "Infrastructure" },
    { "id": "5", "name": "Command Center", "status": "in_progress", "health": 85, "category": "Infrastructure" },
    { "id": "6", "name": "Group Training", "status": "planned", "health": 0, "category": "Revenue" },
    { "id": "7", "name": "Digital Products", "status": "planned", "health": 0, "category": "Revenue" }
  ]
}
```

### Notifications
```json
{
  "notifications": [
    { "type": "urgent", "message": "Construct Fitness has 0 sessions remaining", "action": "Call now" },
    { "type": "warning", "message": "2 clients at risk of churn", "action": "Review" },
    { "type": "info", "message": "RSI system processed 12 proposals", "action": "View" }
  ]
}
```

---

## 🎨 UI RECOMMENDATIONS

### Priority Widgets for Prototype:

1. **$200K Goal Progress Bar** (Critical)
   - Show 0% complete
   - Highlight "behind" status
   - Show needed per month: $20,000

2. **At-Risk Clients Alert** (Critical)
   - Red alert for Construct Fitness (0 sessions)
   - Yellow for Chao & Lokey
   - Show potential revenue loss: $4,500

3. **RSI Agent Status** (Infrastructure)
   - 4 pillars with queue counts
   - Show Forager: 54 proposals queued

4. **Today's Actions** (Task List)
   - 5 actionable items
   - Priorities: CRITICAL, HIGH, MEDIUM

5. **Infrastructure Health** (System)
   - 6 MCP servers connected
   - All systems green

---

## ⚡ QUICK START FOR PROTOTYPE

### Option 1: Use Live Data (Recommended)
```bash
# Add to your React app
npm install # if not done

# Update App.tsx with usePHNXData hook
# Deploy to Bolt
```

### Option 2: Use Local JSON (Development)
```bash
# Copy the generated file to your public folder
cp ~/.openclaw/workspace/command-center-data.json ./public/

# In App.tsx:
const response = await fetch('/command-center-data.json');
```

---

## 🔄 SYNC SCHEDULE

- **Frequency:** Every hour (:00 minutes)
- **Cron:** `0 * * * *` 
- **Log:** `/tmp/sync.log`
- **Last Update:** Check `data.last_updated`

---

## 🚨 TROUBLESHOOTING

### If GitHub fetch fails:
1. Check if repo is public: https://github.com/fredericklaw/phnx-dashboard
2. Verify raw URL: https://raw.githubusercontent.com/fredericklaw/phnx-dashboard/main/command-center-data.json
3. Fallback to local mock data

### If data is stale:
1. Check last_updated timestamp
2. Cron runs every hour
3. Manual sync: `~/.openclaw/workspace/sync-command-center.sh`

---

## 📞 SUPPORT

**Files Location:**
- Sync script: `~/.openclaw/workspace/sync-command-center.sh`
- Data file: `~/.openclaw/workspace/command-center-data.json`
- Log file: `/tmp/sync.log`

**Commands:**
```bash
# Manual sync
~/.openclaw/workspace/sync-command-center.sh

# Check cron
 crontab -l | grep sync

# View data
cat ~/.openclaw/workspace/command-center-data.json | jq
```

---

*Ready for prototype deployment!* 🚀
