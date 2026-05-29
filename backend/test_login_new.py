import requests
import json

# Test Login with the user we registered earlier
print("=" * 70)
print("TESTING LOGIN WITH NEWLY REGISTERED USER")
print("=" * 70)

login_data = {
    'email': 'kavishtest999@gmail.com',
    'password': 'Test@12345'
}

try:
    login_resp = requests.post(
        'https://sherise-mobile-app.onrender.com/auth/login',
        json=login_data,
        timeout=10
    )
    print(f"Status Code: {login_resp.status_code}")
    print(f"Response: {login_resp.text}")
    
    if login_resp.status_code == 200:
        print("\n✅ LOGIN SUCCESSFUL!")
        login_json = login_resp.json()
        login_token = login_json.get('access_token')
        login_user = login_json.get('user')
        print(f"Token (first 30 chars): {login_token[:30]}..." if login_token else "No token")
        print(f"User Email: {login_user.get('email')}")
        print(f"User Name: {login_user.get('name')}")
    else:
        print("\n❌ LOGIN FAILED")
        
except Exception as e:
    print(f"❌ Error: {e}")
