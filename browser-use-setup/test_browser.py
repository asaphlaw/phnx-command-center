import asyncio
import os
from browser_use import Agent, Browser

# Test with local browser first (no API key needed)
# For cloud/stealth mode, set BROWSER_USE_API_KEY

async def test_browser():
    print("🌐 Testing Browser-Use...")
    print("")
    
    # Create browser instance (local mode)
    browser = Browser()
    
    # Create agent with a simple task
    agent = Agent(
        task="Navigate to example.com and tell me the page title",
        llm=None,  # We'll handle LLM separately through OpenClaw
        browser=browser,
    )
    
    try:
        result = await agent.run()
        print(f"✅ SUCCESS! Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_browser())
