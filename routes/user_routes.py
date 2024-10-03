from flask import Blueprint, request, jsonify
from services.user_service import register_user

bp = Blueprint('user_routes', __name__)

@bp.route('/api/v1/users/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Invalid input"}), 400
    
    return register_user(username, password)
