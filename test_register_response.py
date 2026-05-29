#!/usr/bin/env python3
"""Test registration endpoint response format"""
import requests
import json
import random
import string

BASE_URL = 'https://sherise-mobile-app.onrender.com'

def random_email():
    """Generate random email"""
    rand = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"test_{rand}@gmail.com"

# Test registration
email = random_email()
print(f"Testing registration with: {email}")

payload = {
    "name": "Test User",
    "email": email,
    "password": "testpass123"
}

print(f"\nPayload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(f'{BASE_URL}/auth/register', json=payload, timeout=10)
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"Response Body: {response.text}")
    
    if response.status_code == 201:
        data = response.json()
        print(f"\n✅ SUCCESS - Registration Response:")
        print(json.dumps(data, indent=2))
        
        # Check required fields
        required_fields = ['access_token', 'token_type', 'user']
        for field in required_fields:
            if field in data:
                print(f"✅ Has '{field}': {type(data[field])}")
            else:
                print(f"❌ Missing '{field}'")
                
        if 'user' in data and isinstance(data['user'], dict):
            user_fields = ['id', 'name', 'email']
            for field in user_fields:
                if field in data['user']:
                    print(f"   ✅ user.{field}: {data['user'][field]}")
                else:
                    print(f"   ❌ user.{field}: MISSING")
    else:
        print(f"\n❌ ERROR - Status {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
except Exception as e:
    print(f"❌ Exception: {e}")
