from flask import Blueprint, request
from services.train_service import create_train
from middleware.api_key_middleware import require_api_key

bp = Blueprint('admin_routes', __name__)

@bp.route('/api/v1/admin/trains/add', methods=['POST'])
@require_api_key
def add_train():
    data = request.get_json()
    return create_train(data)
