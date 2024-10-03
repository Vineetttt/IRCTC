from utils.db import get_db
from mysql.connector import Error as MySQL_Error
from utils.train_utils import validate_train_data, train_number_exists, fetch_trains_by_route
from utils.error_handling import handle_db_error, log_unexpected_error

def create_train(data):
    db = get_db()
    cursor = db.cursor()

    is_valid, message = validate_train_data(data)
    if not is_valid:
        return {"error": message}, 400

    train_number = data['train_number']
    if train_number_exists(cursor, train_number):
        return {"error": "Train Number already exists"}, 409  
    
    try:
        cursor.execute(
            'INSERT INTO trains (train_number, name, source, destination, total_seats, available_seats) VALUES (%s, %s, %s, %s, %s, %s)',
            (data['train_number'], data['name'], data['source'], data['destination'], data['total_seats'], data['total_seats'])
        )
        db.commit()
        return {"message": "Train added successfully.", "payload": data}, 201
    except MySQL_Error as e:
        return handle_db_error(e)
    except Exception as e:
        return log_unexpected_error(e)
    finally:
        cursor.close()
        db.close()

def get_seat_availability(source, destination):
    if not source or not destination:
        return {"error": "Source and destination cannot be empty."}, 400
    if source.lower() == destination.lower():
        return {"error": "Source and Destination must be different."}, 400
    try:
        trains = fetch_trains_by_route(source, destination)
        if not trains:
            return {"message": "No trains available for the specified route."}, 404
        response = [
            {
                "train_number": train[0],
                "name": train[1],
                "source": train[2],
                "destination": train[3],
                "total_seats": train[4],
                "available_seats": train[5]
            } for train in trains
        ]
        return response, 200
    except MySQL_Error as e:
        return handle_db_error(e)
    except Exception as e:
        return log_unexpected_error(e)
