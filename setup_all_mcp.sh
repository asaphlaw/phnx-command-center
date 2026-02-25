#!/bin/bash
# Master MCP Server Setup - A to D in order
# Usage: source setup_all_mcp.sh

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     🔌 MCP SERVER SETUP - COMPLETE PRODUCTIVITY SUITE        ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "This script will set up MCP servers in order of impact:"
echo ""
echo "  A) GitHub (Impact: 10/10) - Code management"
echo "  B) Brave Search (Impact: 9/10) - Web research"
echo "  C) Google Workspace (Impact: 9/10) - Email/Calendar"
echo "  D) Continue with current 4 servers"
echo ""
echo "Current productivity: 32/73 (44%)"
echo "Target productivity: 64/73 (88%)"
echo ""

read -p "Continue with setup? (y/n): " CONTINUE

if [ "$CONTINUE" != "y" ]; then
    echo "Setup cancelled."
    return 0
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP A: GITHUB SETUP (Highest Impact)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

read -p "Set up GitHub? (y/n/skip): " GITHUB
if [ "$GITHUB" == "y" ]; then
    source ~/.openclaw/workspace/setup_github.sh
elif [ "$GITHUB" == "skip" ]; then
    echo "⏭️  Skipping GitHub"
else
    echo "❌ GitHub setup declined"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP B: BRAVE SEARCH SETUP"
echo "═══════════════════════════════════════════════════════════════"
echo ""

read -p "Set up Brave Search? (y/n/skip): " BRAVE
if [ "$BRAVE" == "y" ]; then
    source ~/.openclaw/workspace/setup_brave.sh
elif [ "$BRAVE" == "skip" ]; then
    echo "⏭️  Skipping Brave Search"
else
    echo "❌ Brave Search setup declined"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "STEP C: GOOGLE WORKSPACE SETUP"
echo "═══════════════════════════════════════════════════════════════"
echo ""

read -p "Set up Google Workspace? (y/n/skip): " GOOGLE
if [ "$GOOGLE" == "y" ]; then
    source ~/.openclaw/workspace/setup_google.sh
elif [ "$GOOGLE" == "skip" ]; then
    echo "⏭️  Skipping Google Workspace"
else
    echo "❌ Google Workspace setup declined"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "SETUP COMPLETE"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Calculate final status
ENABLED=4  # Base: filesystem, fetch, git, sqlite
[ -n "$GITHUB_TOKEN" ] && ENABLED=$((ENABLED + 1))
[ -n "$BRAVE_API_KEY" ] && ENABLED=$((ENABLED + 1))
[ -f "$HOME/.config/gcloud/application_default_credentials.json" ] && ENABLED=$((ENABLED + 1))

echo "Enabled MCP servers: $ENABLED"
echo ""
echo "Current servers:"
echo "  ✅ filesystem    - Local file access"
echo "  ✅ fetch         - Web scraping"
echo "  ✅ git           - Git operations"
echo "  ✅ sqlite        - Database queries"
[ -n "$GITHUB_TOKEN" ] && echo "  ✅ github        - Code management"
[ -n "$BRAVE_API_KEY" ] && echo "  ✅ brave-search  - Web search"
[ -f "$HOME/.config/gcloud/application_default_credentials.json" ] && echo "  ✅ google        - Gmail/Calendar"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "To use these servers, restart Claude Desktop or your terminal"
echo "═══════════════════════════════════════════════════════════════"
