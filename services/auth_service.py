import bcrypt
from mysql.connector import Error as MySQL_Error
from utils.db import get_db
from utils.auth_utils import username_exists, email_exists, validate_username, fetch_user_password, insert_user
from utils.error_handling import handle_db_error, log_unexpected_error
from flask_jwt_extended import create_access_token
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def register_account(username, email, password, role):
    # Validate username
    is_valid_username, message = validate_username(username)
    if not is_valid_username:
        logger.warning(f"Invalid username '{username}': {message}")
        return {"error": message}, 400
    
    db = get_db()
    cursor = db.cursor()

    try:
        # Check if username or email already exists
        if username_exists(cursor, username.lower()):
            logger.warning(f"Registration failed for '{username}': Username already exists.")
            return {"error": "Username already exists."}, 409  
        if email_exists(cursor, email.lower()):
            logger.warning(f"Registration failed for '{username}': Email already exists.")
            return {"error": "Email already exists."}, 409  

        # Hash password with bcrypt
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        insert_user(cursor, db, username.lower(), email.lower(), hashed_password.decode('utf-8'), role)

        logger.info(f"User registered successfully: '{username}' with role '{role}'")
        return {"message": "User registered successfully", "username": username}, 201
    except MySQL_Error as e:
        logger.error(f"Database error during registration for '{username}': {str(e)}")
        return handle_db_error(e)
    except Exception as e:
        logger.error(f"Unexpected error during registration for '{username}': {str(e)}")
        return log_unexpected_error(e)
    finally:
        cursor.close()
        db.close()

def login_user(username, password):
    db = get_db()
    cursor = db.cursor()

    try:
        # Check if username exists
        if not username_exists(cursor, username):
            logger.warning(f"Login attempt for non-existing user '{username}'")
            return {"error": "User does not exist, Please register"}, 404

        user = fetch_user_password(cursor, username)

        if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
            # Generate JWT token
            access_token = create_access_token(identity=username, expires_delta=timedelta(hours=6))
            logger.info(f"User '{username}' logged in successfully.")
            return {"access_token": access_token}, 200
        else:
            logger.warning(f"Invalid password attempt for user '{username}'.")
            return {"error": "Invalid Password, please try again."}, 401
    except MySQL_Error as e:
        logger.error(f"Database error during login for '{username}': {str(e)}")
        return handle_db_error(e)
    except Exception as e:
        logger.error(f"Unexpected error during login for '{username}': {str(e)}")
        return log_unexpected_error(e)
    finally:
        cursor.close()
        db.close()