from flask import Blueprint, request
from services.train_service import get_seat_availability

bp = Blueprint('train_routes', __name__)

@bp.route('/api/v1/trains/availability', methods=['GET'])
def availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return {"error": "Source and destination are required."}, 400

    return get_seat_availability(source, destination)
