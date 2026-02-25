# 4-Pillar RSI Architecture
# Recursive Self-Improving Agent Swarm
# Version: 1.0.0
# Date: 2026-02-25

## Overview

A self-improving, self-healing multi-agent system designed for continuous optimization of the PHNX Command Center.

## The Four Pillars

### 1. THE FORAGER (Researcher & Innovator)
**Role:** Discovers improvements and optimizations
**Permissions:**
- Web search access
- GitHub API read
- ArXiv API read
- ClawHub skill registry read
- Read-only access to system logs

**Loop:**
- Runs every 60 minutes via heartbeat
- Searches for: optimization techniques, new skills, prompt engineering frameworks
- Drafts proposals as SKILL.md files
- Passes to Forge via `proposals/` directory

**Output:** `proposals/forager_[timestamp].md`

---

### 2. THE FORGE (Developer & Self-Healer)
**Role:** Implements improvements and fixes errors
**Permissions:**
- Read/Write to `staging/` directory
- Terminal execution (sandboxed)
- Read stack traces and logs
- Write SKILL.md files

**Functions:**
- **Improving:** Takes Forager proposals, writes code (Python/TS/YAML)
- **Healing:** Monitors processes, diagnoses crashes, writes patches
- **Testing:** Creates unit tests for new code

**Output:** `staging/forge_[timestamp]/`

---

### 3. THE CRUCIBLE (Sandbox & Verifier)
**Role:** Validates all changes before production
**Permissions:**
- Docker container execution only
- No internet access (isolated)
- Read-only from `staging/`

**Process:**
1. Receives code from Forge
2. Runs in isolated Docker container
3. Executes automated tests
4. LLM-as-judge evaluation (0.0-1.0 score)
5. **If score < 0.8:** Return to Forge with logs
6. **If score >= 0.8:** Pass to Warden

**Safety:** Maximum 5 retry loops, then escalate to human

**Output:** `validation/reports/[timestamp].json`

---

### 4. THE WARDEN (Governor & Safety)
**Role:** Final authority before production deployment
**Permissions:**
- Read/Write to live `~/.openclaw/`
- Read Constitution (safety rules)
- Merge approved changes
- Human notification (Telegram/WhatsApp)

**Safety Rules (Constitution):**
1. Never expose internal ports publicly
2. Never share API keys outside encrypted storage
3. Never auto-delete production data
4. Never disable security features
5. All changes must pass Crucible validation

**Process:**
1. Reviews Crucible validation report
2. Checks against Constitution
3. **If approved:** Merges to production
4. **If rejected:** Logs reason, notifies human
5. **If 5 retries exhausted:** Halts, notifies human

**Output:** Production deployment + audit log

---

## Communication Protocol

### File-Based State Machine
```
proposals/          → Forager outputs
staging/            → Forge work directory
validation/         → Crucible test results
deployed/           → Warden production merges
logs/               → Audit trail for all decisions
```

### Agent Handoff Format
```json
{
  "from": "forager",
  "to": "forge",
  "type": "proposal",
  "priority": "high",
  "proposal_id": "uuid",
  "created_at": "iso_timestamp",
  "content": "..."
}
```

## Heartbeat Loop

**Trigger:** Every 60 minutes via HEARTBEAT.md

**Sequence:**
1. HEARTBEAT → Trigger Forager
2. Forager → Search → Proposal → Save to proposals/
3. [Async] Forge polls proposals/, implements
4. Forge → Code → Save to staging/
5. [Async] Crucible polls staging/, validates
6. Crucible → Report → Save to validation/
7. [Async] Warden polls validation/, reviews
8. Warden → Deploy OR Reject
9. Loop continues

## Safety Mechanisms

### Circuit Breakers
- Max 5 retry loops per proposal
- Max 3 deployments per hour
- Auto-halt on Constitution violation
- Human approval required for:
  - Network config changes
  - Credential modifications
  - Data deletion operations

### Audit Trail
Every action logged to `logs/rsi_audit_[date].jsonl`:
- Timestamp
- Agent name
- Action type
- Input hash
- Output hash
- Success/failure
- Duration

## Implementation Status

- [ ] Pillar 1: Forager agent configured
- [ ] Pillar 2: Forge agent configured
- [ ] Pillar 3: Crucible sandbox configured
- [ ] Pillar 4: Warden governor configured
- [ ] HEARTBEAT.md updated with trigger
- [ ] Constitution (safety rules) defined
- [ ] Communication directories created
- [ ] Docker isolation for Crucible
- [ ] Telegram/WhatsApp alert system
- [ ] Audit logging enabled

## Next Steps

See IMPLEMENTATION_GUIDE.md for setup instructions.
