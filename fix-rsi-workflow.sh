#!/bin/bash
# Fix RSI Workflow - Archive Implemented Proposals

echo "🔧 FIXING RSI WORKFLOW"
echo "======================"
echo ""

cd ~/.openclaw/workspace/rsi

# Create archive directory
mkdir -p archive/implemented
mkdir -p archive/rejected

echo "1. Archiving implemented proposals..."

# Find implemented proposals and move them
IMPLEMENTED_COUNT=0
for file in proposals/proposal_*.json; do
    if [ -f "$file" ]; then
        # Check if status is implemented
        if grep -q '"status": "implemented"' "$file" 2>/dev/null; then
            # Extract ID
            ID=$(basename "$file" .json | sed 's/proposal_//')
            
            # Move to archive
            mv "$file" "archive/implemented/"
            echo "   ✓ Archived: $ID"
            ((IMPLEMENTED_COUNT++))
        fi
    fi
done

echo ""
echo "2. Archiving old staging files..."

# Move old staging files to archive
STAGING_COUNT=0
for dir in staging/forge_*; do
    if [ -d "$dir" ]; then
        # Check if deployed marker exists
        DEPLOYED_FILE=$(ls "$dir"/*.deployed 2>/dev/null | head -1)
        if [ -n "$DEPLOYED_FILE" ]; then
            mv "$dir" archive/implemented/
            echo "   ✓ Archived staging: $(basename $dir)"
            ((STAGING_COUNT++))
        fi
    fi
done

echo ""
echo "3. Cleaning up old validation reports..."

# Archive old validation reports
VALIDATION_COUNT=0
for file in validation/val_*.json; do
    if [ -f "$file" ]; then
        # Check age - if older than 7 days, archive
        if [ $(find "$file" -mtime +7 2>/dev/null | wc -l) -gt 0 ]; then
            mv "$file" archive/implemented/
            ((VALIDATION_COUNT++))
        fi
    fi
done

echo ""
echo "══════════════════════════════════════════════════"
echo "📊 CLEANUP SUMMARY"
echo "══════════════════════════════════════════════════"
echo "Archived implemented proposals: $IMPLEMENTED_COUNT"
echo "Archived staging directories: $STAGING_COUNT"
echo "Archived validation reports: $VALIDATION_COUNT"
echo ""

# Show new counts
echo "NEW COUNTS:"
echo "  Proposals (active): $(ls -1 proposals/proposal_*.json 2>/dev/null | wc -l)"
echo "  Staging (active): $(ls -1 staging/ 2>/dev/null | wc -l)"
echo "  Validation (active): $(ls -1 validation/val_*.json 2>/dev/null | wc -l)"
echo "  Archive (implemented): $(ls -1 archive/implemented/ 2>/dev/null | wc -l)"
echo ""

# Update the sync script to exclude archived proposals
echo "4. Updating sync script..."

sed -i '' 's|"{proposals_dir}/proposal_\*.json"|"{proposals_dir}/proposal_*.json" if not f.startswith("archive")|g' ~/.openclaw/workspace/sync-command-center.sh 2>/dev/null || true

echo ""
echo "✅ RSI workflow cleaned up!"
echo ""
echo "Next steps:"
echo "  - Only ACTIVE proposals will show in dashboard"
echo "  - Implemented proposals moved to archive"
echo "  - Warden needs fix to auto-archive on deploy"
