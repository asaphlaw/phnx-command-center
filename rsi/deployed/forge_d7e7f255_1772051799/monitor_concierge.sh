#!/bin/bash
# Monitor script - runs every 5 minutes via cron

if ! pgrep -f fred_pt_bot.py > /dev/null; then
    echo "$(date): Concierge Bot down, restarting..." >> /tmp/bot_monitor.log
    /Users/fredericklaw/.openclaw/workspace/rsi/staging/forge_d7e7f255_1772051799/restart_concierge.sh
fi
