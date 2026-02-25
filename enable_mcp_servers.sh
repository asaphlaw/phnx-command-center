#!/bin/bash
# Enable High-Impact MCP Servers
# Run: source enable_mcp_servers.sh

echo "🔌 ENABLING MCP SERVERS"
echo "========================"
echo ""

# Check which API keys are available
echo "Checking API credentials..."

SERVERS_ENABLED=0

# 1. GitHub (if token available)
if [ -n "$GITHUB_TOKEN" ]; then
    echo "✅ GitHub: Token found - ENABLING"
    export GITHUB_PERSONAL_ACCESS_TOKEN="$GITHUB_TOKEN"
    ((SERVERS_ENABLED++))
else
    echo "⏸️  GitHub: No GITHUB_TOKEN found"
    echo "   Get token: https://github.com/settings/tokens"
fi

# 2. Brave Search (if key available)
if [ -n "$BRAVE_API_KEY" ]; then
    echo "✅ Brave Search: Key found - ENABLING"
    ((SERVERS_ENABLED++))
else
    echo "⏸️  Brave Search: No BRAVE_API_KEY found"
    echo "   Get key: https://brave.com/search/api"
fi

# 3. Google (Gmail/Calendar) - Check for credentials
if [ -f "$HOME/.config/gcloud/application_default_credentials.json" ] || [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "✅ Google: Credentials found - ENABLING"
    ((SERVERS_ENABLED++))
else
    echo "⏸️  Google (Gmail/Calendar): No credentials found"
    echo "   Setup: gcloud auth application-default login"
fi

# 4. Filesystem (always enabled)
echo "✅ Filesystem: Always enabled"
((SERVERS_ENABLED++))

echo ""
echo "========================"
echo "Enabled: $SERVERS_ENABLED/4 servers"
echo ""

if [ $SERVERS_ENABLED -lt 4 ]; then
    echo "To enable more servers, set these environment variables:"
    echo "  export GITHUB_TOKEN='ghp_...'"
    echo "  export BRAVE_API_KEY='...'"
    echo "  gcloud auth application-default login"
    echo ""
fi

echo "MCP Client ready to use!"
