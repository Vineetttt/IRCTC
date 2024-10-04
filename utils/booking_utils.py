from utils.db import get_db
from mysql.connector import Error as MySQL_Error

def create_booking(cursor, username, train_number, seats_booked):
    cursor.execute(
        'INSERT INTO bookings (username, train_number, seats_booked) VALUES (%s, %s, %s)',
        (username, train_number, seats_booked)
    )
    return cursor.lastrowid  

def get_booking_by_id(cursor, booking_id):
    cursor.execute(
        'SELECT booking_id, username, train_number, seats_booked, created_at FROM bookings WHERE booking_id = %s',
        (booking_id,)
    )
    return cursor.fetchone()  

def update_available_seats(cursor, train_number, seats_to_book):
    cursor.execute(
        'UPDATE trains SET available_seats = available_seats - %s WHERE train_number = %s',
        (seats_to_book, train_number)
    )

def select_available_seats(cursor, train_number):
    cursor.execute('SELECT available_seats FROM trains WHERE train_number = %s FOR UPDATE', (train_number,))
    return cursor.fetchone()  
