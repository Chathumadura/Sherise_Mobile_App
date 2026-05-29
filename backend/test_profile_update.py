import requests
import json

print("=" * 80)
print("STEP 1: LOGIN WITH KAVISHKA")
print("=" * 80)

# Step 1: Login
login_data = {'email': 'kavishka@gmail.com', 'password': '123456'}
login_resp = requests.post(
    'https://sherise-mobile-app.onrender.com/auth/login',
    json=login_data,
    timeout=10
)

if login_resp.status_code != 200:
    print(f"❌ Login failed: {login_resp.json()}")
    exit()

login_json = login_resp.json()
token = login_json['access_token']
user_id = login_json['user']['id']

print(f"✅ Login successful!")
print(f"User ID: {user_id}")
print(f"Token: {token[:30]}...")

print("\n" + "=" * 80)
print("STEP 2: UPDATE PROFILE")
print("=" * 80)

# Step 2: Update profile
update_data = {
    'full_name': 'Kavishka Updated',
    'phone': '0712345678',
    'address': 'Colombo, Sri Lanka',
    'bio': 'Testing profile update functionality',
    'occupation': 'Developer'
}

headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
update_resp = requests.put(
    'https://sherise-mobile-app.onrender.com/profile',
    json=update_data,
    headers=headers,
    timeout=10
)

print(f"Status: {update_resp.status_code}")
print(f"Response: {update_resp.text}")

if update_resp.status_code == 200:
    print("\n✅ Profile updated successfully!")
else:
    print("\n❌ Profile update failed")
    exit()

print("\n" + "=" * 80)
print("STEP 3: GET PROFILE (VERIFY UPDATE)")
print("=" * 80)

# Step 3: Get profile to verify
get_resp = requests.get(
    'https://sherise-mobile-app.onrender.com/profile',
    headers=headers,
    timeout=10
)

if get_resp.status_code == 200:
    profile = get_resp.json()
    print(f"✅ Profile retrieved successfully!")
    print(f"Full Name: {profile.get('full_name')}")
    print(f"Phone: {profile.get('phone')}")
    print(f"Address: {profile.get('address')}")
    print(f"Bio: {profile.get('bio')}")
    print(f"Occupation: {profile.get('occupation')}")
else:
    print(f"❌ Get profile failed: {get_resp.json()}")

print("\n" + "=" * 80)
print("STEP 4: CHECK DATABASE")
print("=" * 80)

import sqlite3
conn = sqlite3.connect('sherise.db')
cursor = conn.cursor()

cursor.execute('SELECT full_name, phone, address, bio, occupation FROM profiles WHERE user_id = ?', (user_id,))
profile_db = cursor.fetchone()

if profile_db:
    print(f"✅ Profile found in database!")
    print(f"Full Name: {profile_db[0]}")
    print(f"Phone: {profile_db[1]}")
    print(f"Address: {profile_db[2]}")
    print(f"Bio: {profile_db[3]}")
    print(f"Occupation: {profile_db[4]}")
else:
    print("❌ Profile not found in database")

conn.close()

print("\n" + "=" * 80)
print("✅ FULL FLOW COMPLETE - DATA SAVED TO DATABASE!")
print("=" * 80)
