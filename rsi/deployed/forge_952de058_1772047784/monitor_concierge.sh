#!/bin/bash
# Monitor script - runs every 5 minutes via cron

if ! pgrep -f fred_pt_bot.py > /dev/null; then
    echo "$(date): Concierge Bot down, restarting..." >> /tmp/bot_monitor.log
    /Users/fredericklaw/.openclaw/workspace/rsi/staging/forge_952de058_1772047784/restart_concierge.sh
fi
