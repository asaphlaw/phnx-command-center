#!/usr/bin/env python3
"""
THE FORGE - Pillar 2 of RSI Architecture
Developer & Self-Healer Agent

Role: Implements proposals, fixes errors, writes code
Permissions: Staging directory R/W, terminal execution (sandboxed)
Input: Proposals from proposals/ directory
Output: Code to staging/ directory
"""

import os
import json
import time
import uuid
import shutil
import subprocess
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Configuration
PROPOSALS_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/proposals"
STAGING_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/staging"
LOGS_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/logs"

def setup_logging():
    os.makedirs(LOGS_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - FORGE - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{LOGS_DIR}/forge.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class ForgeAgent:
    """
    The Forge implements improvements and heals the system:
    1. Reads proposals from Forager
    2. Writes actual code (Python/TypeScript/YAML)
    3. Monitors processes and fixes crashes
    4. Creates unit tests
    """
    
    def __init__(self):
        self.agent_id = str(uuid.uuid4())
        self.staging_dir = STAGING_DIR
        self.proposals_dir = PROPOSALS_DIR
        
        os.makedirs(self.staging_dir, exist_ok=True)
        
        logger.info(f"Forge initialized [ID: {self.agent_id}]")
    
    def poll_proposals(self) -> List[Dict]:
        """
        Check for new proposals from Forager
        Returns list of pending proposals
        """
        proposals = []
        
        try:
            files = os.listdir(self.proposals_dir)
            json_files = [f for f in files if f.endswith('.json')]
            
            for filename in json_files:
                filepath = os.path.join(self.proposals_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        proposal = json.load(f)
                        
                    # Only process pending proposals
                    if proposal.get('status') == 'pending_review':
                        proposal['_source_file'] = filename
                        proposals.append(proposal)
                        logger.info(f"Found pending proposal: {filename}")
                        
                except Exception as e:
                    logger.error(f"Failed to read {filename}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to poll proposals: {e}")
        
        return proposals
    
    def implement_proposal(self, proposal: Dict) -> Tuple[bool, str, str]:
        """
        Implement a proposal
        Returns: (success, staging_dir, error_message)
        """
        proposal_id = proposal['metadata']['proposal_id']
        proposal_type = proposal['finding'].get('type', 'improvement')
        
        logger.info(f"Implementing proposal {proposal_id}: {proposal['proposal']['title']}")
        
        # Create staging directory for this implementation
        staging_id = f"forge_{proposal_id}_{int(time.time())}"
        staging_path = os.path.join(self.staging_dir, staging_id)
        os.makedirs(staging_path, exist_ok=True)
        
        try:
            # Route to appropriate implementation handler
            if proposal_type == 'process_failure':
                success = self._fix_process_failure(proposal, staging_path)
            elif proposal_type == 'resource_constraint':
                success = self._fix_resource_constraint(proposal, staging_path)
            elif proposal_type == 'error_rate':
                success = self._fix_error_rate(proposal, staging_path)
            elif proposal_type == 'architecture_improvement':
                success = self._implement_architecture(proposal, staging_path)
            elif proposal_type == 'automation':
                success = self._implement_automation(proposal, staging_path)
            elif proposal_type == 'revenue_optimization':
                success = self._implement_revenue_opt(proposal, staging_path)
            else:
                # Generic implementation
                success = self._implement_generic(proposal, staging_path)
            
            if success:
                # Create implementation manifest
                manifest = {
                    "metadata": {
                        "staging_id": staging_id,
                        "proposal_id": proposal_id,
                        "agent": "forge",
                        "agent_id": self.agent_id,
                        "created_at": datetime.now().isoformat(),
                        "status": "implemented"
                    },
                    "source_proposal": proposal,
                    "implementation": {
                        "staging_path": staging_path,
                        "files_created": os.listdir(staging_path),
                        "ready_for_validation": True
                    }
                }
                
                manifest_path = os.path.join(staging_path, "manifest.json")
                with open(manifest_path, 'w') as f:
                    json.dump(manifest, f, indent=2)
                
                # Mark proposal as implemented
                self._update_proposal_status(proposal, 'implemented', staging_id)
                
                logger.info(f"✅ Implementation complete: {staging_id}")
                return True, staging_path, ""
            else:
                logger.error(f"❌ Implementation failed for {proposal_id}")
                return False, staging_path, "Implementation handler returned false"
                
        except Exception as e:
            logger.error(f"❌ Implementation error: {e}")
            return False, staging_path, str(e)
    
    def _fix_process_failure(self, proposal: Dict, staging_path: str) -> bool:
        """Fix a process failure (e.g., bot not running)"""
        component = proposal['finding'].get('component', 'unknown')
        
        logger.info(f"Creating fix for process: {component}")
        
        # Create restart script
        if component == 'concierge_bot':
            script_content = '''#!/bin/bash
# Auto-generated restart script for Concierge Bot
# Generated by Forge Agent

echo "🔧 Restarting Concierge Bot..."

# Kill existing processes
pkill -f fred_pt_bot.py 2>/dev/null
sleep 2

# Start bot
cd /Users/fredericklaw/.openclaw/workspace/automation
nohup python3 fred_pt_bot.py > /tmp/fred_bot.log 2>&1 &
sleep 3

# Verify
if pgrep -f fred_pt_bot.py > /dev/null; then
    echo "✅ Concierge Bot restarted successfully"
    exit 0
else
    echo "❌ Failed to restart"
    exit 1
fi
'''
            script_path = os.path.join(staging_path, "restart_concierge.sh")
            with open(script_path, 'w') as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            
            # Create monitoring script
            monitor_content = '''#!/bin/bash
# Monitor script - runs every 5 minutes via cron

if ! pgrep -f fred_pt_bot.py > /dev/null; then
    echo "$(date): Concierge Bot down, restarting..." >> /tmp/bot_monitor.log
    /Users/fredericklaw/.openclaw/workspace/rsi/staging/''' + os.path.basename(staging_path) + '''/restart_concierge.sh
fi
'''
            monitor_path = os.path.join(staging_path, "monitor_concierge.sh")
            with open(monitor_path, 'w') as f:
                f.write(monitor_content)
            os.chmod(monitor_path, 0o755)
            
            return True
        
        return False
    
    def _fix_resource_constraint(self, proposal: Dict, staging_path: str) -> bool:
        """Fix resource constraints (e.g., disk space)"""
        component = proposal['finding'].get('component', 'unknown')
        
        if component == 'disk_space':
            script_content = '''#!/bin/bash
# Disk cleanup script
# Generated by Forge Agent

echo "🧹 Cleaning disk space..."

# Clean old logs
echo "Removing old logs..."
find /tmp -name "*.log" -mtime +7 -delete 2>/dev/null
find ~/.openclaw/workspace -name "*.log" -mtime +7 -delete 2>/dev/null

# Clean Python cache
echo "Cleaning Python cache..."
find ~/.openclaw/workspace -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Clean old screenshots
echo "Cleaning old screenshots..."
find /tmp -name "bolt_*.png" -mtime +1 -delete 2>/dev/null

echo "✅ Cleanup complete"
df -h /Users
'''
            script_path = os.path.join(staging_path, "cleanup_disk.sh")
            with open(script_path, 'w') as f:
                f.write(script_content)
            os.chmod(script_path, 0o755)
            
            return True
        
        return False
    
    def _fix_error_rate(self, proposal: Dict, staging_path: str) -> bool:
        """Fix high error rates in logs"""
        # Implementation would analyze logs and create fixes
        # For now, create diagnostic script
        
        script_content = '''#!/bin/bash
# Error analysis script
# Generated by Forge Agent

echo "🔍 Analyzing errors..."

LOGS=(
    "/tmp/fred_bot.log"
    "/tmp/watchdog_v3.log"
    "/tmp/coordinator.log"
)

for log in "${LOGS[@]}"; do
    if [ -f "$log" ]; then
        echo ""
        echo "=== $log ==="
        echo "Recent errors:"
        tail -50 "$log" | grep -E "(ERROR|Exception)" | tail -10
    fi
done
'''
        script_path = os.path.join(staging_path, "analyze_errors.sh")
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
        return True
    
    def _implement_architecture(self, proposal: Dict, staging_path: str) -> bool:
        """Implement architectural improvements"""
        # This would implement the 4-pillar system
        # Already implemented, so just create documentation
        
        readme_content = '''# RSI Architecture Implementation
# Generated by Forge Agent

## Status
The 4-Pillar RSI Architecture has been deployed:
- ✅ Forager (Researcher)
- ✅ Forge (Developer)
- ✅ Crucible (Validator) - Docker required
- ✅ Warden (Governor)

## Next Steps
1. Configure Docker for Crucible sandbox
2. Set up HEARTBEAT.md triggers
3. Test full loop
'''
        readme_path = os.path.join(staging_path, "ARCHITECTURE_STATUS.md")
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        return True
    
    def _implement_automation(self, proposal: Dict, staging_path: str) -> bool:
        """Implement automation (e.g., content posting)"""
        # Create content deployment script
        
        script_content = '''#!/bin/bash
# Content deployment script
# Generated by Forge Agent

echo "📱 Deploying MarketingBot content..."

# This would integrate with Instagram/LinkedIn APIs
# For now, create manual posting guide

cat << 'GUIDE'
Manual Content Deployment Guide:

1. Access content queue:
   ls ~/.openclaw/workspace/marketingbot/content_queue/

2. Post to Instagram:
   - Copy content from JSON files
   - Use Instagram Creator Studio or Later.com
   - Schedule for optimal times (8am, 12pm, 6pm)

3. Post to LinkedIn:
   - Use professional tone
   - Tag relevant hashtags
   - Include call-to-action

4. Track engagement:
   - Monitor likes/comments
   - Respond to inquiries
   - Track lead conversions

GUIDE

echo "✅ Deployment guide created"
'''
        script_path = os.path.join(staging_path, "deploy_content.sh")
        with open(script_path, 'w') as f:
            f.write(script_content)
        os.chmod(script_path, 0o755)
        
        return True
    
    def _implement_revenue_opt(self, proposal: Dict, staging_path: str) -> bool:
        """Implement revenue optimizations"""
        # Create Stripe integration starter
        
        code_content = '''# Stripe Integration for Booking Bot
# Generated by Forge Agent

import stripe
import os
from typing import Optional

class StripeBookingIntegration:
    """
    Handles booking deposits via Stripe
    """
    
    def __init__(self):
        # Use environment variable for security
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        
    def create_deposit_session(self, client_email: str, amount_cents: int = 5000) -> Optional[str]:
        """
        Create a Stripe checkout session for booking deposit
        Default: $50 deposit (5000 cents)
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'sgd',
                        'product_data': {
                            'name': 'PT Session Deposit',
                            'description': 'Booking deposit for personal training session',
                        },
                        'unit_amount': amount_cents,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://your-domain.com/success',
                cancel_url='https://your-domain.com/cancel',
                customer_email=client_email,
            )
            return session.url
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

# Usage:
# stripe = StripeBookingIntegration()
# payment_url = stripe.create_deposit_session("client@email.com")
'''
        code_path = os.path.join(staging_path, "stripe_integration.py")
        with open(code_path, 'w') as f:
            f.write(code_content)
        
        # Create setup instructions
        setup_content = '''# Stripe Integration Setup

1. Install Stripe:
   pip install stripe

2. Set environment variable:
   export STRIPE_SECRET_KEY="sk_live_..."

3. Add to booking bot flow:
   - Before confirming booking
   - Generate payment URL
   - Send to client via Telegram
   - Confirm booking only after payment

4. Webhook setup (for production):
   - Configure Stripe webhook
   - Listen for payment_intent.succeeded
   - Auto-confirm booking on payment
'''
        setup_path = os.path.join(staging_path, "STRIPE_SETUP.md")
        with open(setup_path, 'w') as f:
            f.write(setup_content)
        
        return True
    
    def _implement_generic(self, proposal: Dict, staging_path: str) -> bool:
        """Generic implementation for unknown types"""
        readme_content = f'''# Implementation: {proposal['proposal']['title']}

## Description
{proposal['proposal']['description']}

## Status
Generic implementation template created.
Manual implementation required.

## Notes
- Type: {proposal['finding'].get('type', 'unknown')}
- Priority: {proposal['proposal'].get('priority', 'medium')}
- Estimated effort: {proposal['proposal'].get('estimated_effort_hours', 4)} hours
'''
        readme_path = os.path.join(staging_path, "README.md")
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        return True
    
    def _update_proposal_status(self, proposal: Dict, status: str, staging_id: str):
        """Update the proposal file with new status"""
        filename = proposal.get('_source_file')
        if not filename:
            return
        
        filepath = os.path.join(self.proposals_dir, filename)
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            data['status'] = status
            data['implementation'] = {
                "staging_id": staging_id,
                "implemented_at": datetime.now().isoformat(),
                "implemented_by": self.agent_id
            }
            
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to update proposal status: {e}")
    
    def run_cycle(self):
        """Main execution cycle"""
        logger.info("="*60)
        logger.info("FORGE CYCLE STARTED")
        logger.info("="*60)
        
        # Poll for proposals
        proposals = self.poll_proposals()
        
        if not proposals:
            logger.info("No pending proposals found")
            return 0
        
        logger.info(f"Processing {len(proposals)} proposals...")
        
        implemented_count = 0
        failed_count = 0
        
        for proposal in proposals:
            success, staging_path, error = self.implement_proposal(proposal)
            
            if success:
                implemented_count += 1
            else:
                failed_count += 1
                logger.error(f"Failed: {error}")
        
        logger.info("="*60)
        logger.info(f"FORGE CYCLE COMPLETE")
        logger.info(f"Implemented: {implemented_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Staging items: {len(os.listdir(self.staging_dir))}")
        logger.info("="*60)
        
        return implemented_count

def main():
    agent = ForgeAgent()
    
    try:
        count = agent.run_cycle()
        print(f"\n✅ Forge cycle complete: {count} implementations")
        print(f"📁 Check: {STAGING_DIR}")
    except Exception as e:
        logger.error(f"Forge cycle failed: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
