import requests
import sqlite3

users = [
    ('kavishka@gmail.com', '123456', 'Kavishka User 1'),
    ('avishka@gmail.com', '123456', 'Avishka User 2'),
    ('daham@gmail.com', '123456', 'Daham User 3'),
    ('test@gmail.com', '123456', 'Test User 4'),
]

print("=" * 100)
print("TESTING ALL USERS: LOGIN → UPDATE PROFILE → VERIFY DATABASE")
print("=" * 100)

for email, password, new_name in users:
    print(f"\n{'=' * 100}")
    print(f"USER: {email}")
    print(f"{'=' * 100}")
    
    # Step 1: Login
    try:
        login_resp = requests.post(
            'https://sherise-mobile-app.onrender.com/auth/login',
            json={'email': email, 'password': password},
            timeout=10
        )
        
        if login_resp.status_code != 200:
            print(f"❌ Login failed: {login_resp.json()}")
            continue
            
        token = login_resp.json()['access_token']
        user_id = login_resp.json()['user']['id']
        print(f"✅ Login successful - User ID: {user_id}")
        
        # Step 2: Update profile
        headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        update_data = {
            'full_name': new_name,
            'phone': f'077{user_id}111111',
            'address': f'City {user_id}',
            'bio': f'Updated on 2026-05-30 for user {user_id}',
            'occupation': 'Professional'
        }
        
        update_resp = requests.put(
            'https://sherise-mobile-app.onrender.com/profile',
            json=update_data,
            headers=headers,
            timeout=10
        )
        
        if update_resp.status_code != 200:
            print(f"❌ Update failed: {update_resp.json()}")
            continue
            
        print(f"✅ Profile updated successfully")
        
        # Step 3: Get updated profile
        get_resp = requests.get(
            'https://sherise-mobile-app.onrender.com/profile',
            headers=headers,
            timeout=10
        )
        
        if get_resp.status_code == 200:
            profile = get_resp.json()
            print(f"✅ Profile retrieved:")
            print(f"   Name: {profile.get('full_name')}")
            print(f"   Phone: {profile.get('phone')}")
            print(f"   Bio: {profile.get('bio')}")
        
        # Step 4: Verify in database
        conn = sqlite3.connect('sherise.db')
        cursor = conn.cursor()
        cursor.execute('SELECT full_name, phone, address, bio FROM profiles WHERE user_id = ?', (user_id,))
        db_profile = cursor.fetchone()
        conn.close()
        
        if db_profile:
            print(f"✅ Database verified:")
            print(f"   Name: {db_profile[0]}")
            print(f"   Phone: {db_profile[1]}")
            print(f"   Address: {db_profile[2]}")
            print(f"   Bio: {db_profile[3]}")
            print(f"✅ {email} - FULL FLOW SUCCESS")
        else:
            print(f"❌ Profile not found in database")
            
    except Exception as e:
        print(f"❌ Error: {e}")

print(f"\n{'=' * 100}")
print("✅ ALL USERS TEST COMPLETE")
print(f"{'=' * 100}")
