import logging
from flask import jsonify
from utils.db import get_db
from utils.error_handling import handle_db_error, log_unexpected_error
from utils.train_utils import train_number_exists
from utils.auth_utils import username_exists
from utils.booking_utils import (
    create_booking,
    get_booking_by_id,
    update_available_seats,
    select_available_seats
)
from mysql.connector import Error as MySQL_Error

logger = logging.getLogger(__name__)

def book_seat(data):
    db = get_db()
    cursor = db.cursor()

    train_number = data.get('train_number')
    username = data.get('username')
    seats_to_book = data.get('seats_to_book')

    if not train_number:
        logger.warning("Train number is required.")
        return {"error": "Train number is required."}, 400
    if not train_number_exists(cursor, train_number):
        logger.warning("Invalid Train Number, no train record found.")
        return {"error": "Invalid Train Number, no train record found"}, 400
    if not username:
        logger.warning("Username is required.")
        return {"error": "Username is required."}, 400
    if not username_exists(cursor, username):
        logger.warning("Invalid username.")
        return {"error": "Invalid username"}, 400
    if not seats_to_book or seats_to_book <= 0:
        logger.warning("Invalid number of seats to book.")
        return {"error": "Invalid number of seats to book."}, 400

    try:
        db.autocommit = False 

        # Check available seats
        available_seats = select_available_seats(cursor, train_number)

        if available_seats[0] == 0:
            logger.warning("No available seats to book.")
            return {"error": "No available seats to book."}, 400
        elif available_seats[0] < seats_to_book:
            logger.warning(f"Only {available_seats[0]} seats are available. Requested: {seats_to_book}.")
            return {"error": f"Only {available_seats[0]} seats are available. You requested {seats_to_book}."}, 400

        # Update available seats in trains table
        update_available_seats(cursor, train_number, seats_to_book)

        # Insert booking record and get the booking ID
        booking_id = create_booking(cursor, username, train_number, seats_to_book)

        db.commit()  

        logger.info(f"Seat booked successfully for user '{username}' on train '{train_number}'. Booking ID: {booking_id}.")
        return {
            "message": "Seat booked successfully.",
            "train_number": train_number,
            "booking_id": booking_id
        }, 201

    except MySQL_Error as e:
        db.rollback()  
        logger.error(f"Database error occurred while booking seat: {e}")
        return handle_db_error(e)
    except Exception as e:
        db.rollback() 
        logger.error(f"Unexpected error occurred while booking seat: {e}")
        return log_unexpected_error(e)
    finally:
        cursor.close() 
        db.close()  


def fetch_booking_details(booking_id):
    db = get_db()
    cursor = db.cursor()

    if booking_id <= 0:
        logger.warning("Invalid booking ID. It must be a positive integer.")
        return {"error": "Invalid booking ID. It must be a positive integer."}, 400

    try:
        booking_details = get_booking_by_id(cursor, booking_id)

        if booking_details is None:
            logger.warning(f"No booking found for booking ID {booking_id}.")
            return {"error": "No booking found."}, 404

        booking_time = booking_details[4].isoformat() if booking_details[4] else None

        logger.info(f"Fetched booking details for booking ID {booking_id}.")
        return {
            "booking_id": booking_details[0],
            "username": booking_details[1],
            "train_number": booking_details[2],
            "seats_booked": booking_details[3],
            "booking_time": booking_time  
        }

    except MySQL_Error as e:
        logger.error(f"Database error occurred while fetching booking details: {e}")
        return handle_db_error(e)
    except Exception as e:
        logger.error(f"Unexpected error occurred while fetching booking details: {e}")
        return log_unexpected_error(e)
    finally:
        cursor.close()  
        db.close()  
