from flask import current_app as app

def log_unexpected_error(e):
    app.logger.error(f"Unexpected error: {str(e)}")
    return {"message": "An unexpected error occurred. Please try again later.", "error": str(e)}, 500

def handle_db_error(e):
    app.logger.error(f"Database error: {str(e)}")
    return {"message": "A database error occurred. Please try again later.", "error": str(e)}, 500
