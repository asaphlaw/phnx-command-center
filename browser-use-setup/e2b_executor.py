#!/usr/bin/env python3
"""
E2B Code Executor - Safe sandbox for AI-generated code

Enables PHNX to:
- Run Python scripts safely
- Process data files
- Convert formats
- Execute automation scripts
- Without touching host system
"""

import asyncio
import os
from typing import Dict, Optional, List
from dataclasses import dataclass

# E2B imports
try:
    from e2b import Sandbox
    E2B_AVAILABLE = True
except ImportError:
    E2B_AVAILABLE = False

@dataclass
class ExecutionResult:
    """Result of code execution"""
    success: bool
    stdout: str
    stderr: str
    exit_code: int
    duration_ms: int
    files: List[str]

class E2BExecutor:
    """
    Safe code execution using E2B sandboxes
    
    Usage:
        executor = E2BExecutor()
        
        # Run Python code
        result = await executor.run_python("""
            import pandas as pd
            df = pd.DataFrame({'a': [1,2,3]})
            print(df.to_json())
        """)
        
        # Run command
        result = await executor.run_command("ls -la")
        
        # Process file
        result = await executor.process_file("data.csv", "convert_to_json")
    """
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self.api_key = os.getenv('E2B_API_KEY')
        self.sandbox = None
        
        if not E2B_AVAILABLE:
            raise ImportError("E2B not installed. Run: pip install e2b")
    
    async def _get_sandbox(self):
        """Get or create sandbox instance"""
        if self.sandbox is None:
            if self.api_key:
                self.sandbox = Sandbox(api_key=self.api_key)
            else:
                # Limited usage without API key
                self.sandbox = Sandbox()
        return self.sandbox
    
    async def run_python(self, code: str, files: Dict[str, str] = None) -> ExecutionResult:
        """
        Execute Python code in sandbox
        
        Args:
            code: Python code to execute
            files: Optional files to upload {'filename': 'content'}
            
        Returns:
            ExecutionResult with stdout, stderr, exit code
        """
        sbx = await self._get_sandbox()
        
        try:
            # Upload files if provided
            if files:
                for filename, content in files.items():
                    sbx.files.write(filename, content)
            
            # Run code
            execution = sbx.run_code(code, timeout=self.timeout)
            
            return ExecutionResult(
                success=execution.exit_code == 0,
                stdout=execution.stdout,
                stderr=execution.stderr,
                exit_code=execution.exit_code,
                duration_ms=execution.duration,
                files=[]
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=0,
                files=[]
            )
    
    async def run_command(self, command: str) -> ExecutionResult:
        """
        Run shell command in sandbox
        
        Args:
            command: Shell command to execute
            
        Returns:
            ExecutionResult
        """
        sbx = await self._get_sandbox()
        
        try:
            execution = sbx.commands.run(command, timeout=self.timeout)
            
            return ExecutionResult(
                success=execution.exit_code == 0,
                stdout=execution.stdout,
                stderr=execution.stderr,
                exit_code=execution.exit_code,
                duration_ms=execution.duration,
                files=[]
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=str(e),
                exit_code=-1,
                duration_ms=0,
                files=[]
            )
    
    async def process_data(self, data: str, operation: str) -> ExecutionResult:
        """
        Common data processing operations
        
        Args:
            data: Input data (CSV, JSON, etc.)
            operation: One of:
                - 'csv_to_json'
                - 'json_to_csv'
                - 'analyze_csv'
                - 'count_lines'
                - 'extract_emails'
                
        Returns:
            ExecutionResult with processed output
        """
        operations = {
            'csv_to_json': '''import csv
import json
import sys

reader = csv.DictReader(open('input.csv'))
data = list(reader)
print(json.dumps(data, indent=2))
''',
            'json_to_csv': '''import json
import csv
import sys

data = json.load(open('input.json'))
if data and len(data) > 0:
    writer = csv.DictWriter(sys.stdout, fieldnames=data[0].keys())
    writer.writeheader()
    writer.writerows(data)
''',
            'analyze_csv': '''import pandas as pd
df = pd.read_csv('input.csv')
print(df.describe().to_string())
print(f"\\nShape: {df.shape}")
print(f"\\nColumns: {list(df.columns)}")
''',
            'count_lines': '''with open('input.txt') as f:
    print(len(f.readlines()))
''',
            'extract_emails': '''import re
with open('input.txt') as f:
    text = f.read()
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    print('\\n'.join(set(emails)))
'''
        }
        
        if operation not in operations:
            return ExecutionResult(
                success=False,
                stdout="",
                stderr=f"Unknown operation: {operation}. Available: {list(operations.keys())}",
                exit_code=-1,
                duration_ms=0,
                files=[]
            )
        
        # Determine file extension
        ext = 'txt'
        if 'csv' in operation:
            ext = 'csv'
        elif 'json' in operation:
            ext = 'json'
        
        return await self.run_python(
            operations[operation],
            files={f'input.{ext}': data}
        )
    
    async def close(self):
        """Close sandbox connection"""
        if self.sandbox:
            self.sandbox.close()
            self.sandbox = None

# Convenience wrapper for sync usage
class E2BTool:
    """Synchronous wrapper for E2BExecutor"""
    
    def __init__(self, timeout: int = 60):
        self.executor = E2BExecutor(timeout)
    
    def run_python(self, code: str, files: Dict[str, str] = None) -> ExecutionResult:
        """Run Python code (sync wrapper)"""
        return asyncio.run(self.executor.run_python(code, files))
    
    def run_command(self, command: str) -> ExecutionResult:
        """Run shell command (sync wrapper)"""
        return asyncio.run(self.executor.run_command(command))
    
    def process_data(self, data: str, operation: str) -> ExecutionResult:
        """Process data (sync wrapper)"""
        return asyncio.run(self.executor.process_data(data, operation))

def test():
    """Test E2B execution"""
    print("🛡️ Testing E2B Code Execution...")
    print()
    
    try:
        tool = E2BTool()
        
        # Test 1: Simple Python
        print("Test 1: Run Python code")
        result = tool.run_python("""
import sys
print("Hello from E2B sandbox!")
print(f"Python version: {sys.version}")
        """)
        print(f"  Success: {result.success}")
        print(f"  Output: {result.stdout.strip()}")
        print()
        
        # Test 2: Data processing
        print("Test 2: Process CSV data")
        csv_data = "name,age,city\nAlice,30,NYC\nBob,25,LA\nCharlie,35,Chicago"
        result = tool.process_data(csv_data, 'analyze_csv')
        print(f"  Success: {result.success}")
        print(f"  Output preview: {result.stdout[:200]}...")
        print()
        
        # Test 3: Command execution
        print("Test 3: Run shell command")
        result = tool.run_command("uname -a")
        print(f"  Success: {result.success}")
        print(f"  Output: {result.stdout.strip()}")
        print()
        
        print("✅ E2B execution working!")
        
    except Exception as e:
        print(f"⚠️ E2B test failed: {e}")
        print("Note: E2B requires API key for full functionality")
        print("Get key: https://e2b.dev/dashboard")

if __name__ == "__main__":
    test()
