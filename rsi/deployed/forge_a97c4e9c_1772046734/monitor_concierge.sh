#!/bin/bash
# Monitor script - runs every 5 minutes via cron

if ! pgrep -f fred_pt_bot.py > /dev/null; then
    echo "$(date): Concierge Bot down, restarting..." >> /tmp/bot_monitor.log
    /Users/fredericklaw/.openclaw/workspace/rsi/staging/forge_a97c4e9c_1772046734/restart_concierge.sh
fi
