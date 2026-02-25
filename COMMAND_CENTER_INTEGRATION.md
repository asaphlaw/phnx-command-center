# Command Center Integration Layer
## Connect Bolt Deployment to OpenClaw/PHNX

---

## 🎉 DEPLOYMENT STATUS

**URL:** https://openclaw-kimiclaw-re-pbz1.bolt.host/  
**Status:** ✅ LIVE  
**Session:** demo-user-001  
**Email:** kimiclaw@openclaw.dev  

---

## 🔌 INTEGRATION ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────┐
│                 COMMAND CENTER (Bolt)                        │
│                     (Web Interface)                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │    Tasks     │  │  Pomodoro    │  │    Agents    │      │
│  │   Display    │  │   Timer      │  │   Status     │      │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘      │
│         │                 │                 │               │
│         └────────┬────────┴────────┬────────┘               │
│                  │                 │                        │
│         ┌────────▼────────┐  ┌─────▼──────┐                │
│         │   Bolt DB       │  │   API      │                │
│         │   (SQLite)      │  │  Layer     │                │
│         └────────┬────────┘  └─────┬──────┘                │
└──────────────────┼─────────────────┼───────────────────────┘
                   │                 │
                   │                 │
                   ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    OPENCLAW / PHNX                           │
│                     (Core Systems)                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  RSI 4-Pillar│  │  Vector Mem  │  │  MCP Client  │      │
│  │  System      │  │  (ChromaDB)  │  │  (6 servers) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Airtable     │  │  Goal Track  │  │  File Sys    │      │
│  │ Integration  │  │  ($200K)     │  │  (Workspace) │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 DATA SYNC MAPPING

### Tasks (Bolt ↔ PHNX)
```javascript
// Bolt Database Schema
{
  id: string,
  title: string,
  description: string,
  status: 'todo' | 'in-progress' | 'done',
  priority: 'low' | 'medium' | 'high',
  due_date: timestamp,
  tags: string[],
  created_at: timestamp
}

// PHNX Mapping
{
  source: 'command-center',
  type: 'task',
  data: { /* task data */ },
  sync_status: 'pending' | 'synced',
  last_sync: timestamp
}
```

### Pomodoro Sessions (Bolt ↔ PHNX)
```javascript
// Bolt Database Schema
{
  id: string,
  task_id: string,
  duration: number, // minutes
  start_time: timestamp,
  end_time: timestamp,
  interruptions: number,
  notes: string
}

// PHNX Mapping
→ Logs to ~/.openclaw/workspace/productivity/
→ RSI can analyze productivity patterns
→ Goal Tracker can measure work hours
```

### Agents (Bolt ↔ PHNX)
```javascript
// Bolt Database Schema
{
  id: string,
  name: string,
  type: 'forager' | 'forge' | 'crucible' | 'warden',
  status: 'active' | 'idle' | 'error',
  last_run: timestamp,
  metrics: object
}

// PHNX Mapping
→ Reads from ~/.openclaw/workspace/rsi/status/
→ Real-time agent heartbeat
→ Command execution interface
```

---

## 🔧 INTEGRATION CODE

### API Bridge (Node.js/Express)
```javascript
// bridge-server.js
const express = require('express');
const { exec } = require('child_process');
const fs = require('fs').promises;
const path = require('path');

const app = express();
app.use(express.json());

const WORKSPACE = '/Users/fredericklaw/.openclaw/workspace';

// Health check
app.get('/api/health', async (req, res) => {
  res.json({ 
    status: 'operational',
    timestamp: new Date().toISOString(),
    services: {
      rsi: await checkRSI(),
      phnx: await checkPHNX(),
      airtable: await checkAirtable()
    }
  });
});

// Get RSI status
app.get('/api/rsi/status', async (req, res) => {
  try {
    const status = await fs.readFile(
      path.join(WORKSPACE, 'rsi/logs/orchestrator.log'),
      'utf8'
    );
    const lines = status.split('\n').slice(-20);
    res.json({ logs: lines, status: 'active' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

// Run RSI command
app.post('/api/rsi/run', async (req, res) => {
  const { pillar } = req.body;
  
  exec(
    `cd ${WORKSPACE}/rsi && python3 orchestrate.py --${pillar}`,
    (error, stdout, stderr) => {
      if (error) {
        res.status(500).json({ error: error.message });
      } else {
        res.json({ output: stdout, error: stderr });
      }
    }
  );
});

// Get Airtable data
app.get('/api/airtable/clients', async (req, res) => {
  // Proxy to Airtable integration
  exec(
    `cd ${WORKSPACE}/skills/airtable && python3 airtable_integration.py`,
    (error, stdout) => {
      res.json({ data: stdout });
    }
  );
});

// Get $200K goal status
app.get('/api/goal/status', async (req, res) => {
  exec(
    `cd ${WORKSPACE}/skills && python3 goal_tracker.py`,
    (error, stdout) => {
      res.json({ report: stdout });
    }
  );
});

app.listen(3001, () => {
  console.log('PHNX Bridge running on port 3001');
});
```

