#!/bin/bash
# GitHub Push Helper Script
# Run this after creating the GitHub repo

echo "═══════════════════════════════════════════════════════════"
echo "🔗 STEP 2: PUSH CODE TO GITHUB"
echo "═══════════════════════════════════════════════════════════"
echo ""

# Navigate to workspace
cd ~/.openclaw/workspace

echo "1. Checking current git status..."
git status

echo ""
echo "2. Adding remote (your GitHub repo)..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/fredericklaw/phnx-dashboard.git

echo ""
echo "3. Setting branch name..."
git branch -M main

echo ""
echo "4. Pushing to GitHub..."
echo "   (You may be asked to sign in to GitHub)"
echo ""
git push -u origin main

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "✅ IF PUSH SUCCEEDS:"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Your data will be live at:"
echo "https://raw.githubusercontent.com/fredericklaw/phnx-dashboard/main/command-center-data.json"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "❌ IF PUSH FAILS (authentication):"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "You need to set up GitHub authentication:"
echo ""
echo "Option A - GitHub CLI (Recommended):"
echo "   brew install gh"
echo "   gh auth login"
echo ""
echo "Option B - Personal Access Token:"
echo "   1. Go to https://github.com/settings/tokens"
echo "   2. Generate new token (classic)"
echo "   3. Select 'repo' scope"
echo "   4. Copy token"
echo "   5. Run: git push https://<TOKEN>@github.com/fredericklaw/phnx-dashboard.git"
echo ""
