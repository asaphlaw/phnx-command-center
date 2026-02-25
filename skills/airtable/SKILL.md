---
name: airtable-cci
description: Airtable integration for the Command Control Interface. Connects to Fred's business database for revenue tracking, client management, and goal monitoring. Use when: (1) checking business metrics, (2) syncing deployment projects with business goals, (3) automating client/revenue workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "env": ["AIRTABLE_API_TOKEN"], "bins": ["python3"] },
      },
  }
---

# Airtable CCI Skill

Integration with Fred's Airtable business database.

## Base: appCsi3KNqXcNNfFC

### Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **PT Clients** | Personal training client management | Client Name, Status, Rate per Session, Sessions Remaining |
| **PT Revenue (P&L)** | Profit/loss tracking | Monthly breakdowns |
| **$200K Goal Tracker** | 2026 revenue goal tracking | Month, Target ($16,667), Actual Revenue, % to Target |
| **Exercise Library** | Training content catalog | Exercises, descriptions |
| **Corp Clients** | Corporate account rental clients | Client Name, Status, Monthly Revenue |
| **Payout Schedule** | Payment tracking | Dates, amounts, recipients |
| **Cash Position** | Financial overview | Current cash position |

## Business Context

### Revenue Streams
1. **Personal Training** - Primary income
   - 6 clients (4 active, 2 at risk, 1 inactive)
   - Rates: $80-90/session
   - ~$3,055 in booked sessions remaining
   
2. **Corporate Account Rental** - Side hustle
   - 3 active clients (Dart group)
   - $5,300 revenue in February 2026

### 2026 Goal
- **Target:** $200,000 net profit
- **Monthly target:** $16,667
- **Current status:** Behind (Feb at 31.8%)

## Scripts

### airtable_client.py
Main API client for interacting with Airtable.

**Usage:**
```bash
# Set token
export AIRTABLE_API_TOKEN="your_token"

# List tables
python3 scripts/airtable_client.py tables

# Get records from table
python3 scripts/airtable_client.py records "PT Clients" --max 20

# List accessible bases
python3 scripts/airtable_client.py bases
```

## Integration with CCI

Use this skill to:
1. Pull client data before building PT client portals
2. Check revenue status before deploying new offers
3. Track which projects will impact the $200K goal
4. Automate client follow-ups based on status

## Example Workflows

### Deploy Client Portal
```bash
# Get at-risk clients
python3 scripts/airtable_client.py records "PT Clients" --view "At Risk"

# Deploy retention landing page for them
cci.py deploy "Create a client retention page with special offer" --project pt-retention
```

### Revenue Dashboard
```bash
# Pull goal tracker data
python3 -c "
import os
os.environ['AIRTABLE_API_TOKEN'] = '...'
from scripts.airtable_client import AirtableClient
client = AirtableClient()
data = client.get_records('%24200K%20Goal%20Tracker')
print(json.dumps(data, indent=2))
"
```
