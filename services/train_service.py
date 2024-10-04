from utils.db import get_db
from mysql.connector import Error as MySQL_Error
from utils.train_utils import validate_train_data, train_number_exists, insert_train, fetch_trains
from utils.error_handling import handle_db_error, log_unexpected_error
import logging

logger = logging.getLogger(__name__)

def create_train(data):
    db = get_db()  
    cursor = db.cursor()  

    try:
        is_valid, message = validate_train_data(data)
        if not is_valid:
            logging.warning(f"Validation error: {message}")
            return {"error": message}, 400

        train_number = data['train_number']
        if train_number_exists(cursor, train_number):  
            logging.warning("Train Number already exists.")
            return {"error": "Train Number already exists"}, 409  

        result = insert_train(cursor, data)  
        db.commit()  
        logging.info(f"Train added successfully: {data['train_number']} - {data['name']}") 
        return result
    except MySQL_Error as e:
        logging.error(f"Database error while adding train: {e}")
        db.rollback()  
        return handle_db_error(e)
    except Exception as e:
        logging.error(f"Unexpected error while adding train: {e}")
        return log_unexpected_error(e)
    finally:
        cursor.close()  
        db.close()  

def get_seat_availability(source, destination):
    if not source or not destination:
        return {"error": "Source and destination cannot be empty."}, 400
    if source.lower() == destination.lower():
        return {"error": "Source and Destination must be different."}, 400

    db = get_db()  
    cursor = db.cursor() 

    try:
        trains = fetch_trains(cursor, source, destination) 
        if not trains:
            logging.info(f"No trains available for route: {source} to {destination}.")
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
        logging.info(f"Fetched trains from {source} to {destination}.")
        return response, 200
    except MySQL_Error as e:
        logging.error(f"Database error while fetching trains: {e}")
        return handle_db_error(e)
    except Exception as e:
        logging.error(f"Unexpected error while fetching trains: {e}")
        return log_unexpected_error(e)
    finally:
        cursor.close()  
        db.close()  