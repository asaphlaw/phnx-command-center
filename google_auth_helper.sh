#!/bin/bash
# Interactive Google Auth Setup
# Run this in your terminal: source google_auth_helper.sh

echo "═══════════════════════════════════════════════════════════"
echo "          🔶 GOOGLE AUTHENTICATION HELPER"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Check if already authenticated
if [ -f "$HOME/.config/gcloud/application_default_credentials.json" ]; then
    echo "✅ Google credentials found!"
    cat "$HOME/.config/gcloud/application_default_credentials.json" | head -5
    echo ""
    echo "Running MCP setup..."
    source ~/.openclaw/workspace/setup_google.sh
    exit 0
fi

echo "🔶 Step 1: Authenticate with Google"
echo "───────────────────────────────────────────────────────────"
echo ""
echo "This will open a browser. After authentication, come back here."
echo ""
read -p "Press ENTER to start authentication..."

gcloud auth application-default login

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Authentication successful!"
    echo ""
    echo "🔶 Step 2: Enable Google Workspace MCP"
    echo "───────────────────────────────────────────────────────────"
    source ~/.openclaw/workspace/setup_google.sh
else
    echo ""
    echo "❌ Authentication failed. Please try again."
fi
