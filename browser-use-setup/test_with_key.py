import asyncio
import os
from browser_use import Agent, Browser, ChatBrowserUse

async def test_browser():
    api_key = os.getenv('BROWSER_USE_API_KEY')
    
    if not api_key:
        print("❌ BROWSER_USE_API_KEY not set")
        print("Get your key at: https://cloud.browser-use.com/new-api-key")
        return
    
    print("🌐 Testing Browser-Use with API key...")
    print("")
    
    # Create browser instance
    # use_cloud=True for stealth browsers, False for local
    browser = Browser(use_cloud=False)  # Local browser
    
    # Create LLM client
    llm = ChatBrowserUse()
    
    # Create agent
    agent = Agent(
        task="Navigate to https://example.com and tell me what you see",
        llm=llm,
        browser=browser,
    )
    
    try:
        result = await agent.run()
        print(f"✅ SUCCESS!")
        print(f"Result: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_browser())
