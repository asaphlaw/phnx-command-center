#!/usr/bin/env python3
"""
Send Gmail via MCP Server
Run: python3 send_gmail_test.py
"""

import subprocess
import json

# Email details
TO = "clement.teojunrong@gmail.com"
SUBJECT = "Test from PHNX"
BODY = "Hello typing this from kimi, scheduling it to be sent at 930am today."

print("📧 Sending test email via Gmail MCP...")
print(f"To: {TO}")
print(f"Subject: {SUBJECT}")
print(f"Body: {BODY}")
print()

# The MCP server would be called through Claude Desktop
# This is a placeholder showing how it would work
print("Note: MCP servers are configured for Claude Desktop.")
print("Please use Claude Desktop to send this email, or run:")
print()
print("  npx -y @modelcontextprotocol/server-google")
print()
print("With proper environment variables set.")
