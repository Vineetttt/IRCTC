from werkzeug.security import generate_password_hash
from mysql.connector import Error as MySQL_Error, IntegrityError
from utils.db import get_db
from utils.user_utils import username_exists, validate_username

def register_user(username, password):
    db = get_db()
    cursor = db.cursor()

    # Validate username
    is_valid_username, message = validate_username(username)
    if not is_valid_username:
        return {"error": message}, 400

    # Check if username already existss
    if username_exists(cursor, username):
        return {"error": "Username already exists."}, 409  

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    try:
        cursor.execute(
            'INSERT INTO users (username, password) VALUES (%s, %s)',
            (username, hashed_password)  # Default role as user, noone can modify it
        )
        db.commit()
        return {"message": "User registered successfully", "username": username}, 201

    except MySQL_Error as e:
        app.logger.error(f"Database error: {str(e)}")
        db.rollback()
        return {"error": "An error occurred while registering the user."}, 500

    except Exception as e:
        app.logger.error(f"Unexpected error: {str(e)}")
        db.rollback()
        return {"error": "An unexpected error occurred."}, 500