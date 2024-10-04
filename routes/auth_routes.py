from flask import Blueprint, request, jsonify
from services.auth_service import register_account, login_user
from middleware.api_key_middleware import require_api_key
import logging

bp = Blueprint('auth_routes', __name__)
logger = logging.getLogger(__name__)

@bp.route('/api/v1/user/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        logger.warning("Invalid input for user registration")
        return jsonify({"error": "Invalid input"}), 400
    return register_account(username, email, password, role="user")

@bp.route('/api/v1/admin/register', methods=['POST'])
@require_api_key  
def register_admin_route():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not email or not password:
        logger.warning("Invalid input for admin registration")
        return jsonify({"error": "Invalid input"}), 400
    return register_account(username, email, password, role="admin")

@bp.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        logger.warning("Invalid input for login")
        return jsonify({"error": "Invalid input"}), 400
    return login_user(username, password)