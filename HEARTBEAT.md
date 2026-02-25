# HEARTBEAT.md - RSI System Trigger

This file triggers the 4-Pillar RSI Architecture on a scheduled loop.

## INSTRUCTIONS

**Every 60 minutes, execute:**

```bash
cd /Users/fredericklaw/.openclaw/workspace/rsi
python3 orchestrate.py --full-cycle
```

## THE 4 PILLARS

1. **FORAGER** → Discovers improvements → Saves to `proposals/`
2. **FORGE** → Implements proposals → Saves to `staging/`
3. **CRUCIBLE** → Validates changes → Saves to `validation/`
4. **WARDEN** → Deploys approved changes → Updates live system

## SAFETY

- Max 10 proposals per cycle
- Max 3 deployments per hour
- Auto-halt on Constitution violations
- Human escalation after 5 failed retries

## MANUAL COMMANDS

```bash
# Check status
python3 orchestrate.py --status

# Run individual pillars
python3 orchestrate.py --forager
python3 orchestrate.py --forge
python3 orchestrate.py --crucible
python3 orchestrate.py --warden

# Halt/Resume
python3 orchestrate.py --halt
python3 orchestrate.py --resume
```

*RSI Version: 1.0.0 | Activated: 2026-02-26*
