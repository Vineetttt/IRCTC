from mysql.connector import Error as MySQL_Error

def username_exists(cursor, username):
    cursor.execute('SELECT username FROM users WHERE username = %s', (username,))
    return cursor.fetchone() is not None

def validate_username(username):
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be between 3 and 50 characters."
    return True, ""