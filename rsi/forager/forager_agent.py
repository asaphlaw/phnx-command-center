#!/usr/bin/env python3
"""
THE FORAGER - Pillar 1 of RSI Architecture
Researcher & Innovator Agent

Role: Discovers improvements, searches for optimizations
Permissions: Web access, GitHub/ArXiv/ClawHub API read
Output: Proposals to proposals/ directory
"""

import os
import json
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configuration
PROPOSALS_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/proposals"
LOGS_DIR = "/Users/fredericklaw/.openclaw/workspace/rsi/logs"
LOBBSTER_DIR = "/Users/fredericklaw/.openclaw/workspace/projects/lobster-project"

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - FORAGER - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"{LOGS_DIR}/forager.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ForagerAgent:
    """
    The Forager continuously searches for:
    1. New optimization techniques
    2. Updated scripts and frameworks
    3. Better prompt engineering patterns
    4. System inefficiencies
    """
    
    def __init__(self):
        self.agent_id = str(uuid.uuid4())
        self.proposals_dir = PROPOSALS_DIR
        self.logs_dir = LOGS_DIR
        
        # Ensure directories exist
        os.makedirs(self.proposals_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        logger.info(f"Forager initialized [ID: {self.agent_id}]")
    
    def scan_system_inefficiencies(self) -> List[Dict]:
        """
        Scan current system for inefficiencies
        Returns list of potential improvements
        """
        issues = []
        
        # Check 1: Bot status
        logger.info("Scanning bot processes...")
        import subprocess
        try:
            result = subprocess.run(
                ["pgrep", "-f", "fred_pt_bot"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode != 0:
                issues.append({
                    "type": "process_failure",
                    "component": "concierge_bot",
                    "severity": "high",
                    "description": "Booking bot not running",
                    "suggested_action": "Restart fred_pt_bot.py"
                })
        except Exception as e:
            logger.warning(f"Could not scan processes: {e}")
        
        # Check 2: Disk usage
        logger.info("Checking disk usage...")
        try:
            result = subprocess.run(
                ["df", "-h", "/Users"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                if len(lines) > 1:
                    usage = lines[1].split()
                    if len(usage) > 4:
                        percent = usage[4].replace('%', '')
                        if int(percent) > 80:
                            issues.append({
                                "type": "resource_constraint",
                                "component": "disk_space",
                                "severity": "medium",
                                "description": f"Disk usage at {percent}%",
                                "suggested_action": "Clean old logs and temp files"
                            })
        except Exception as e:
            logger.warning(f"Could not check disk: {e}")
        
        # Check 3: Log errors
        logger.info("Scanning recent logs...")
        log_files = [
            "/tmp/fred_bot.log",
            "/tmp/watchdog_v3.log",
            "/tmp/coordinator.log"
        ]
        
        for log_file in log_files:
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r') as f:
                        # Read last 100 lines
                        lines = f.readlines()[-100:]
                        error_count = sum(1 for line in lines if 'ERROR' in line or 'Exception' in line)
                        if error_count > 5:
                            issues.append({
                                "type": "error_rate",
                                "component": os.path.basename(log_file),
                                "severity": "high" if error_count > 10 else "medium",
                                "description": f"{error_count} errors in recent logs",
                                "suggested_action": "Review and fix error sources"
                            })
                except Exception as e:
                    logger.warning(f"Could not read {log_file}: {e}")
        
        return issues
    
    def research_optimizations(self) -> List[Dict]:
        """
        Research external sources for optimizations
        This is a simplified version - full version would use APIs
        """
        proposals = []
        
        # Proposal 1: Based on today's experience
        proposals.append({
            "type": "architecture_improvement",
            "title": "Implement 4-Pillar RSI System",
            "description": "Replace manual monitoring with self-improving agent swarm",
            "rationale": "Today we spent 6+ hours on browser debugging that could have been auto-detected and fixed",
            "expected_impact": "Save 10+ hours/week on maintenance",
            "implementation_complexity": "medium",
            "priority": "high"
        })
        
        # Proposal 2: Content automation
        proposals.append({
            "type": "automation",
            "title": "Deploy MarketingBot Content",
            "description": "7 posts are ready but not published. Implement auto-posting to Instagram/LinkedIn",
            "rationale": "Lost lead generation opportunity - 0 new leads from content today",
            "expected_impact": "5-10 new leads/week",
            "implementation_complexity": "low",
            "priority": "high"
        })
        
        # Proposal 3: Payment integration
        proposals.append({
            "type": "revenue_optimization",
            "title": "Add Stripe Payment to Booking Bot",
            "description": "Accept booking deposits to reduce no-shows",
            "rationale": "Currently no payment on booking - clients can no-show without consequence",
            "expected_impact": "Reduce no-shows by 50%, +$300/month revenue protection",
            "implementation_complexity": "medium",
            "priority": "medium"
        })
        
        return proposals
    
    def create_proposal(self, finding: Dict) -> str:
        """
        Create a formal proposal document
        Returns the file path
        """
        proposal_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        
        proposal = {
            "metadata": {
                "proposal_id": proposal_id,
                "agent": "forager",
                "agent_id": self.agent_id,
                "created_at": timestamp,
                "version": "1.0"
            },
            "finding": finding,
            "proposal": {
                "title": finding.get("title", "System Improvement"),
                "description": finding.get("description", ""),
                "rationale": finding.get("rationale", ""),
                "expected_impact": finding.get("expected_impact", ""),
                "implementation_complexity": finding.get("implementation_complexity", "medium"),
                "priority": finding.get("priority", "medium"),
                "estimated_effort_hours": self._estimate_effort(finding)
            },
            "status": "pending_review",
            "assigned_to": "forge",
            "retry_count": 0
        }
        
        # Save proposal
        filename = f"proposal_{proposal_id}_{finding.get('type', 'improvement')}.json"
        filepath = os.path.join(self.proposals_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(proposal, f, indent=2)
        
        logger.info(f"Created proposal: {filename}")
        return filepath
    
    def _estimate_effort(self, finding: Dict) -> int:
        """Estimate implementation effort in hours"""
        complexity = finding.get("implementation_complexity", "medium")
        
        effort_map = {
            "low": 1,
            "medium": 4,
            "high": 8,
            "very_high": 16
        }
        
        return effort_map.get(complexity, 4)
    
    def run_cycle(self):
        """
        Main execution cycle - runs every heartbeat
        """
        logger.info("="*60)
        logger.info("FORAGER CYCLE STARTED")
        logger.info("="*60)
        
        # Step 1: Scan for inefficiencies
        logger.info("Phase 1: Scanning system...")
        issues = self.scan_system_inefficiencies()
        logger.info(f"Found {len(issues)} inefficiencies")
        
        # Step 2: Research optimizations
        logger.info("Phase 2: Researching optimizations...")
        optimizations = self.research_optimizations()
        logger.info(f"Generated {len(optimizations)} optimization proposals")
        
        # Step 3: Create proposals
        logger.info("Phase 3: Creating proposals...")
        all_findings = issues + optimizations
        
        created_count = 0
        for finding in all_findings:
            try:
                filepath = self.create_proposal(finding)
                created_count += 1
                logger.info(f"  ✓ {os.path.basename(filepath)}")
            except Exception as e:
                logger.error(f"Failed to create proposal: {e}")
        
        # Step 4: Summary
        logger.info("="*60)
        logger.info(f"FORAGER CYCLE COMPLETE")
        logger.info(f"Proposals created: {created_count}")
        logger.info(f"Pending in queue: {len(os.listdir(self.proposals_dir))}")
        logger.info("="*60)
        
        return created_count

def main():
    """Entry point for standalone execution or heartbeat trigger"""
    agent = ForagerAgent()
    
    try:
        count = agent.run_cycle()
        print(f"\n✅ Forager cycle complete: {count} proposals created")
        print(f"📁 Check: {PROPOSALS_DIR}")
    except Exception as e:
        logger.error(f"Forager cycle failed: {e}")
        print(f"\n❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
