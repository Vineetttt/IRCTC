from mysql.connector import Error as MySQL_Error

def username_exists(cursor, username):
    cursor.execute('SELECT username FROM users WHERE username = %s', (username,))
    return cursor.fetchone() is not None

def email_exists(cursor, email):
    cursor.execute('SELECT email FROM users WHERE email = %s', (email,))
    return cursor.fetchone() is not None

def validate_username(username):
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be between 3 and 50 characters."
    return True, ""

def fetch_user_password(cursor, username):
    cursor.execute('SELECT password FROM users WHERE username = %s', (username,))
    return cursor.fetchone()

def insert_user(cursor, db, username, email, hashed_password, role):
    cursor.execute(
        'INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)',
        (username, email, hashed_password, role)
    )
    db.commit()