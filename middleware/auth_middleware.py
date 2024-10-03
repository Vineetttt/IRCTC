from flask import request, jsonify
import jwt
from functools import wraps
from flask import current_app as app

def token_required(f):
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing!"}), 403

        try:
            token = token.split(" ")[1] 
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = data['sub']  
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token is invalid!"}), 403
        except Exception as e:
            return jsonify({"error": "Token validation error: " + str(e)}), 500

        return f(current_user, *args, **kwargs)
    
    return decorated
