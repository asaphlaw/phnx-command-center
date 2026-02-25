# MCP Quick Setup - High Impact Servers

## ALREADY ENABLED (4 servers)
✅ filesystem    - Local file access
✅ fetch         - Web scraping via npx
✅ git           - Git operations via npx  
✅ sqlite        - Database queries via npx

## TO ENABLE (Highest Impact First):

### 1. GitHub (Impact: 10/10) - CODE MANAGEMENT
```bash
# Get token: https://github.com/settings/tokens
# Scopes needed: repo, read:org, read:user
export GITHUB_TOKEN='ghp_xxxxxxxxxxxx'
```

### 2. Brave Search (Impact: 9/10) - WEB SEARCH
```bash
# Get key: https://brave.com/search/api (free tier available)
export BRAVE_API_KEY='BSxxxxxxxxxxxxxxxx'
```

### 3. Google Workspace (Impact: 9/10) - EMAIL/CALENDAR
```bash
# Authenticate with Google
gcloud auth application-default login
# Or create service account: https://developers.google.com/workspace/guides/create-credentials
```

### 4. Slack (Impact: 7/10) - MESSAGING
```bash
# Create app: https://api.slack.com/apps
# Add scopes: channels:read, chat:write
export SLACK_BOT_TOKEN='xoxb-xxxxxxxxxxxx'
export SLACK_TEAM_ID='Txxxxxxxx'
```

## ACTIVATE ALL
```bash
cd ~/.openclaw/workspace
source enable_mcp_servers.sh
```

## PRODUCTIVITY GAINS
| Server | Productivity Impact | Use Cases |
|--------|-------------------|-----------|
| GitHub | 10/10 | Push code, create PRs, manage issues |
| Brave Search | 9/10 | Research, fact-checking, discovery |
| Google | 9/10 | Email drafting, calendar scheduling |
| Filesystem | 9/10 | File operations, reading configs |
| Fetch | 8/10 | Web scraping, API calls |
| Git | 8/10 | Commit changes, view diffs, branching |
| Slack | 7/10 | Team notifications, status updates |
| SQLite | 7/10 | Data queries, analytics |

Current: 4/9 servers = 32/73 productivity potential
With all: 9/9 servers = 73/73 productivity potential