---

## 📊 DASHBOARD WIDGETS TO ADD

### 1. $200K Goal Progress Widget
```
┌─────────────────────────────────────┐
│  💰 $200K GOAL TRACKER              │
├─────────────────────────────────────┤
│  Progress: ████████░░░░ 18%         │
│  Current: $36,000 / $200,000        │
│  This Month: $3,055 / $16,667       │
│                                     │
│  🔴 Behind by $13,612               │
│                                     │
│  [View Details] [Action Plan]       │
└─────────────────────────────────────┘
```

### 2. At-Risk Clients Alert
```
┌─────────────────────────────────────┐
│  ⚠️ AT-RISK CLIENTS (3)             │
├─────────────────────────────────────┤
│  🔴 Construct Fitness - 0 sessions  │
│  ⚠️ Chao - 5 sessions               │
│  ⚠️ Lokey - 5 sessions              │
│                                     │
│  [Send Retention Offer] [Call Now]  │
└─────────────────────────────────────┘
```

### 3. RSI Agent Control
```
┌─────────────────────────────────────┐
│  🤖 RSI AGENT SWARM                 │
├─────────────────────────────────────┤
│  Forager  🟢 Idle    Run ▶️         │
│  Forge    🟢 Idle    Run ▶️         │
│  Crucible 🟢 Idle    Run ▶️         │
│  Warden   🟢 Idle    Run ▶️         │
│                                     │
│  [Run Full Cycle] [View Logs]       │
└─────────────────────────────────────┘
```

### 4. Today's Actions (Airtable Sync)
```
┌─────────────────────────────────────┐
│  ✅ TODAY'S ACTIONS                 │
├─────────────────────────────────────┤
│  ☐ Call Construct Fitness           │
│  ☐ Call Chao                        │
│  ☐ Call Lokey                       │
│  ☑ Post availability on IG          │
│  ☐ Follow up on 2 leads             │
│                                     │
│  [Sync with Airtable]               │
└─────────────────────────────────────┘
```

---

## 🚀 NEXT STEPS

### Phase 1: Connect Data (Today)
1. ✅ Deploy Bolt app - DONE
2. ⏳ Create API bridge (300 lines)
3. ⏳ Sync Bolt DB with PHNX workspace
4. ⏳ Test real-time updates

### Phase 2: Add Business Widgets (Tomorrow)
1. Add $200K goal tracker widget
2. Add at-risk clients panel
3. Add RSI agent controls
4. Add Airtable sync button

### Phase 3: Automation (This Week)
1. Auto-sync tasks to Airtable
2. RSI commands from web UI
3. Pomodoro → Productivity tracking
4. Alerts → Telegram notifications

---

## 💻 COMMANDS TO RUN

```bash
# Start bridge server
cd ~/.openclaw/workspace/command-center-bridge
node bridge-server.js

# Test connection
curl http://localhost:3001/api/health

# Sync data
curl http://localhost:3001/api/sync
```

---

## 🎯 INTEGRATION COMPLETE WHEN:

- [ ] Command Center shows live RSI status
- [ ] $200K goal updates in real-time
- [ ] At-risk clients auto-populate
- [ ] Can trigger RSI actions from web
- [ ] Tasks sync between Bolt and Airtable
- [ ] Pomodoro sessions log to PHNX

---

**Command Center is LIVE! Now building the bridge to connect to your PHNX infrastructure.** 🔥
