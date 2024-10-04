from flask import Blueprint, request, jsonify
from services.booking_service import book_seat, fetch_booking_details
from middleware.auth_middleware import token_required

bp = Blueprint('booking_routes', __name__)

@bp.route('/api/v1/trains/book', methods=['POST'])
@token_required  
def book_a_seat(current_user):
    data = request.get_json()
    return book_seat(data)

@bp.route('/api/v1/trains/get-bookings/<int:booking_id>', methods=['GET'])
@token_required
def get_booking_details(current_user,booking_id):
    booking_details = fetch_booking_details(booking_id)

    if booking_details is None:
        return {"error": "Booking not found."}, 404
    return jsonify(booking_details), 200