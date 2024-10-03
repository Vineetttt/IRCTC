from utils.db import get_db
from utils.train_utils import validate_train_data, train_number_exists

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
