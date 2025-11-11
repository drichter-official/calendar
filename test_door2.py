#!/usr/bin/env python
"""Test script to verify door 2 works correctly."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from website.app import app

def test_door2():
    """Test the /door/2 endpoint."""
    with app.test_client() as client:
        print("Testing /door/2 endpoint...")
        response = client.get('/door/2')

        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.content_type}")

        if response.status_code == 200:
            print("✓ SUCCESS: Door 2 page loads correctly!")
            # Check if it contains diagonal rule text
            if b'Diagonal Rule' in response.data:
                print("✓ SUCCESS: Page contains Diagonal Rule text!")
            if b'both main diagonals' in response.data:
                print("✓ SUCCESS: Page contains diagonal constraint description!")
        else:
            print(f"✗ FAIL: Non-200 status code: {response.status_code}")
            print(f"   Response: {response.data[:500]}")

def test_generate_door2():
    """Test the /generate/2 endpoint."""
    with app.test_client() as client:
        print("\nTesting /generate/2 endpoint...")
        response = client.get('/generate/2')

        print(f"Status Code: {response.status_code}")
        print(f"Content-Type: {response.content_type}")

        try:
            data = response.get_json()
            print(f"Response JSON: {data}")

            if response.status_code == 200:
                if data.get('success'):
                    print("✓ SUCCESS: Generation endpoint works correctly for door 2!")
                else:
                    print(f"✗ FAIL: Generation failed with message: {data.get('message')}")
            else:
                print(f"✗ FAIL: Non-200 status code: {response.status_code}")
                print(f"   Error: {data.get('message', 'No message')}")
        except Exception as e:
            print(f"✗ FAIL: Could not parse JSON response")
            print(f"   Error: {e}")
            print(f"   Response: {response.data[:200]}")

if __name__ == '__main__':
    test_door2()
    test_generate_door2()

