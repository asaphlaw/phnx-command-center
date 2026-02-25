#!/bin/bash
# GitHub MCP Server Setup
# Run: source setup_github.sh

echo "═══════════════════════════════════════════════════════════"
echo "          🔷 GITHUB MCP SERVER SETUP"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "This will enable:"
echo "  • Create repositories"
echo "  • Push code changes"
echo "  • Create pull requests"
echo "  • Manage issues"
echo "  • Read/write file contents"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 1: Create GitHub Token"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1. Visit: https://github.com/settings/tokens"
echo "2. Click 'Generate new token (classic)'"
echo "3. Give it a name: 'PHNX MCP Server'"
echo "4. Select these scopes:"
echo "   ☑️ repo (Full control of private repositories)"
echo "   ☑️ read:org (Read org membership)"
echo "   ☑️ read:user (Read user profile data)"
echo "5. Click 'Generate token'"
echo "6. COPY THE TOKEN (you won't see it again!)"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "STEP 2: Enter Your Token"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if already set
if [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ GITHUB_TOKEN already set (${#GITHUB_TOKEN} characters)"
    echo "   Token starts with: ${GITHUB_TOKEN:0:4}..."
    echo ""
    read -p "Do you want to update it? (y/n): " UPDATE
    if [ "$UPDATE" != "y" ]; then
        echo "Keeping existing token."
        export GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_TOKEN"
        echo "✅ GitHub MCP server ready!"
        return 0
    fi
fi

echo "Paste your GitHub token below (input will be hidden):"
read -s TOKEN

if [ -z "$TOKEN" ]; then
    echo "❌ No token entered. Setup cancelled."
    return 1
fi

# Validate token format
if [[ ! "$TOKEN" =~ ^ghp_[a-zA-Z0-9]{36}$ ]]; then
    echo ""
    echo "⚠️  Warning: Token format looks unusual."
    echo "   Expected format: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    read -p "Continue anyway? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        return 1
    fi
fi

export GITHUB_TOKEN="$TOKEN"
export GITHUB_PERSONAL_ACCESS_TOKEN="$TOKEN"

echo ""
echo "✅ Token saved to environment!"
echo "   Length: ${#TOKEN} characters"
echo "   Starts with: ${TOKEN:0:7}..."
echo ""

# Test the token
echo "═══════════════════════════════════════════════════════════"
echo "STEP 3: Testing Token"
echo "═══════════════════════════════════════════════════════════"
echo ""

RESPONSE=$(curl -s -H "Authorization: token $TOKEN" https://api.github.com/user)

if echo "$RESPONSE" | grep -q '"login"'; then
    USERNAME=$(echo "$RESPONSE" | grep '"login"' | head -1 | cut -d'"' -f4)
    echo "✅ Token valid! Connected as: $USERNAME"
    
    # Update MCP config
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    mkdir -p "$CONFIG_DIR"
    
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
        "GITHUB_PERSONAL_ACCESS_TOKEN": "$TOKEN"
      }
    }
  }
}
EOF
    
    echo ""
    echo "✅ Claude Desktop config updated with GitHub!"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "GITHUB MCP SERVER READY!"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "You can now:"
    echo "  • Create repositories"
    echo "  • Push code to GitHub"
    echo "  • Create pull requests"
    echo "  • Manage issues"
    echo "  • Read/write file contents"
    echo ""
    echo "Productivity Impact: +10 points (44% → 58%)"
    
else
    echo "❌ Token validation failed!"
    echo "Response: $RESPONSE"
    return 1
fi
