# PHNX Command Center - Comprehensive Design Document
## For Bolt Deployment

---

## 🎯 MISSION

Create a unified visual interface that displays:
- Complete infrastructure overview
- All agents and their status
- Ongoing projects
- Real-time metrics
- Control interface

---

## 📊 INFRASTRUCTURE INVENTORY

### CORE SYSTEMS

```
┌─────────────────────────────────────────────────────────────────┐
│                    PHNX INFRASTRUCTURE MAP                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LAYER 1: INTERFACE                                              │
│  ├── Kimi Web Chat (Current)                                     │
│  ├── KimiClaw (Coordinator - Persistent)                         │
│  └── Telegram (PT Bot - Active)                                  │
│                                                                  │
│  LAYER 2: PHNX CORE                                              │
│  ├── Browser-Use (Web Automation) ✅                            │
│  ├── Vector Memory (ChromaDB) ✅                                │
│  ├── MCP Client (6 Servers) ✅                                  │
│  ├── LangGraph (Workflows) ✅                                   │
│  └── E2B (Code Sandbox) ⏳                                      │
│                                                                  │
│  LAYER 3: RSI SYSTEM                                             │
│  ├── Forager (Researcher) ✅                                    │
│  ├── Forge (Developer) ✅                                       │
│  ├── Crucible (Validator) ✅                                    │
│  └── Warden (Governor) ✅                                       │
│                                                                  │
│  LAYER 4: MCP SERVERS                                            │
│  ├── GitHub (fredericklaw) ✅                                   │
│  ├── Google (Gmail/Calendar) ✅                                 │
│  ├── Filesystem ✅                                              │
│  ├── Fetch ✅                                                   │
│  ├── Git ✅                                                     │
│  └── SQLite ✅                                                  │
│                                                                  │
│  LAYER 5: PROJECTS                                               │
│  ├── RSI 4-Pillar System (Active)                               │
│  ├── PT Booking Bot (Active)                                    │
│  ├── Browser-Use Integration (Complete)                         │
│  ├── MCP Server Suite (Complete)                                │
│  └── Command Center (In Progress)                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎨 COMMAND CENTER DESIGN

### Layout Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  PHNX COMMAND CENTER                    [Status: 🟢 OPERATIONAL] │
├─────────────────┬─────────────────────────┬─────────────────────┤
│                 │                         │                     │
│  INFRASTRUCTURE │    AGENT SWARM          │   REAL-TIME         │
│  HEALTH         │    STATUS               │   METRICS           │
│                 │                         │                     │
│  🟢 Core        │  🤖 Forager    🟢      │  CPU: 23%          │
│  🟢 RSI         │  🔨 Forge      🟢      │  RAM: 1.2GB        │
│  🟢 MCP         │  🔥 Crucible   🟢      │  Uptime: 4h 32m    │
│  🟢 Memory      │  🛡️ Warden     🟢      │                     │
│                 │                         │  Active Tasks: 3   │
│  [View Details] │  [View Logs]            │  Queue: 12         │
│                 │                         │                     │
├─────────────────┴─────────────────────────┴─────────────────────┤
│                                                                 │
│  PROJECT DASHBOARD                                              │
│  ┌──────────────┬──────────────┬──────────────┬──────────────┐ │
│  │ RSI System   │ PT Bot       │ Browser-Use  │ MCP Suite    │ │
│  │ Status: 🟢   │ Status: 🟢   │ Status: 🟢   │ Status: 🟢   │ │
│  │ Health: 100% │ Bookings: 0  │ Version: 0.11│ Servers: 6   │ │
│  │ Last: 2m ago │ Last: --     │ Tests: ✅    │ APIs: ✅     │ │
│  └──────────────┴──────────────┴──────────────┴──────────────┘ │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  COMMAND INTERFACE                                              │
│  [Run Forager] [Check Status] [Deploy Changes] [View Reports]  │
│                                                                 │
│  > _                                                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 GENIUS IDEAS FOR COMMAND CENTER

### 1. **Holographic Agent View**
- 3D visualization of agents working
- Real-time animation of data flow
- Click agent to see internals

### 2. **Predictive Health Cards**
- ML-predicted system failures
- Proactive maintenance alerts
- "Fix before it breaks" recommendations

### 3. **Voice Command Interface**
- "Hey PHNX, run forager"
- Speech-to-text command input
- Audio feedback for status

### 4. **AR/VR Integration**
- Put on VR headset = enter command center
- Walk around infrastructure in 3D space
- Grab agents with hand controllers

### 5. **Collaborative Workspace**
- Multiple users in same command center
- Real-time cursor tracking
- Shared annotations

### 6. **Chaos Engineering Mode**
- "Break things" button
- Simulates failures for testing
- Validates RSI self-healing

### 7. **Time Travel Debugger**
- Scroll back through system history
- See what happened at any point
- Replay agent decisions

### 8. **Sentiment Dashboard**
- Track "mood" of system
- Agent stress levels
- Color-coded emotional state

### 9. **Auto-Documentation**
- Screenshots system changes
- Generates changelog automatically
- Creates video demos

### 10. **Gamification**
- Achievement badges for milestones
- Leaderboard for agent efficiency
- XP points for system optimizations

---

## 🛠️ TECH STACK FOR BOLT

### Frontend
- **Framework:** React + TypeScript
- **Styling:** Tailwind CSS + Framer Motion (animations)
- **Charts:** Recharts / D3.js
- **3D:** Three.js (optional for holographic view)
- **Icons:** Lucide React

### Backend
- **Runtime:** Node.js + Express
- **Real-time:** Socket.io (WebSocket)
- **Database:** SQLite (local state)
- **API:** REST + GraphQL

### Integration
- **RSI API:** Direct file system calls
- **MCP Bridge:** Proxy to MCP servers
- **Metrics:** System information gathering
- **Logs:** Real-time log streaming

---

## 📱 RESPONSIVE BREAKPOINTS

- **Desktop:** 1920x1080 (full dashboard)
- **Laptop:** 1366x768 (condensed view)
- **Tablet:** 1024x768 (stacked panels)
- **Mobile:** 375x812 (single column, essential only)

---

## 🔐 SECURITY CONSIDERATIONS

- API keys stored in environment variables
- GitHub token never exposed to frontend
- Read-only access by default
- Confirmation for destructive actions
- Session timeout for idle users

---

## 📈 SUCCESS METRICS

- Load time < 2 seconds
- Real-time updates < 500ms latency
- 99% uptime for command center itself
- User can perform any action in < 3 clicks

---

*Design Document v1.0 - Ready for Implementation*
