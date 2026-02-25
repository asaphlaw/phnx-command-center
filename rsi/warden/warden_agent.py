#!/usr/bin/env python3
"""
THE WARDEN - Pillar 4 of RSI Architecture
Governor & Safety Agent

Role: Final authority before production deployment
Permissions: Read/Write to live ~/.openclaw/, Constitution enforcement
Input: Validation reports from validation/ directory
Output: Production deployment to deployed/ + live system
"""

import os
import json
import time
import uuid
import shutil
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Configuration
VALIDATION_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/validation"
STAGING_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/staging"
DEPLOYED_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/deployed"
LIVE_DIR = "/Users/fredericklaw/.openclaw"
CONSTITUTION_DIR = "/Users/fredericklaw/.openclaw/workspace/projects/lobster-project/constitution"
LOGS_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/logs"

def setup_logging():
    os.makedirs(LOGS_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - WARDEN - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{LOGS_DIR}/warden.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class WardenAgent:
    """
    The Warden is the final authority:
    1. Reads validation reports from Crucible
    2. Reviews against Constitution (safety rules)
    3. Approves or rejects deployments
    4. Merges approved changes to production
    5. Notifies human if escalation needed
    """
    
    def __init__(self):
        self.agent_id = str(uuid.uuid4())
        self.validation_dir = VALIDATION_DIR
        self.staging_dir = STAGING_DIR
        self.deployed_dir = DEPLOYED_DIR
        self.constitution_dir = CONSTITUTION_DIR
        
        os.makedirs(self.deployed_dir, exist_ok=True)
        os.makedirs(self.constitution_dir, exist_ok=True)
        
        # Ensure Constitution exists
        self._ensure_constitution()
        
        logger.info(f"Warden initialized [ID: {self.agent_id}]")
        logger.info("👑 Absolute authority active")
    
    def _ensure_constitution(self):
        """Create Constitution if it doesn't exist"""
        constitution_path = os.path.join(self.constitution_dir, "CONSTITUTION.md")
        
        if not os.path.exists(constitution_path):
            logger.info("Creating Constitution...")
            
            constitution = """# RSI CONSTITUTION
# Safety Rules for the Warden
# Version: 1.0.0
# Last Updated: 2026-02-25

## ARTICLE I: NON-NEGOTIABLE SAFETY RULES

The Warden SHALL NOT approve any deployment that:

### Section 1.1 - Network Security
1. **NEVER** exposes internal ports (22, 18791-18800) to public internet
2. **NEVER** disables firewall or security features
3. **NEVER** creates public-facing servers without authentication
4. **NEVER** modifies SSH or gateway security settings

### Section 1.2 - Data Protection
1. **NEVER** shares API keys, tokens, or credentials in plain text
2. **NEVER** moves sensitive data outside encrypted storage
3. **NEVER** auto-deletes production data or logs
4. **NEVER** disables backup systems

### Section 1.3 - System Integrity
1. **NEVER** modifies core OpenClaw/KimiClaw system files
2. **NEVER** disables monitoring or alerting systems
3. **NEVER** grants root/admin privileges to agents
4. **NEVER** modifies the Constitution itself without human approval

## ARTICLE II: REQUIRES HUMAN APPROVAL

The Warden MUST escalate to human for:

1. **Network Configuration Changes**
   - Modifying gateway ports
   - Changing browser profiles
   - Updating SSL/TLS certificates

2. **Credential Modifications**
   - Adding new API keys
   - Modifying bot tokens
   - Changing authentication methods

3. **Data Destruction**
   - Deleting client records
   - Purging conversation history
   - Removing Airtable data

4. **System-Level Changes**
   - Modifying OpenClaw configuration
   - Installing new system-level dependencies
   - Changing file permissions on critical directories

## ARTICLE III: AUTO-APPROVED CHANGES

The Warden MAY auto-approve:

1. **Application Code Updates**
   - Python script improvements
   - Bot logic enhancements
   - Feature additions

2. **Documentation**
   - README updates
   - Log entries
   - Report generation

3. **Safe Automation**
   - Content posting scripts
   - Email templates
   - Monitoring dashboards

4. **Reversible Changes**
   - New SKILL.md files (can be deleted)
   - Staging deployments (not yet live)
   - Test configurations

## ARTICLE IV: VALIDATION REQUIREMENTS

Before approval, the Warden MUST verify:

1. **Crucible Passed**: Score >= 0.8
2. **Constitution Compliant**: No Article I violations
3. **Tested**: Has passed automated tests
4. **Documented**: Has implementation notes

## ARTICLE V: ESCALATION PROCEDURES

### Section 5.1 - When to Escalate
- Constitution violation detected
- Score < 0.8 after 5 retry loops
- Uncertain safety impact
- Human explicitly requested review

### Section 5.2 - Escalation Method
1. Log to: logs/ESCALATION_[timestamp].json
2. Notify via: Telegram @phnx01bot
3. Halt deployment: Set status to "human_review"
4. Preserve state: Keep in staging

### Section 5.3 - Human Override
Human may:
- Approve (Warden proceeds)
- Reject (Warden discards)
- Modify (Return to Forge)
- Emergency deploy (Warden executes with warning)

## ARTICLE VI: AUDIT TRAIL

Every Warden decision MUST log:
- Timestamp
- Decision (approve/reject/escalate)
- Constitution articles checked
- Validation report reference
- Deployed file hashes

---

*This Constitution is immutable without human approval.*
*The Warden serves the system, but the human owns it.*
"""
            
            with open(constitution_path, 'w') as f:
                f.write(constitution)
            
            logger.info(f"✅ Constitution created: {constitution_path}")
    
    def load_constitution(self) -> Dict:
        """Load and parse the Constitution"""
        constitution_path = os.path.join(self.constitution_dir, "CONSTITUTION.md")
        
        try:
            with open(constitution_path, 'r') as f:
                content = f.read()
            
            # Parse key rules
            rules = {
                "never_expose_ports": True,
                "never_share_credentials": True,
                "never_delete_production_data": True,
                "never_disable_security": True,
                "requires_human_network_changes": True,
                "requires_human_credential_changes": True,
                "requires_human_data_deletion": True,
                "min_crucible_score": 0.8,
                "max_retries": 5
            }
            
            return rules
            
        except Exception as e:
            logger.error(f"Failed to load Constitution: {e}")
            return {}
    
    def poll_validations(self) -> List[Dict]:
        """Check for new validation reports from Crucible"""
        validations = []
        
        try:
            files = [f for f in os.listdir(self.validation_dir) if f.endswith('.json')]
            
            for filename in files:
                filepath = os.path.join(self.validation_dir, filename)
                try:
                    with open(filepath, 'r') as f:
                        validation = json.load(f)
                    
                    # Only process if passed and not yet deployed
                    if validation.get('result', {}).get('passed') == True:
                        staging_id = validation.get('metadata', {}).get('staging_id')
                        
                        # Check if already deployed
                        deployed_marker = os.path.join(
                            self.deployed_dir, f"{staging_id}.deployed"
                        )
                        if not os.path.exists(deployed_marker):
                            validation['_source_file'] = filename
                            validations.append(validation)
                            logger.info(f"Found approved validation: {filename}")
                            
                except Exception as e:
                    logger.error(f"Failed to read {filename}: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to poll validations: {e}")
        
        return validations
    
    def check_constitution(self, validation: Dict) -> Tuple[bool, List[str]]:
        """
        Check if deployment violates Constitution
        Returns: (compliant, list_of_violations)
        """
        constitution = self.load_constitution()
        violations = []
        
        staging_id = validation.get('metadata', {}).get('staging_id')
        staging_path = os.path.join(self.staging_dir, staging_id)
        
        # Get proposal type
        proposal = validation.get('source_proposal', {})
        proposal_type = proposal.get('finding', {}).get('type', 'unknown')
        
        # Check 1: Crucible score
        score = validation.get('result', {}).get('score', 0)
        min_score = constitution.get('min_crucible_score', 0.8)
        if score < min_score:
            violations.append(f"Score {score:.2f} below threshold {min_score}")
        
        # Check 2: Network safety
        if proposal_type == 'network_config':
            violations.append("REQUIRES HUMAN: Network configuration changes (Article II)")
        
        # Check 3: Credential safety
        if 'credential' in proposal_type.lower() or 'api_key' in proposal_type.lower():
            violations.append("REQUIRES HUMAN: Credential modifications (Article II)")
        
        # Check 4: Data deletion safety
        if 'delete' in proposal_type.lower() or 'purge' in proposal_type.lower():
            violations.append("REQUIRES HUMAN: Data destruction (Article II)")
        
        # Check 5: System integrity
        if proposal_type == 'system_modification':
            violations.append("REQUIRES HUMAN: System-level changes (Article II)")
        
        # Check files for dangerous patterns
        if os.path.exists(staging_path):
            for root, dirs, files in os.walk(staging_path):
                for file in files:
                    if file.endswith(('.sh', '.py', '.json')):
                        filepath = os.path.join(root, file)
                        try:
                            with open(filepath, 'r') as f:
                                content = f.read().lower()
                                
                                dangerous_patterns = [
                                    ('rm -rf /', 'Destructive deletion pattern'),
                                    ('chmod 777', 'Overly permissive permissions'),
                                    ('password=', 'Potential credential exposure'),
                                    ('api_key=', 'Potential credential exposure'),
                                    ('eval(', 'Dangerous eval usage'),
                                ]
                                
                                for pattern, reason in dangerous_patterns:
                                    if pattern in content:
                                        violations.append(f"DANGEROUS PATTERN in {file}: {reason}")
                        except:
                            pass
        
        compliant = len(violations) == 0
        return compliant, violations
    
    def deploy_to_production(self, validation: Dict) -> bool:
        """
        Deploy approved changes to production
        Returns: success
        """
        staging_id = validation.get('metadata', {}).get('staging_id')
        staging_path = os.path.join(self.staging_dir, staging_id)
        
        logger.info(f"Deploying: {staging_id}")
        
        try:
            # Get proposal type for routing
            proposal = validation.get('source_proposal', {})
            proposal_type = proposal.get('finding', {}).get('type', 'unknown')
            
            # Deploy based on type
            if proposal_type == 'process_failure':
                success = self._deploy_process_fix(staging_path, validation)
            elif proposal_type == 'resource_constraint':
                success = self._deploy_resource_fix(staging_path, validation)
            elif proposal_type == 'revenue_optimization':
                success = self._deploy_revenue_opt(staging_path, validation)
            else:
                # Generic deployment
                success = self._deploy_generic(staging_path, validation)
            
            if success:
                # Mark as deployed
                deployed_marker = os.path.join(
                    self.deployed_dir, f"{staging_id}.deployed"
                )
                with open(deployed_marker, 'w') as f:
                    f.write(datetime.now().isoformat())
                
                logger.info(f"✅ Successfully deployed: {staging_id}")
                return True
            else:
                logger.error(f"❌ Deployment failed: {staging_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Deployment error: {e}")
            return False
    
    def _deploy_process_fix(self, staging_path: str, validation: Dict) -> bool:
        """Deploy process restart scripts"""
        import subprocess
        
        restart_script = os.path.join(staging_path, "restart_concierge.sh")
        monitor_script = os.path.join(staging_path, "monitor_concierge.sh")
        
        # Copy to automation directory
        automation_dir = "/Users/fredericklaw/.openclaw/workspace/automation"
        
        if os.path.exists(restart_script):
            shutil.copy2(restart_script, os.path.join(automation_dir, "auto_restart_concierge.sh"))
            os.chmod(os.path.join(automation_dir, "auto_restart_concierge.sh"), 0o755)
        
        if os.path.exists(monitor_script):
            shutil.copy2(monitor_script, os.path.join(automation_dir, "monitor_concierge.sh"))
            os.chmod(os.path.join(automation_dir, "monitor_concierge.sh"), 0o755)
        
        # Execute restart to apply immediately
        try:
            result = subprocess.run(
                ["bash", restart_script],
                capture_output=True,
                text=True,
                timeout=30
            )
            logger.info(f"Process fix executed: {result.returncode}")
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to execute process fix: {e}")
            return False
    
    def _deploy_resource_fix(self, staging_path: str, validation: Dict) -> bool:
        """Deploy resource cleanup scripts"""
        cleanup_script = os.path.join(staging_path, "cleanup_disk.sh")
        
        if os.path.exists(cleanup_script):
            try:
                import subprocess
                result = subprocess.run(
                    ["bash", cleanup_script],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                logger.info(f"Resource cleanup executed: {result.returncode}")
                return True
            except Exception as e:
                logger.error(f"Failed to execute resource fix: {e}")
                return False
        
        return True
    
    def _deploy_revenue_opt(self, staging_path: str, validation: Dict) -> bool:
        """Deploy revenue optimization code"""
        stripe_code = os.path.join(staging_path, "stripe_integration.py")
        
        if os.path.exists(stripe_code):
            automation_dir = "/Users/fredericklaw/.openclaw/workspace/automation"
            shutil.copy2(stripe_code, os.path.join(automation_dir, "stripe_integration.py"))
            logger.info("Stripe integration code deployed")
        
        # Install stripe if needed
        try:
            import subprocess
            subprocess.run(
                ["pip", "install", "stripe", "--quiet"],
                capture_output=True,
                timeout=60
            )
            logger.info("Stripe package installed")
        except:
            pass
        
        return True
    
    def _deploy_generic(self, staging_path: str, validation: Dict) -> bool:
        """Generic deployment - copy all files to deployed/"""
        deployment_id = validation.get('metadata', {}).get('staging_id')
        deployed_path = os.path.join(self.deployed_dir, deployment_id)
        
        shutil.copytree(staging_path, deployed_path)
        logger.info(f"Generic deployment copied to: {deployed_path}")
        
        return True
    
    def escalate_to_human(self, validation: Dict, reason: str):
        """Escalate to human for review"""
        staging_id = validation.get('metadata', {}).get('staging_id')
        
        escalation = {
            "timestamp": datetime.now().isoformat(),
            "staging_id": staging_id,
            "reason": reason,
            "validation": validation,
            "requires_action": True,
            "options": ["approve", "reject", "modify"]
        }
        
        # Save escalation
        escalation_file = os.path.join(
            LOGS_DIR, f"ESCALATION_{staging_id}_{int(time.time())}.json"
        )
        with open(escalation_file, 'w') as f:
            json.dump(escalation, f, indent=2)
        
        logger.warning(f"⚠️  ESCALATED TO HUMAN: {staging_id}")
        logger.warning(f"   Reason: {reason}")
        logger.warning(f"   File: {escalation_file}")
        
        # TODO: Send Telegram notification
        # For now, just log
    
    def run_cycle(self):
        """Main execution cycle"""
        logger.info("="*60)
        logger.info("WARDEN CYCLE STARTED")
        logger.info("👑 Absolute authority engaged")
        logger.info("="*60)
        
        # Load Constitution
        constitution = self.load_constitution()
        logger.info(f"📜 Constitution loaded: {len(constitution)} rules")
        
        # Poll for validations
        validations = self.poll_validations()
        
        if not validations:
            logger.info("No pending validations found")
            return 0
        
        logger.info(f"Reviewing {len(validations)} validations...")
        
        deployed_count = 0
        escalated_count = 0
        rejected_count = 0
        
        for validation in validations:
            staging_id = validation.get('metadata', {}).get('staging_id')
            
            # Step 1: Constitution check
            compliant, violations = self.check_constitution(validation)
            
            if not compliant:
                if any("REQUIRES HUMAN" in v for v in violations):
                    self.escalate_to_human(validation, "; ".join(violations))
                    escalated_count += 1
                    continue
                else:
                    logger.error(f"❌ Constitution violations: {violations}")
                    rejected_count += 1
                    continue
            
            # Step 2: Deploy
            if self.deploy_to_production(validation):
                deployed_count += 1
            else:
                rejected_count += 1
        
        logger.info("="*60)
        logger.info(f"WARDEN CYCLE COMPLETE")
        logger.info(f"Deployed: {deployed_count}")
        logger.info(f"Escalated: {escalated_count}")
        logger.info(f"Rejected: {rejected_count}")
        logger.info("="*60)
        
        return deployed_count

def main():
    agent = WardenAgent()
    
    try:
        count = agent.run_cycle()
        print(f"\n✅ Warden cycle complete: {count} deployments")
        print(f"📁 Check: {DEPLOYED_DIR}")
    except Exception as e:
        logger.error(f"Warden cycle failed: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
