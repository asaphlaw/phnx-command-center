# MCP Server Productivity Suite
# High-impact servers for PHNX

import os
import json
from typing import Dict, List

class MCPServerManager:
    """
    Manages MCP servers for maximum productivity
    
    Priority order (highest impact first):
    1. Filesystem    - Already enabled (local file access)
    2. Fetch         - Web scraping (no API key needed)
    3. Git           - Git operations (no API key needed)
    4. GitHub        - Repo management (needs GITHUB_TOKEN)
    5. Brave Search  - Web search (needs BRAVE_API_KEY)
    6. Google        - Gmail/Calendar (needs Google OAuth)
    7. Slack         - Messaging (needs SLACK tokens)
    8. PostgreSQL    - Database access (if needed)
    """
    
    SERVERS = {
        # Tier 1: Always Available (No API Key)
        "filesystem": {
            "enabled": True,
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", 
                     os.path.expanduser("~/.openclaw/workspace")],
            "description": "Local file system access",
            "productivity_score": 9,
            "api_key_required": False
        },
        "fetch": {
            "enabled": True,
            "command": "uvx",
            "args": ["mcp-server-fetch"],
            "description": "Web scraping and fetching",
            "productivity_score": 8,
            "api_key_required": False
        },
        "git": {
            "enabled": True,
            "command": "uvx",
            "args": ["mcp-server-git"],
            "description": "Git repository operations",
            "productivity_score": 8,
            "api_key_required": False
        },
        "sqlite": {
            "enabled": True,
            "command": "uvx",
            "args": ["mcp-server-sqlite", "--db-path", 
                     os.path.expanduser("~/.openclaw/workspace/vector_db/chroma.sqlite3")],
            "description": "SQLite database queries",
            "productivity_score": 7,
            "api_key_required": False
        },
        
        # Tier 2: API Key Required (High Impact)
        "github": {
            "enabled": False,
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-github"],
            "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_TOKEN", "")},
            "description": "GitHub repository management",
            "productivity_score": 10,
            "api_key_required": True,
            "setup_url": "https://github.com/settings/tokens"
        },
        "brave-search": {
            "enabled": False,
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-brave-search"],
            "env": {"BRAVE_API_KEY": os.getenv("BRAVE_API_KEY", "")},
            "description": "Web search via Brave",
            "productivity_score": 9,
            "api_key_required": True,
            "setup_url": "https://brave.com/search/api"
        },
        "google": {
            "enabled": False,
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-google"],
            "description": "Gmail, Calendar, Drive",
            "productivity_score": 9,
            "api_key_required": True,
            "setup_url": "https://developers.google.com/workspace/guides/create-credentials"
        },
        
        # Tier 3: Specialized (Medium Impact)
        "slack": {
            "enabled": False,
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-slack"],
            "description": "Slack messaging",
            "productivity_score": 7,
            "api_key_required": True,
            "setup_url": "https://api.slack.com/apps"
        },
        "postgres": {
            "enabled": False,
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-postgres", 
                     os.getenv("DATABASE_URL", "postgresql://localhost/phnx")],
            "description": "PostgreSQL database access",
            "productivity_score": 6,
            "api_key_required": False
        }
    }
    
    def __init__(self):
        self.config = self.SERVERS.copy()
        self._auto_enable()
    
    def _auto_enable(self):
        """Auto-enable servers with available credentials"""
        # Check for GitHub token
        if os.getenv("GITHUB_TOKEN"):
            self.config["github"]["enabled"] = True
            self.config["github"]["env"]["GITHUB_PERSONAL_ACCESS_TOKEN"] = os.getenv("GITHUB_TOKEN")
        
        # Check for Brave key
        if os.getenv("BRAVE_API_KEY"):
            self.config["brave-search"]["enabled"] = True
            self.config["brave-search"]["env"]["BRAVE_API_KEY"] = os.getenv("BRAVE_API_KEY")
        
        # Check for Google credentials
        if os.path.exists(os.path.expanduser("~/.config/gcloud/application_default_credentials.json")):
            self.config["google"]["enabled"] = True
        
        # Check for Slack tokens
        if os.getenv("SLACK_BOT_TOKEN") and os.getenv("SLACK_TEAM_ID"):
            self.config["slack"]["enabled"] = True
        
        # Check for DATABASE_URL
        if os.getenv("DATABASE_URL"):
            self.config["postgres"]["enabled"] = True
    
    def get_enabled_servers(self) -> List[Dict]:
        """Get list of enabled servers sorted by productivity score"""
        enabled = [
            {"name": name, **config}
            for name, config in self.config.items()
            if config["enabled"]
        ]
        return sorted(enabled, key=lambda x: x["productivity_score"], reverse=True)
    
    def get_setup_guide(self) -> str:
        """Get setup guide for disabled high-impact servers"""
        disabled = [
            (name, config) for name, config in self.config.items()
            if not config["enabled"] and config.get("api_key_required")
        ]
        
        if not disabled:
            return "✅ All high-impact MCP servers are enabled!"
        
        guide = ["# MCP Server Setup Guide\n", "Enable these for maximum productivity:\n"]
        
        for name, config in sorted(disabled, key=lambda x: x[1]["productivity_score"], reverse=True):
            guide.append(f"\n## {name.upper()} (Impact: {config['productivity_score']}/10)")
            guide.append(f"Purpose: {config['description']}")
            guide.append(f"Setup: {config.get('setup_url', 'See documentation')}")
            
            if name == "github":
                guide.append("```bash")
                guide.append("export GITHUB_TOKEN='ghp_your_token_here'")
                guide.append("```")
            elif name == "brave-search":
                guide.append("```bash")
                guide.append("export BRAVE_API_KEY='your_key_here'")
                guide.append("```")
            elif name == "google":
                guide.append("```bash")
                guide.append("gcloud auth application-default login")
                guide.append("```")
            elif name == "slack":
                guide.append("```bash")
                guide.append("export SLACK_BOT_TOKEN='xoxb-...'")
                guide.append("export SLACK_TEAM_ID='T...'")
                guide.append("```")
        
        return "\n".join(guide)
    
    def generate_claude_config(self) -> Dict:
        """Generate Claude Desktop configuration"""
        mcp_servers = {}
        
        for name, config in self.config.items():
            if config["enabled"]:
                server_config = {
                    "command": config["command"],
                    "args": config["args"]
                }
                if "env" in config:
                    server_config["env"] = config["env"]
                mcp_servers[name] = server_config
        
        return {"mcpServers": mcp_servers}
    
    def status(self) -> Dict:
        """Get current status"""
        enabled = len([s for s in self.config.values() if s["enabled"]])
        total = len(self.config)
        
        return {
            "enabled": enabled,
            "total": total,
            "productivity_potential": sum(
                s["productivity_score"] for s in self.config.values() if s["enabled"]
            ),
            "max_productivity": sum(s["productivity_score"] for s in self.config.values()),
            "servers": {
                name: "✅" if config["enabled"] else "⏸️"
                for name, config in self.config.items()
            }
        }

def main():
    """Test MCP Server Manager"""
    print("🔌 MCP SERVER PRODUCTIVITY SUITE")
    print("="*60)
    
    manager = MCPServerManager()
    
    # Show status
    status = manager.status()
    print(f"\nStatus: {status['enabled']}/{status['total']} servers enabled")
    print(f"Productivity: {status['productivity_potential']}/{status['max_productivity']}")
    
    print("\nEnabled Servers:")
    for server in manager.get_enabled_servers():
        print(f"  ✅ {server['name']}: {server['description']} (Impact: {server['productivity_score']})")
    
    # Show setup guide for disabled
    guide = manager.get_setup_guide()
    if "All high-impact" not in guide:
        print("\n" + guide)
    
    # Generate config
    config = manager.generate_claude_config()
    print("\n📄 Claude Desktop Config Generated")
    print(json.dumps(config, indent=2))

if __name__ == "__main__":
    main()
