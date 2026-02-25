#!/usr/bin/env python3
"""
Airtable Integration for PHNX
Connects to Fred's business database
"""

import os
import json
import requests
from typing import Dict, List, Optional

class AirtableClient:
    """
    Airtable API client for PHNX
    
    Usage:
        client = AirtableClient()
        clients = client.get_pt_clients()
        revenue = client.get_revenue_summary()
    """
    
    BASE_ID = "appCsi3KNqXcNNfFC"
    
    def __init__(self):
        self.api_key = os.getenv('AIRTABLE_API_TOKEN')
        if not self.api_key:
            raise ValueError("AIRTABLE_API_TOKEN not set")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _get(self, table: str, params: Dict = None) -> Dict:
        """Make GET request to Airtable"""
        url = f"https://api.airtable.com/v0/{self.BASE_ID}/{table}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_pt_clients(self, max_records: int = 20) -> List[Dict]:
        """Get personal training clients"""
        data = self._get("PT%20Clients", {"maxRecords": max_records})
        return data.get('records', [])
    
    def get_at_risk_clients(self) -> List[Dict]:
        """Get clients marked as at-risk"""
        # Filter by status if view exists
        data = self._get("PT%20Clients")
        records = data.get('records', [])
        # Filter for low sessions or specific status
        at_risk = []
        for r in records:
            fields = r.get('fields', {})
            remaining = fields.get('Sessions Remaining', 0)
            status = fields.get('Status', '')
            if remaining <= 2 or 'risk' in status.lower():
                at_risk.append(r)
        return at_risk
    
    def get_revenue_summary(self) -> Dict:
        """Get revenue summary from P&L"""
        data = self._get("PT%20Revenue%20(P%26L)")
        return data
    
    def get_goal_tracker(self) -> List[Dict]:
        """Get $200K goal tracker data"""
        data = self._get("%24200K%20Goal%20Tracker")
        return data.get('records', [])
    
    def get_corp_clients(self) -> List[Dict]:
        """Get corporate rental clients"""
        data = self._get("Corp%20Clients")
        return data.get('records', [])

def test_connection():
    """Test Airtable connection"""
    print("🧪 Testing Airtable Connection...")
    print()
    
    try:
        client = AirtableClient()
        
        # Test 1: Get PT Clients
        print("1. PT Clients:")
        clients = client.get_pt_clients(max_records=3)
        for c in clients:
            name = c['fields'].get('Client Name', 'Unknown')
            status = c['fields'].get('Status', 'N/A')
            remaining = c['fields'].get('Sessions Remaining', 0)
            print(f"   • {name}: {status} ({remaining} sessions left)")
        print()
        
        # Test 2: At-risk clients
        print("2. At-Risk Clients:")
        at_risk = client.get_at_risk_clients()
        if at_risk:
            for c in at_risk:
                name = c['fields'].get('Client Name', 'Unknown')
                remaining = c['fields'].get('Sessions Remaining', 0)
                print(f"   ⚠️ {name}: {remaining} sessions remaining")
        else:
            print("   ✅ No at-risk clients")
        print()
        
        # Test 3: Corporate clients
        print("3. Corporate Clients:")
        corp = client.get_corp_clients()
        for c in corp[:3]:
            name = c['fields'].get('Client Name', 'Unknown')
            status = c['fields'].get('Status', 'N/A')
            revenue = c['fields'].get('Monthly Revenue', 0)
            print(f"   • {name}: {status} (${revenue}/mo)")
        print()
        
        print("✅ Airtable connection successful!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_connection()
