#!/usr/bin/env python3
"""
Quick test to verify the API endpoints are working
"""
import sys
import os

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app

def test_endpoints():
    """Test basic endpoints"""
    with app.test_client() as client:
        # Test root endpoint
        response = client.get('/')
        print(f"GET / - Status: {response.status_code}")
        
        # Test API notes endpoint
        response = client.get('/api/notes')
        print(f"GET /api/notes - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.get_json()}")
        
        # Test API users endpoint
        response = client.get('/api/users')
        print(f"GET /api/users - Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.get_json()}")

if __name__ == "__main__":
    print("Testing API endpoints...")
    test_endpoints()
    print("Test completed!")