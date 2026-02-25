#!/usr/bin/env python3
"""
RSI ORCHESTRATOR
Master controller for the 4-Pillar RSI Architecture

Usage:
  python3 orchestrate.py --full-cycle    # Run all 4 pillars
  python3 orchestrate.py --status        # Check system status
  python3 orchestrate.py --forager       # Run Forager only
  python3 orchestrate.py --forge         # Run Forge only
  python3 orchestrate.py --crucible      # Run Crucible only
  python3 orchestrate.py --warden        # Run Warden only
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Dict, List, Optional

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(BASE_DIR, "logs")

def setup_logging():
    os.makedirs(LOGS_DIR, exist_ok=True)
    log_file = os.path.join(LOGS_DIR, f"orchestrator_{datetime.now().strftime('%Y%m%d')}.log")
    
    class Logger:
        def __init__(self, log_file):
            self.log_file = log_file
        
        def log(self, level: str, message: str):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            line = f"[{timestamp}] {level}: {message}"
            print(line)
            with open(self.log_file, 'a') as f:
                f.write(line + "\n")
        
        def info(self, msg): self.log("INFO", msg)
        def error(self, msg): self.log("ERROR", msg)
        def success(self, msg): self.log("SUCCESS", msg)
        def warning(self, msg): self.log("WARNING", msg)
    
    return Logger(log_file)

logger = setup_logging()

class RSIOrchestrator:
    """
    Orchestrates the 4-Pillar RSI system
    """
    
    def __init__(self):
        self.base_dir = BASE_DIR
        self.pillars = {
            "forager": {
                "name": "The Forager",
                "script": "forager/forager_agent.py",
                "input_dir": None,
                "output_dir": "proposals",
                "description": "Researcher & Innovator"
            },
            "forge": {
                "name": "The Forge",
                "script": "forge/forge_agent.py",
                "input_dir": "proposals",
                "output_dir": "staging",
                "description": "Developer & Self-Healer"
            },
            "crucible": {
                "name": "The Crucible",
                "script": "crucible/crucible_agent.py",
                "input_dir": "staging",
                "output_dir": "validation",
                "description": "Sandbox & Verifier"
            },
            "warden": {
                "name": "The Warden",
                "script": "warden/warden_agent.py",
                "input_dir": "validation",
                "output_dir": "deployed",
                "description": "Governor & Safety"
            }
        }
    
    def check_halt(self) -> bool:
        """Check if system is halted"""
        halt_file = os.path.join(self.base_dir, ".halt")
        return os.path.exists(halt_file)
    
    def run_pillar(self, pillar_name: str) -> bool:
        """Run a single pillar"""
        if pillar_name not in self.pillars:
            logger.error(f"Unknown pillar: {pillar_name}")
            return False
        
        pillar = self.pillars[pillar_name]
        script_path = os.path.join(self.base_dir, pillar["script"])
        
        if not os.path.exists(script_path):
            logger.error(f"Script not found: {script_path}")
            return False
        
        logger.info(f"🚀 Running {pillar['name']} ({pillar['description']})...")
        
        try:
            import subprocess
            result = subprocess.run(
                ["python3", script_path],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout per pillar
                cwd=self.base_dir
            )
            
            if result.returncode == 0:
                logger.success(f"✅ {pillar['name']} completed successfully")
                return True
            else:
                logger.error(f"❌ {pillar['name']} failed with code {result.returncode}")
                if result.stderr:
                    logger.error(f"   Error: {result.stderr[:200]}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏰ {pillar['name']} timed out after 5 minutes")
            return False
        except Exception as e:
            logger.error(f"❌ {pillar['name']} error: {e}")
            return False
    
    def run_full_cycle(self):
        """Run all 4 pillars in sequence"""
        logger.info("="*70)
        logger.info("🦞 RSI FULL CYCLE STARTED")
        logger.info("="*70)
        logger.info(f"Timestamp: {datetime.now().isoformat()}")
        logger.info("")
        
        # Check halt
        if self.check_halt():
            logger.warning("⚠️  System is HALTED (remove .halt file to resume)")
            return False
        
        results = {}
        
        # Phase 1: Forager
        logger.info("-"*70)
        logger.info("PHASE 1/4: FORAGER")
        logger.info("-"*70)
        results["forager"] = self.run_pillar("forager")
        time.sleep(2)  # Brief pause between phases
        
        # Phase 2: Forge
        logger.info("")
        logger.info("-"*70)
        logger.info("PHASE 2/4: FORGE")
        logger.info("-"*70)
        results["forge"] = self.run_pillar("forge")
        time.sleep(2)
        
        # Phase 3: Crucible
        logger.info("")
        logger.info("-"*70)
        logger.info("PHASE 3/4: CRUCIBLE")
        logger.info("-"*70)
        results["crucible"] = self.run_pillar("crucible")
        time.sleep(2)
        
        # Phase 4: Warden
        logger.info("")
        logger.info("-"*70)
        logger.info("PHASE 4/4: WARDEN")
        logger.info("-"*70)
        results["warden"] = self.run_pillar("warden")
        
        # Summary
        logger.info("")
        logger.info("="*70)
        logger.info("RSI CYCLE SUMMARY")
        logger.info("="*70)
        
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        
        for pillar, success in results.items():
            status = "✅ PASS" if success else "❌ FAIL"
            logger.info(f"  {status}: {self.pillars[pillar]['name']}")
        
        logger.info("")
        logger.info(f"Total: {success_count}/{total_count} pillars successful")
        
        if success_count == total_count:
            logger.success("🎉 FULL CYCLE COMPLETE - All pillars operational!")
        else:
            logger.warning("⚠️  Partial success - review logs for failures")
        
        logger.info("="*70)
        
        return success_count == total_count
    
    def get_status(self) -> Dict:
        """Get current system status"""
        status = {
            "timestamp": datetime.now().isoformat(),
            "system_halted": self.check_halt(),
            "pillars": {},
            "queues": {},
            "recent_activity": {}
        }
        
        # Check each pillar
        for pillar_name, pillar in self.pillars.items():
            script_path = os.path.join(self.base_dir, pillar["script"])
            status["pillars"][pillar_name] = {
                "name": pillar["name"],
                "description": pillar["description"],
                "script_exists": os.path.exists(script_path),
                "input_dir": pillar["input_dir"],
                "output_dir": pillar["output_dir"]
            }
        
        # Check queue sizes
        for dir_name in ["proposals", "staging", "validation", "deployed"]:
            dir_path = os.path.join(self.base_dir, dir_name)
            if os.path.exists(dir_path):
                count = len([f for f in os.listdir(dir_path) if not f.startswith('.')])
                status["queues"][dir_name] = count
            else:
                status["queues"][dir_name] = 0
        
        # Recent logs
        log_files = sorted([f for f in os.listdir(LOGS_DIR) if f.endswith('.log')], reverse=True)
        status["recent_activity"]["log_files"] = log_files[:5]
        
        return status
    
    def print_status(self):
        """Print formatted status"""
        status = self.get_status()
        
        print("\n" + "="*70)
        print("🦞 RSI SYSTEM STATUS")
        print("="*70)
        print(f"Timestamp: {status['timestamp']}")
        print(f"System: {'🛑 HALTED' if status['system_halted'] else '✅ OPERATIONAL'}")
        print("")
        
        print("PILLARS:")
        for pillar_name, pillar in status["pillars"].items():
            script_ok = "✅" if pillar["script_exists"] else "❌"
            print(f"  {script_ok} {pillar['name']}: {pillar['description']}")
        
        print("")
        print("QUEUES:")
        for queue, count in status["queues"].items():
            print(f"  📁 {queue}/: {count} items")
        
        print("")
        print("RECENT LOGS:")
        for log_file in status["recent_activity"]["log_files"]:
            print(f"  📝 {log_file}")
        
        print("="*70)

def main():
    parser = argparse.ArgumentParser(
        description="RSI Orchestrator - 4-Pillar Self-Improving System"
    )
    
    parser.add_argument(
        "--full-cycle", 
        action="store_true",
        help="Run all 4 pillars in sequence"
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show system status"
    )
    
    parser.add_argument(
        "--forager",
        action="store_true",
        help="Run Forager only"
    )
    
    parser.add_argument(
        "--forge",
        action="store_true",
        help="Run Forge only"
    )
    
    parser.add_argument(
        "--crucible",
        action="store_true",
        help="Run Crucible only"
    )
    
    parser.add_argument(
        "--warden",
        action="store_true",
        help="Run Warden only"
    )
    
    parser.add_argument(
        "--halt",
        action="store_true",
        help="Halt the RSI system"
    )
    
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume the RSI system"
    )
    
    args = parser.parse_args()
    
    orchestrator = RSIOrchestrator()
    
    # Handle halt/resume
    if args.halt:
        halt_file = os.path.join(BASE_DIR, ".halt")
        with open(halt_file, 'w') as f:
            f.write(datetime.now().isoformat())
        print("🛑 RSI system HALTED")
        print(f"   Remove {halt_file} to resume")
        return 0
    
    if args.resume:
        halt_file = os.path.join(BASE_DIR, ".halt")
        if os.path.exists(halt_file):
            os.remove(halt_file)
            print("✅ RSI system RESUMED")
        else:
            print("ℹ️  System was not halted")
        return 0
    
    # Show status
    if args.status:
        orchestrator.print_status()
        return 0
    
    # Run single pillar
    if args.forager:
        success = orchestrator.run_pillar("forager")
        return 0 if success else 1
    
    if args.forge:
        success = orchestrator.run_pillar("forge")
        return 0 if success else 1
    
    if args.crucible:
        success = orchestrator.run_pillar("crucible")
        return 0 if success else 1
    
    if args.warden:
        success = orchestrator.run_pillar("warden")
        return 0 if success else 1
    
    # Default: full cycle
    if args.full_cycle or len(sys.argv) == 1:
        success = orchestrator.run_full_cycle()
        return 0 if success else 1
    
    parser.print_help()
    return 0

if __name__ == "__main__":
    sys.exit(main())
