from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector import Error as MySQL_Error, IntegrityError
from utils.db import get_db
from utils.user_utils import username_exists, validate_username, fetch_user_password
from utils.error_handling import handle_db_error, log_unexpected_error
from flask_jwt_extended import create_access_token
from datetime import timedelta

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
        return handle_db_error(e)
    except Exception as e:
        return log_unexpected_error(e)
    finally:
        cursor.close()
        db.close()

def login_user(username, password):
    db = get_db()
    cursor = db.cursor()

    # Check if username exists
    if not username_exists(cursor, username):
        return {"error": "User does not exist."}, 404

    # Fetch the stored hashed password
    user = fetch_user_password(cursor, username)
    
    try:
        if user and check_password_hash(user[0], password):
            # Generate JWT token
            access_token = create_access_token(identity=username, expires_delta=timedelta(hours=6))
            return {"access_token": access_token}, 200
        else:
            return {"error": "Invalid credentials."}, 401
    except MySQL_Error as e:
        return handle_db_error(e)
    except Exception as e:
        return log_unexpected_error(e)
    finally:
        cursor.close()
        db.close()
    