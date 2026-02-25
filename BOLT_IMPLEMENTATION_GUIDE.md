# PHNX Command Center
## Implementation for Bolt.new

### Prompt for Bolt:

Create a React-based Command Center dashboard with the following specifications:

**PROJECT STRUCTURE:**
```
phnx-command-center/
├── src/
│   ├── components/
│   │   ├── Dashboard.tsx
│   │   ├── InfrastructurePanel.tsx
│   │   ├── AgentSwarm.tsx
│   │   ├── MetricsPanel.tsx
│   │   ├── ProjectCards.tsx
│   │   ├── CommandInterface.tsx
│   │   └── StatusIndicator.tsx
│   ├── hooks/
│   │   ├── useSystemMetrics.ts
│   │   ├── useAgentStatus.ts
│   │   └── useRSIStatus.ts
│   ├── types/
│   │   └── index.ts
│   ├── App.tsx
│   └── index.css
├── public/
│   └── index.html
├── package.json
└── README.md
```

**CORE FEATURES:**

1. **Real-time Infrastructure Health Display**
   - Show status of all 6 MCP servers
   - Display RSI 4-pillar system status
   - PHNX Core component health
   - Connection status indicators

2. **Agent Swarm Visualization**
   - Forager, Forge, Crucible, Warden status
   - Last run timestamps
   - Current activity
   - Queue depths

3. **Project Dashboard**
   - RSI System card
   - PT Booking Bot card
   - Browser-Use integration card
   - MCP Server Suite card

4. **Metrics Panel**
   - CPU/Memory usage
   - Uptime counter
   - Active tasks
   - Queue statistics

5. **Command Interface**
   - Quick action buttons
   - Terminal-style command input
   - Output display area

**DESIGN SPECIFICATIONS:**

- Dark theme (cyberpunk/command center aesthetic)
- Neon accents (cyan #00ffff, purple #ff00ff, green #00ff00)
- Glassmorphism panels
- Animated status indicators
- Responsive grid layout

**SAMPLE DATA (for demonstration):**

```typescript
const infrastructureData = {
  core: {
    browserUse: { status: 'active', version: '0.11.13' },
    vectorMemory: { status: 'active', collections: 1 },
    mcpClient: { status: 'active', servers: 6 },
    langGraph: { status: 'active', workflows: 3 }
  },
  rsi: {
    forager: { status: 'idle', lastRun: '2m ago', proposals: 12 },
    forge: { status: 'idle', lastRun: '2m ago', staged: 12 },
    crucible: { status: 'idle', lastRun: '2m ago', validated: 12 },
    warden: { status: 'idle', lastRun: '2m ago', deployed: 20 }
  },
  mcp: {
    github: { status: 'connected', user: 'fredericklaw' },
    google: { status: 'connected', services: ['gmail', 'calendar'] },
    filesystem: { status: 'active' },
    fetch: { status: 'active' },
    git: { status: 'active' },
    sqlite: { status: 'active' }
  }
};
```

**TECHNICAL REQUIREMENTS:**

- React 18 with TypeScript
- Tailwind CSS for styling
- Framer Motion for animations
- Lucide React for icons
- Recharts for metrics graphs
- Socket.io client for real-time updates (optional)

**DEPLOYMENT:**

Ready to deploy on Bolt.new with one-click.

---

## FILE: package.json

```json
{
  "name": "phnx-command-center",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "framer-motion": "^10.16.4",
    "lucide-react": "^0.294.0",
    "recharts": "^2.10.3",
    "tailwindcss": "^3.3.6",
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "typescript": "^5.3.3"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  },
  "devDependencies": {
    "react-scripts": "5.0.1"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  }
}
```

---

## DEPLOY INSTRUCTIONS FOR BOLT:

1. Go to https://bolt.new
2. Create new project
3. Copy all files below
4. Install dependencies: npm install
5. Start dev server: npm start
6. Deploy: Click "Deploy"

---

Ready to generate complete source code.
