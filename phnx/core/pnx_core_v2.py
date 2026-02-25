"""
PHNX Core v2.0 - Complete Cognitive Architecture

Integrated components:
- Browser-Use (Web automation) ✅
- Vector Memory (Semantic recall) ✅
- MCP Client (Universal tools) ✅
- E2B Executor (Safe code execution) ⏳
- LangGraph (Workflow orchestration) ✅
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tools.browser_use_tool import BrowserUseTool
from memory.vector_memory import VectorMemory
from tools.mcp_client import MCPClient
from workflows.langgraph_orchestrator import create_phnx_workflow

class PHNXCore:
    """
    PHNX v2.0 - Your AI assistant with exponential capabilities
    
    Usage:
        from phnx import PHNXCore
        phnx = PHNXCore()
    """
    
    def __init__(self):
        print("🔥 PHNX Core v2.0 Initializing...")
        
        self.browser = BrowserUseTool()
        self.memory = VectorMemory()
        self.mcp = MCPClient()
        self.workflow = create_phnx_workflow()
        
        print("✅ PHNX Core v2.0 Ready!")
        print("   Components: Browser | Memory | MCP | LangGraph")
    
    def status(self):
        return {
            "version": "2.0.0",
            "components": {
                "browser_use": "active",
                "vector_memory": "active",
                "mcp_client": "active",
                "langgraph": "active",
                "e2b": "installed (needs API key)"
            }
        }

if __name__ == "__main__":
    phnx = PHNXCore()
    print(phnx.status())
