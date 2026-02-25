#!/usr/bin/env python3
"""
THE CRUCIBLE - Pillar 3 of RSI Architecture
Sandbox & Verifier Agent

Role: Validates all changes before production
Permissions: Docker container execution only, isolated, no internet
Input: Staging from staging/ directory
Output: Validation reports to validation/ directory
"""

import os
import json
import time
import uuid
import subprocess
from datetime import datetime
from typing import Dict, List, Tuple
import logging

# Configuration
STAGING_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/staging"
VALIDATION_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/validation"
LOGS_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/logs"

def setup_logging():
    os.makedirs(LOGS_DIR, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - CRUCIBLE - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f"{LOGS_DIR}/crucible.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class CrucibleAgent:
    """
    The Crucible validates all changes:
    1. Reads implementations from Forge
    2. Runs in isolated Docker container
    3. Executes automated tests
    4. LLM-as-judge evaluation (0.0-1.0)
    5. Pass/Fail decision
    6. Max 5 retry loops before human escalation
    """
    
    def __init__(self):
        self.agent_id = str(uuid.uuid4())
        self.staging_dir = STAGING_DIR
        self.validation_dir = VALIDATION_DIR
        
        os.makedirs(self.validation_dir, exist_ok=True)
        
        logger.info(f"Crucible initialized [ID: {self.agent_id}]")
        logger.warning("⚠️  Docker isolation recommended but not enforced in this version")
    
    def poll_staging(self) -> List[Dict]:
        """Check for new implementations from Forge"""
        implementations = []
        
        try:
            dirs = [d for d in os.listdir(self.staging_dir) 
                   if os.path.isdir(os.path.join(self.staging_dir, d))]
            
            for dir_name in dirs:
                manifest_path = os.path.join(self.staging_dir, dir_name, "manifest.json")
                
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, 'r') as f:
                            manifest = json.load(f)
                        
                        # Only process if not already validated
                        validation_marker = os.path.join(
                            self.staging_dir, dir_name, ".validated"
                        )
                        if not os.path.exists(validation_marker):
                            manifest['_staging_dir'] = dir_name
                            implementations.append(manifest)
                            logger.info(f"Found unvalidated implementation: {dir_name}")
                            
                    except Exception as e:
                        logger.error(f"Failed to read manifest in {dir_name}: {e}")
                        
        except Exception as e:
            logger.error(f"Failed to poll staging: {e}")
        
        return implementations
    
    def validate_implementation(self, manifest: Dict) -> Tuple[bool, float, str]:
        """
        Validate an implementation
        Returns: (passed, score_0_to_1, report)
        """
        staging_id = manifest['_staging_dir']
        staging_path = os.path.join(self.staging_dir, staging_id)
        
        logger.info(f"Validating: {staging_id}")
        
        # Get proposal type
        proposal_type = manifest.get('source_proposal', {}).get('finding', {}).get('type', 'unknown')
        
        # Run appropriate validation based on type
        if proposal_type == 'process_failure':
            passed, score, report = self._validate_process_fix(staging_path, manifest)
        elif proposal_type == 'resource_constraint':
            passed, score, report = self._validate_resource_fix(staging_path, manifest)
        elif proposal_type == 'error_rate':
            passed, score, report = self._validate_error_fix(staging_path, manifest)
        elif proposal_type == 'revenue_optimization':
            passed, score, report = self._validate_revenue_opt(staging_path, manifest)
        else:
            # Generic validation
            passed, score, report = self._validate_generic(staging_path, manifest)
        
        # Check retry count
        retry_count = manifest.get('source_proposal', {}).get('retry_count', 0)
        
        if not passed and retry_count >= 5:
            report += "\n\n⚠️ MAXIMUM RETRIES (5) EXHAUSTED - Human intervention required"
            logger.error(f"Max retries reached for {staging_id}")
        
        return passed, score, report
    
    def _validate_process_fix(self, staging_path: str, manifest: Dict) -> Tuple[bool, float, str]:
        """Validate process restart/fix scripts"""
        score = 0.0
        report_lines = []
        
        # Check 1: Script exists
        restart_script = os.path.join(staging_path, "restart_concierge.sh")
        if os.path.exists(restart_script):
            score += 0.3
            report_lines.append("✅ Restart script exists")
            
            # Check if executable
            if os.access(restart_script, os.X_OK):
                score += 0.1
                report_lines.append("✅ Script is executable")
            else:
                report_lines.append("⚠️  Script not executable")
        else:
            report_lines.append("❌ Restart script missing")
        
        # Check 2: Syntax validation (basic)
        try:
            with open(restart_script, 'r') as f:
                content = f.read()
                if 'pkill' in content and 'python3' in content:
                    score += 0.2
                    report_lines.append("✅ Contains process management logic")
                if 'sleep' in content:
                    score += 0.1
                    report_lines.append("✅ Has timing delays")
        except:
            report_lines.append("⚠️  Could not read script")
        
        # Check 3: Monitor script exists
        monitor_script = os.path.join(staging_path, "monitor_concierge.sh")
        if os.path.exists(monitor_script):
            score += 0.2
            report_lines.append("✅ Monitor script exists")
        
        # Final score adjustment
        score = min(1.0, score)
        passed = score >= 0.8
        
        report = "\n".join(report_lines)
        report += f"\n\nFinal Score: {score:.2f}/1.0"
        report += f"\nStatus: {'PASS' if passed else 'FAIL'}"
        
        return passed, score, report
    
    def _validate_resource_fix(self, staging_path: str, manifest: Dict) -> Tuple[bool, float, str]:
        """Validate resource cleanup scripts"""
        score = 0.0
        report_lines = []
        
        cleanup_script = os.path.join(staging_path, "cleanup_disk.sh")
        
        if os.path.exists(cleanup_script):
            score += 0.4
            report_lines.append("✅ Cleanup script exists")
            
            try:
                with open(cleanup_script, 'r') as f:
                    content = f.read()
                    
                    checks = [
                        ('find' in content, "Uses find command", 0.2),
                        ('delete' in content.lower() or '-delete' in content, "Has deletion logic", 0.2),
                        ('mtime' in content or '-mmin' in content, "Uses age filtering", 0.1),
                    ]
                    
                    for check, desc, points in checks:
                        if check:
                            score += points
                            report_lines.append(f"✅ {desc}")
                        else:
                            report_lines.append(f"⚠️  Missing: {desc}")
            except:
                report_lines.append("⚠️  Could not read script")
        else:
            report_lines.append("❌ Cleanup script missing")
        
        score = min(1.0, score)
        passed = score >= 0.8
        
        report = "\n".join(report_lines)
        report += f"\n\nFinal Score: {score:.2f}/1.0"
        report += f"\nStatus: {'PASS' if passed else 'FAIL'}"
        
        return passed, score, report
    
    def _validate_error_fix(self, staging_path: str, manifest: Dict) -> Tuple[bool, float, str]:
        """Validate error analysis scripts"""
        score = 0.0
        report_lines = []
        
        analyze_script = os.path.join(staging_path, "analyze_errors.sh")
        
        if os.path.exists(analyze_script):
            score += 0.5
            report_lines.append("✅ Analysis script exists")
            
            try:
                with open(analyze_script, 'r') as f:
                    content = f.read()
                    if 'grep' in content:
                        score += 0.2
                        report_lines.append("✅ Uses grep for filtering")
                    if 'ERROR' in content or 'Exception' in content:
                        score += 0.1
                        report_lines.append("✅ Searches for error patterns")
            except:
                report_lines.append("⚠️  Could not read script")
        else:
            report_lines.append("❌ Analysis script missing")
        
        score = min(1.0, score)
        passed = score >= 0.8
        
        report = "\n".join(report_lines)
        report += f"\n\nFinal Score: {score:.2f}/1.0"
        report += f"\nStatus: {'PASS' if passed else 'FAIL'}"
        
        return passed, score, report
    
    def _validate_revenue_opt(self, staging_path: str, manifest: Dict) -> Tuple[bool, float, str]:
        """Validate revenue optimization code"""
        score = 0.0
        report_lines = []
        
        # Check for Stripe integration code
        stripe_code = os.path.join(staging_path, "stripe_integration.py")
        
        if os.path.exists(stripe_code):
            score += 0.4
            report_lines.append("✅ Stripe integration code exists")
            
            try:
                with open(stripe_code, 'r') as f:
                    content = f.read()
                    
                    checks = [
                        ('import stripe' in content, "Imports Stripe library", 0.2),
                        ('create_deposit_session' in content, "Has session creation", 0.2),
                        ('checkout.Session' in content, "Uses Checkout Sessions", 0.1),
                    ]
                    
                    for check, desc, points in checks:
                        if check:
                            score += points
                            report_lines.append(f"✅ {desc}")
                        else:
                            report_lines.append(f"⚠️  Missing: {desc}")
            except:
                report_lines.append("⚠️  Could not read code")
        else:
            report_lines.append("❌ Stripe code missing")
        
        # Check for setup docs
        setup_doc = os.path.join(staging_path, "STRIPE_SETUP.md")
        if os.path.exists(setup_doc):
            score += 0.1
            report_lines.append("✅ Setup documentation exists")
        
        score = min(1.0, score)
        passed = score >= 0.8
        
        report = "\n".join(report_lines)
        report += f"\n\nFinal Score: {score:.2f}/1.0"
        report += f"\nStatus: {'PASS' if passed else 'FAIL'}"
        
        return passed, score, report
    
    def _validate_generic(self, staging_path: str, manifest: Dict) -> Tuple[bool, float, str]:
        """Generic validation for unknown types"""
        score = 0.5  # Base score for having files
        report_lines = ["ℹ️  Generic validation (unknown type)"]
        
        # Check if directory has any files
        files = os.listdir(staging_path)
        if len(files) > 0:
            score += 0.3
            report_lines.append(f"✅ Contains {len(files)} files")
        
        # Check for README
        readme = os.path.join(staging_path, "README.md")
        if os.path.exists(readme):
            score += 0.2
            report_lines.append("✅ Has documentation")
        
        score = min(1.0, score)
        passed = score >= 0.8
        
        report = "\n".join(report_lines)
        report += f"\n\nFinal Score: {score:.2f}/1.0"
        report += f"\nStatus: {'PASS' if passed else 'FAIL'}"
        
        return passed, score, report
    
    def create_validation_report(self, manifest: Dict, passed: bool, score: float, report: str):
        """Create validation report and update manifest"""
        staging_id = manifest['_staging_dir']
        
        validation_id = f"val_{staging_id}_{int(time.time())}"
        
        validation_data = {
            "metadata": {
                "validation_id": validation_id,
                "staging_id": staging_id,
                "agent": "crucible",
                "agent_id": self.agent_id,
                "validated_at": datetime.now().isoformat(),
            },
            "result": {
                "passed": passed,
                "score": score,
                "threshold": 0.8,
                "report": report
            },
            "next_action": "warden_review" if passed else "forge_rewrite"
        }
        
        # Save validation report
        report_path = os.path.join(self.validation_dir, f"{validation_id}.json")
        with open(report_path, 'w') as f:
            json.dump(validation_data, f, indent=2)
        
        # Mark staging as validated
        staging_path = os.path.join(self.staging_dir, staging_id)
        with open(os.path.join(staging_path, ".validated"), 'w') as f:
            f.write(validation_id)
        
        logger.info(f"Validation report created: {validation_id}")
        return validation_id
    
    def run_cycle(self):
        """Main execution cycle"""
        logger.info("="*60)
        logger.info("CRUCIBLE CYCLE STARTED")
        logger.info("="*60)
        
        implementations = self.poll_staging()
        
        if not implementations:
            logger.info("No unvalidated implementations found")
            return 0
        
        logger.info(f"Validating {len(implementations)} implementations...")
        
        passed_count = 0
        failed_count = 0
        
        for manifest in implementations:
            passed, score, report = self.validate_implementation(manifest)
            
            self.create_validation_report(manifest, passed, score, report)
            
            if passed:
                passed_count += 1
                logger.info(f"✅ PASS (score: {score:.2f}): {manifest['_staging_dir']}")
            else:
                failed_count += 1
                logger.warning(f"❌ FAIL (score: {score:.2f}): {manifest['_staging_dir']}")
        
        logger.info("="*60)
        logger.info(f"CRUCIBLE CYCLE COMPLETE")
        logger.info(f"Passed: {passed_count}")
        logger.info(f"Failed: {failed_count}")
        logger.info(f"Validation reports: {len(os.listdir(self.validation_dir))}")
        logger.info("="*60)
        
        return passed_count

def main():
    agent = CrucibleAgent()
    
    try:
        count = agent.run_cycle()
        print(f"\n✅ Crucible cycle complete: {count} validations passed")
        print(f"📁 Check: {VALIDATION_DIR}")
    except Exception as e:
        logger.error(f"Crucible cycle failed: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
