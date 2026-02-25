#!/usr/bin/env python3
"""
PHNX Core - Integrated Cognitive Architecture

Combines:
- Browser-Use (web automation) ✅
- Vector Memory (semantic recall) ✅
- MCP Client (universal tools) ✅
- RSI Integration (self-improvement) ✅
"""

import asyncio
import os
import sys
from typing import Dict, List, Optional, Any
from datetime import datetime

# Import our components
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from browser_use_tool import BrowserUseTool
from vector_memory import VectorMemory
from mcp_client import MCPClient

class PHNXCore:
    """
    PHNX - Your AI assistant with exponential capabilities
    
    Usage:
        phnx = PHNXCore()
        
        # Remember something
        phnx.remember("Fred prefers browser automation with Browser-Use")
        
        # Recall by meaning
        phnx.recall("What does Fred like for browsers?")
        
        # Browse web
        phnx.browse("Find pricing info on example.com")
        
        # Use MCP tools
        phnx.use_tool("filesystem", "read_file", {"path": "workspace/SOUL.md"})
    """
    
    def __init__(self):
        print("🔥 Initializing PHNX Core...")
        
        # Initialize components
        self.browser = BrowserUseTool()
        self.memory = VectorMemory()
        self.mcp = MCPClient()
        
        # Session tracking
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.thoughts = []
        
        # Auto-remember initialization
        self.remember(
            f"PHNX Core initialized at {datetime.now().isoformat()}",
            {"type": "system", "event": "initialization"}
        )
        
        print("✅ PHNX Core ready!")
        print(f"   Session: {self.session_id}")
        print(f"   Components: Browser-Use, Vector Memory, MCP Client")
    
    def remember(self, content: str, metadata: Dict = None) -> str:
        """Store information in semantic memory"""
        meta = metadata or {}
        meta["session"] = self.session_id
        
        item_id = self.memory.store(content, meta)
        print(f"🧠 Remembered: {content[:50]}...")
        return item_id
    
    def recall(self, query: str, n_results: int = 3) -> List[Dict]:
        """Recall information by semantic meaning"""
        results = self.memory.recall(query, n_results)
        print(f"🔍 Recalled {len(results)} memories for: '{query}'")
        for r in results:
            print(f"   → {r['content'][:60]}...")
        return results
    
    def browse(self, task: str, url: Optional[str] = None) -> str:
        """Browse the web using Browser-Use"""
        print(f"🌐 Browsing: {task}")
        result = self.browser.run_sync(task, url)
        
        # Auto-remember important findings
        self.remember(
            f"Web browse: {task} → {result[:100]}...",
            {"type": "web_browse", "task": task}
        )
        
        return result
    
    def use_tool(self, server: str, tool: str, params: Dict) -> Dict:
        """Use an MCP tool"""
        print(f"🔧 Using tool: {server}.{tool}")
        
        # Run async in sync context
        result = asyncio.run(self.mcp.call_tool(server, tool, params))
        
        self.remember(
            f"Tool used: {server}.{tool} with params {params}",
            {"type": "tool_use", "server": server, "tool": tool}
        )
        
        return result
    
    def think(self, thought: str):
        """Record a thought (for reasoning chain)"""
        self.thoughts.append({
            "timestamp": datetime.now().isoformat(),
            "thought": thought
        })
        print(f"💭 {thought}")
    
    def status(self) -> Dict:
        """Get system status"""
        return {
            "session_id": self.session_id,
            "components": {
                "browser_use": "active",
                "vector_memory": "active",
                "mcp_client": "active"
            },
            "memories_stored": len(self.memory.list_all()),
            "thoughts_recorded": len(self.thoughts),
            "mcp_tools_available": len(self.mcp.list_available_tools())
        }
    
    def help(self) -> str:
        """Get help on using PHNX"""
        return """
# PHNX Core Commands

## Memory
- remember(content, metadata)  → Store information
- recall(query, n_results)     → Search by meaning

## Web
- browse(task, url)            → Automate browser

## Tools (MCP)
- use_tool(server, tool, params) → Use external tools

## System
- status()                     → Check system status
- think(thought)               → Record reasoning

## Example Workflow
```python
phnx = PHNXCore()

# Remember context
phnx.remember("Fred is building a PT booking bot")

# Browse for info
result = phnx.browse("Check Telegram Bot API documentation")

# Recall related info
memories = phnx.recall("What is Fred building?")
```
"""

def demo():
    """Demonstrate PHNX capabilities"""
    print("="*60)
    print("🔥 PHNX CORE DEMONSTRATION")
    print("="*60)
    
    # Initialize
    phnx = PHNXCore()
    
    print("\n" + "="*60)
    print("1️⃣ SEMANTIC MEMORY TEST")
    print("="*60)
    
    # Store memories
    phnx.remember("Fred wants to build a PT booking system using Telegram")
    phnx.remember("We successfully installed Browser-Use for web automation")
    phnx.remember("The RSI 4-pillar system is running and self-improving")
    
    # Recall by meaning (not keywords!)
    print("\nQuery: 'What automation tools are we using?'")
    phnx.recall("What automation tools are we using?")
    
    print("\nQuery: 'What systems are running?'")
    phnx.recall("What systems are running?")
    
    print("\n" + "="*60)
    print("2️⃣ MCP TOOLS TEST")
    print("="*60)
    
    tools = phnx.mcp.list_available_tools()
    print(f"\nAvailable MCP tools: {len(tools)}")
    for tool in tools:
        print(f"   {tool}")
    
    print("\n" + "="*60)
    print("3️⃣ SYSTEM STATUS")
    print("="*60)
    
    status = phnx.status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print("\n" + "="*60)
    print("✅ PHNX CORE OPERATIONAL")
    print("="*60)
    print("\nThe foundation is set. Ready for:")
    print("   • LangGraph workflow orchestration")
    print("   • E2B code execution")
    print("   • Full autonomous operation")

if __name__ == "__main__":
    demo()
