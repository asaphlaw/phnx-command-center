#!/usr/bin/env python3
"""
Airtable CCI Integration
Connect to Airtable API for project/revenue tracking
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# Default token storage - should be overridden by env var or 1Password
DEFAULT_TOKEN = os.environ.get('AIRTABLE_API_TOKEN', '')
BASE_ID = "appCsi3KNqXcNNfFC"

class AirtableClient:
    """Airtable API client for CCI integration."""
    
    def __init__(self, token=None, base_id=None):
        self.token = token or DEFAULT_TOKEN
        self.base_id = base_id or BASE_ID
        self.base_url = f"https://api.airtable.com/v0/{self.base_id}"
        
        if not self.token:
            raise ValueError("Airtable API token required. Set AIRTABLE_API_TOKEN env var.")
    
    def _request(self, endpoint, method="GET", data=None):
        """Make authenticated request to Airtable API."""
        url = f"{self.base_url}/{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            headers=headers,
            method=method,
            data=json.dumps(data).encode() if data else None
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise Exception(f"Airtable API error: {e.code} - {error_body}")
    
    def get_bases(self):
        """List accessible bases."""
        url = "https://api.airtable.com/v0/meta/bases"
        headers = {"Authorization": f"Bearer {self.token}"}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    
    def get_tables(self):
        """List tables in the base."""
        url = f"https://api.airtable.com/v0/meta/bases/{self.base_id}/tables"
        headers = {"Authorization": f"Bearer {self.token}"}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    
    def get_records(self, table_name_or_id, max_records=100, view=None):
        """Get records from a table."""
        params = []
        if max_records:
            params.append(f"maxRecords={max_records}")
        if view:
            params.append(f"view={urllib.parse.quote(view)}")
        
        endpoint = table_name_or_id
        if params:
            endpoint += "?" + "&".join(params)
        
        return self._request(endpoint)
    
    def create_record(self, table_name, fields):
        """Create a new record."""
        return self._request(table_name, method="POST", data={"fields": fields})
    
    def update_record(self, table_name, record_id, fields):
        """Update an existing record."""
        return self._request(
            f"{table_name}/{record_id}",
            method="PATCH",
            data={"fields": fields}
        )


def main():
    parser = argparse.ArgumentParser(description="Airtable CCI Integration")
    parser.add_argument("--token", help="Airtable API token (or set AIRTABLE_API_TOKEN)")
    parser.add_argument("--base-id", default=BASE_ID, help="Airtable base ID")
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # List tables
    subparsers.add_parser("tables", help="List tables in base")
    
    # Get records
    records_parser = subparsers.add_parser("records", help="Get records from table")
    records_parser.add_argument("table", help="Table name or ID")
    records_parser.add_argument("--max", "-m", type=int, default=100, help="Max records")
    records_parser.add_argument("--view", "-v", help="View name")
    
    # Get bases
    subparsers.add_parser("bases", help="List accessible bases")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize client
    try:
        client = AirtableClient(token=args.token, base_id=args.base_id)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        if args.command == "tables":
            result = client.get_tables()
            print(json.dumps(result, indent=2))
        
        elif args.command == "records":
            result = client.get_records(args.table, max_records=args.max, view=args.view)
            print(json.dumps(result, indent=2))
        
        elif args.command == "bases":
            result = client.get_bases()
            print(json.dumps(result, indent=2))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    import urllib.parse
    main()
