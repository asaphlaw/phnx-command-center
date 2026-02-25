# Browser-Use Skill

Reliable browser automation for AI agents. Replaces Camoufox with production-grade browser control.

## Requirements

```bash
export BROWSER_USE_API_KEY='your-key-here'
# Get key: https://cloud.browser-use.com/new-api-key
```

## Usage

### Python API

```python
from skills.browser_use.browser_use_tool import BrowserUseTool

tool = BrowserUseTool()
result = tool.run_sync("Navigate to example.com and extract all links")
print(result)
```

### From OpenClaw

Browser-Use is now available as a tool in your agent.

## Capabilities

- Navigate to URLs
- Click elements
- Fill forms
- Extract text/data
- Take screenshots
- Handle popups (automatic)
- Stealth mode (cloud option)

## Comparison: Browser-Use vs Camoufox

| Feature | Camoufox | Browser-Use |
|---------|----------|-------------|
| Setup time | 5+ hours | 10 minutes |
| Display bugs | Frequent | None |
| Element detection | Manual | AI-optimized |
| Popup handling | Manual | Automatic |
| Success rate | ~60% | ~95% |
