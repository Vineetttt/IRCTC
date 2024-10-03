from flask import request, abort
from app.config import Config

API_KEY = Config.API_KEY

def require_api_key(f):
    def decorated_function(*args, **kwargs):
        if request.headers.get("X-API-KEY") == API_KEY:
            return f(*args, **kwargs)
        else:
            abort(401, description="Unauthorized: Invalid API Key")
    return decorated_function