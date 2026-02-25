# Browser-Use Skill for OpenClaw
# Purpose: Reliable browser automation for AI agents

import asyncio
import os
from typing import Optional
from browser_use import Agent, Browser, ChatBrowserUse

class BrowserUseTool:
    """Browser automation using Browser-Use library"""
    
    def __init__(self):
        self.api_key = os.getenv('BROWSER_USE_API_KEY')
        if not self.api_key:
            raise ValueError("BROWSER_USE_API_KEY not set. Get key at https://cloud.browser-use.com/new-api-key")
    
    async def browse(self, task: str, url: Optional[str] = None) -> str:
        """
        Execute a browser task
        
        Args:
            task: Natural language task description
            url: Optional starting URL
            
        Returns:
            Task result as string
        """
        # Prepend URL to task if provided
        if url and url not in task:
            task = f"Navigate to {url} and {task}"
        
        browser = Browser(use_cloud=False)  # Local browser
        llm = ChatBrowserUse()
        
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
        )
        
        try:
            result = await agent.run()
            return str(result)
        except Exception as e:
            return f"Error: {e}"
        # Note: browser.close() not needed, auto-cleanup

    def run_sync(self, task: str, url: Optional[str] = None) -> str:
        """Synchronous wrapper for sync contexts"""
        return asyncio.run(self.browse(task, url))

# Quick test function
def test():
    tool = BrowserUseTool()
    result = tool.run_sync("Navigate to example.com and tell me the page title")
    print(result)

if __name__ == "__main__":
    test()
