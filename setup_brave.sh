#!/bin/bash
# Brave Search MCP Server Setup

echo "═══════════════════════════════════════════════════════════"
echo "          🔍 BRAVE SEARCH MCP SERVER SETUP"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "This will enable:"
echo "  • Web search"
echo "  • News search"
echo "  • Image search"
echo "  • Research and fact-checking"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 1: Get Brave API Key"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Visit: https://brave.com/search/api"
echo "2. Sign up for free tier (2000 queries/month)"
echo "3. Navigate to 'API Keys' section"
echo "4. Create new key: 'PHNX MCP'"
echo "5. COPY THE KEY"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 2: Enter Your API Key"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if already set
if [ -n "$BRAVE_API_KEY" ]; then
    echo "✅ BRAVE_API_KEY already set"
    echo "   Key starts with: ${BRAVE_API_KEY:0:4}..."
    echo ""
    read -p "Do you want to update it? (y/n): " UPDATE
    if [ "$UPDATE" != "y" ]; then
        echo "Keeping existing key."
        return 0
    fi
fi

echo "Paste your Brave API key:"
read -s KEY

if [ -z "$KEY" ]; then
    echo "❌ No key entered. Setup cancelled."
    return 1
fi

export BRAVE_API_KEY="$KEY"

echo ""
echo "✅ Key saved to environment!"
echo ""

# Update config with both GitHub and Brave
CONFIG_DIR="$HOME/Library/Application Support/Claude"
mkdir -p "$CONFIG_DIR"

GITHUB_TOKEN_VALUE="${GITHUB_TOKEN:-${GITHUB_PERSONAL_ACCESS_TOKEN:-}}"

cat > "$CONFIG_DIR/claude_desktop_config.json" << EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "$HOME/.openclaw/workspace"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    "sqlite": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sqlite", "$HOME/.openclaw/workspace/vector_db/chroma.sqlite3"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$GITHUB_TOKEN_VALUE"
      }
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "$KEY"
      }
    }
  }
}
EOF

echo "✅ Claude Desktop config updated with Brave Search!"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "BRAVE SEARCH MCP SERVER READY!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "You can now:"
echo "  • Search the web"
echo "  • Research topics"
echo "  • Fact-check information"
echo "  • Find documentation"
echo ""

if [ -n "$GITHUB_TOKEN_VALUE" ]; then
    echo "Current servers: Filesystem, Fetch, Git, SQLite, GitHub, Brave"
    echo "Productivity Impact: 55/73 (75%)"
else
    echo "Current servers: Filesystem, Fetch, Git, SQLite, Brave"
    echo "Productivity Impact: 41/73 (56%)"
    echo ""
    echo "Next: Run setup_github.sh for maximum productivity!"
fi
