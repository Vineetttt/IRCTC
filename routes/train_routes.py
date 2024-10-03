from flask import Blueprint, request, jsonify
from services.train_service import get_seat_availability
from services.booking_service import book_seat, get_booking_by_id
from middleware.auth_middleware import token_required

bp = Blueprint('train_routes', __name__)

@bp.route('/api/v1/trains/availability', methods=['GET'])
def availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return {"error": "Source and destination are required."}, 400

    return get_seat_availability(source, destination)

@bp.route('/api/v1/trains/book', methods=['POST'])
@token_required  
def book_a_seat(current_user):
    data = request.get_json()
    return book_seat(data)

@bp.route('/api/v1/trains/get-bookings/<int:booking_id>', methods=['GET'])
def get_booking_details(booking_id):
    booking_details = get_booking_by_id(booking_id)

    if booking_details is None:
        return {"error": "Booking not found."}, 404

    return jsonify(booking_details), 200