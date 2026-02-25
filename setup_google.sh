#!/bin/bash
# Google Workspace MCP Server Setup

echo "═══════════════════════════════════════════════════════════"
echo "          🔶 GOOGLE WORKSPACE MCP SERVER SETUP"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "This will enable:"
echo "  • Gmail (read/send emails)"
echo "  • Google Calendar (read/create events)"
echo "  • Google Drive (file access)"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "SETUP OPTIONS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Option A: gcloud CLI (Recommended)"
echo "-----------------------------------"
echo "1. Install gcloud: https://cloud.google.com/sdk/docs/install"
echo "2. Run: gcloud auth application-default login"
echo "3. Grant permissions for Gmail/Calendar"
echo ""
echo "Option B: Service Account (For automation)"
echo "-------------------------------------------"
echo "1. Go to https://console.cloud.google.com/"
echo "2. Create project or select existing"
echo "3. Enable APIs: Gmail, Calendar, Drive"
echo "4. Create Service Account + Download JSON key"
echo "5. Set: export GOOGLE_APPLICATION_CREDENTIALS='/path/to/key.json'"
echo ""
echo "═══════════════════════════════════════════════════════════"

# Check if already authenticated
if [ -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
    echo "✅ Google credentials found!"
    echo "   Location: ~/.config/gcloud/application_default_credentials.json"
    echo ""
    read -p "Re-authenticate? (y/n): " REAUTH
    if [ "$REAUTH" != "y" ]; then
        echo "Keeping existing credentials."
        GOOGLE_AUTH="yes"
    else
        gcloud auth application-default login
        GOOGLE_AUTH="yes"
    fi
else
    echo "No Google credentials found."
    echo ""
    read -p "Have you run 'gcloud auth application-default login'? (y/n): " AUTH_DONE
    
    if [ "$AUTH_DONE" == "y" ]; then
        if [ -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
            echo "✅ Credentials found!"
            GOOGLE_AUTH="yes"
        else
            echo "❌ Credentials not found at expected location."
            echo "   Expected: ~/.config/gcloud/application_default_credentials.json"
            GOOGLE_AUTH="no"
        fi
    else
        echo ""
        echo "Please run: gcloud auth application-default login"
        echo "Then run this script again."
        return 1
    fi
fi

if [ "$GOOGLE_AUTH" == "yes" ]; then
    # Update config
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    mkdir -p "$CONFIG_DIR"
    
    GITHUB_TOKEN_VALUE="${GITHUB_TOKEN:-${GITHUB_PERSONAL_ACCESS_TOKEN:-}}"
    BRAVE_KEY="${BRAVE_API_KEY:-}"
    
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
        "BRAVE_API_KEY": "$BRAVE_KEY"
      }
    },
    "google": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-google"]
    }
  }
}
EOF
    
    echo ""
    echo "✅ Claude Desktop config updated with Google!"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "GOOGLE WORKSPACE MCP SERVER READY!"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "You can now:"
    echo "  • Read Gmail messages"
    echo "  • Send emails"
    echo "  • View calendar events"
    echo "  • Create calendar events"
    echo "  • Access Google Drive files"
    echo ""
    
    ENABLED_COUNT=5
    IMPACT=64
    
    if [ -n "$GITHUB_TOKEN_VALUE" ]; then
        ENABLED_COUNT=$((ENABLED_COUNT + 1))
        IMPACT=$((IMPACT + 10))
    fi
    
    if [ -n "$BRAVE_KEY" ]; then
        ENABLED_COUNT=$((ENABLED_COUNT + 1))
        IMPACT=$((IMPACT + 9))
    fi
    
    echo "Current servers enabled: $ENABLED_COUNT"
    echo "Productivity Impact: $IMPACT/73 ($(($IMPACT * 100 / 73))%)"
fi
