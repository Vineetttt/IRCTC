from flask import jsonify
from utils.db import get_db
from utils.error_handling import handle_db_error, log_unexpected_error
from utils.train_utils import train_number_exists
from utils.auth_utils import username_exists
from mysql.connector import Error as MySQL_Error


def book_seat(data):
    db = get_db()
    cursor = db.cursor()

    train_number = data.get('train_number')
    username = data.get('username')  
    seats_to_book = data.get('seats_to_book')

    if not train_number:
        return {"error": "Train number is required."}, 400
    if not train_number_exists(cursor, train_number):
        return {"error": "Invalid Train Number, no train record found"}, 400
    if not username:
        return {"error": "Username is required."}, 400
    if not username_exists(cursor, username):
        return {"error": "Invalid username"}, 400
    if not seats_to_book or seats_to_book <= 0:
        return {"error": "Invalid number of seats to book."}, 400

    try:
        db.autocommit = False  

        # Lock the row 
        cursor.execute('SELECT available_seats FROM trains WHERE train_number = %s FOR UPDATE', (train_number,))
        available_seats = cursor.fetchone()

        if available_seats[0] == 0:
            return {"error": "No available seats to book."}, 400
        elif available_seats[0] < seats_to_book:
            return {"error": f"Only {available_seats[0]} seats are available. You requested {seats_to_book}."}, 400

        # Update available seats
        cursor.execute('UPDATE trains SET available_seats = available_seats - %s WHERE train_number = %s', (seats_to_book, train_number))

        # Insert the booking and get the booking ID
        cursor.execute('INSERT INTO bookings (username, train_number, seats_booked) VALUES (%s, %s, %s)', (username, train_number, seats_to_book))
        booking_id = cursor.lastrowid 

        db.commit()  # Commit the transaction

        return {
            "message": "Seat booked successfully.",
            "train_number": train_number,
            "booking_id": booking_id  
        }, 201

    except MySQL_Error as e:
        return handle_db_error(e)
    except Exception as e:
        db.rollback()  
        return log_unexpected_error(e)
    finally:
        cursor.close()
        db.close()


def get_booking_by_id(booking_id):
    db = get_db()
    cursor = db.cursor()

    if booking_id <= 0:
        return {"error": "Invalid booking ID. It must be a positive integer."}, 400

    try:
        # Correcting the field name to 'created_at'
        cursor.execute('SELECT booking_id, username, train_number, seats_booked, created_at FROM bookings WHERE booking_id = %s', (booking_id,))
        booking_details = cursor.fetchone()

        if booking_details is None:
            return None

        # Ensure created_at is safely converted
        booking_time = booking_details[4].isoformat() if booking_details[4] else None

        return {
            "booking_id": booking_details[0],
            "username": booking_details[1],
            "train_number": booking_details[2],
            "seats_booked": booking_details[3],
            "booking_time": booking_time  # Using 'created_at' as 'booking_time'
        }

    except MySQL_Error as e:
        return handle_db_error(e)
    except Exception as e:
        return log_unexpected_error(e)
    finally:
        cursor.close()
        db.close()
