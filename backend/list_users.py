import sqlite3

# Open the database
conn = sqlite3.connect('sherise.db')
cursor = conn.cursor()

# Get all users with details
cursor.execute('SELECT id, name, email, is_active FROM users ORDER BY id')
users = cursor.fetchall()

print('=' * 80)
print('ALL USERS IN DATABASE:')
print('=' * 80)

for user in users:
    user_id, name, email, is_active = user
    status = "✅ Active" if is_active else "❌ Inactive"
    print(f'ID: {user_id} | Name: {name:20} | Email: {email:30} | {status}')

print('=' * 80)
print(f'Total Users: {len(users)}')
print('=' * 80)

conn.close()
