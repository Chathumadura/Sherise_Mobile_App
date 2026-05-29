import requests
import json

# Test login with password 123456 for all users
users = [
    ('kavishka@gmail.com', '123456'),
    ('avishka@gmail.com', '123456'),
    ('daham@gmail.com', '123456'),
    ('test@gmail.com', '123456'),
    ('test2@gmail.com', '123456'),
    ('pasindu@gmail.com', '123456'),
    ('sithmikavindi2@gmail.com', '123456'),
]

print("=" * 80)
print("TESTING LOGIN WITH PASSWORD: 123456")
print("=" * 80)

for email, password in users:
    try:
        login_resp = requests.post(
            'https://sherise-mobile-app.onrender.com/auth/login',
            json={'email': email, 'password': password},
            timeout=10
        )
        
        if login_resp.status_code == 200:
            print(f"✅ {email:30} - LOGIN SUCCESS")
        else:
            print(f"❌ {email:30} - {login_resp.status_code} {login_resp.json().get('detail', 'Failed')}")
            
    except Exception as e:
        print(f"❌ {email:30} - Error: {e}")

print("=" * 80)
