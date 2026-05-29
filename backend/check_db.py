import sqlite3

# Open the database
conn = sqlite3.connect('sherise.db')
cursor = conn.cursor()

# Get all users
cursor.execute('SELECT id, name, email, is_active FROM users')
users = cursor.fetchall()

print('=' * 70)
print('DATABASE USERS:')
print('=' * 70)

if users:
    for user in users:
        print(f'ID: {user[0]}, Name: {user[1]}, Email: {user[2]}, Active: {user[3]}')
    print(f'\nTotal Users: {len(users)}')
else:
    print('No users found in database')
    
conn.close()
