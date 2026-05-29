import sqlite3

# Open the database
conn = sqlite3.connect('sherise.db')
cursor = conn.cursor()

# Get user details
cursor.execute('SELECT id, name, email, hashed_password FROM users WHERE email = ?', ('kavishka@gmail.com',))
user = cursor.fetchone()

print('=' * 70)
print('USER: kavishka@gmail.com')
print('=' * 70)

if user:
    print(f'ID: {user[0]}')
    print(f'Name: {user[1]}')
    print(f'Email: {user[2]}')
    print(f'Hashed Password (first 50 chars): {user[3][:50]}...')
    print(f'Hash Length: {len(user[3])}')
    
    # Check if it's bcrypt format ($2a$, $2b$, $2y$) or Argon2 format ($argon2)
    if user[3].startswith('$2'):
        print('Hash Type: BCRYPT (old - won\'t work with Argon2)')
    elif user[3].startswith('$argon2'):
        print('Hash Type: ARGON2 (new - will work)')
    else:
        print('Hash Type: UNKNOWN')
else:
    print('User not found')
    
conn.close()
