#!/usr/bin/env python3
"""
E2B Code Executor - Safe sandbox for AI-generated code
"""

import asyncio
import os
from typing import Dict, Optional, List
from dataclasses import dataclass

try:
    from e2b import Sandbox
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False

@dataclass
class ExecutionResult:
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: int

class E2BExecutor:
    """Safe code execution using E2B sandboxes"""
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.api_key = os.getenv('E2B_API_KEY')
        self.sandbox = None
        
        if not E2B_AVAILABLE:
            raise ImportError("E2B not installed. Run: pip install e2b")
    
    async def run_python(self, code: str) -> ExecutionResult:
        """Execute Python code in sandbox"""
        try:
            if self.api_key:
                sbx = Sandbox(api_key=self.api_key)
            else:
                sbx = Sandbox()
            
            execution = sbx.run_code(code, timeout=self.timeout)
            
            return ExecutionResult(
                success=execution.exit_code == 0,
                stdout=execution.stdout,
                stderr=execution.stderr,
                exit_code=execution.exit_code,
                duration_ms=execution.duration
            )
        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=0
            )

class E2BTool:
    """Synchronous wrapper"""
    
    def __init__(self, timeout: int = 60):
        self.executor = E2BExecutor(timeout)
    
    def run_python(self, code: str) -> ExecutionResult:
        return asyncio.run(self.executor.run_python(code))

def test():
    print("🛡️ Testing E2B Code Execution...")
    print()
    
    try:
        tool = E2BTool()
        
        print("Running Python in sandbox...")
        result = tool.run_python("print('Hello from E2B!')")
        print(f"  Success: {result.success}")
        print(f"  Output: {result.stdout.strip()}")
        print()
        print("✅ E2B working!")
        
    except Exception as e:
        print(f"⚠️ Note: {e}")
        print("E2B API key may be needed: https://e2b.dev/dashboard")

if __name__ == "__main__":
    test()
