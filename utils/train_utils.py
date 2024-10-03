def validate_train_data(data):
    required_fields = ['train_number', 'name', 'source', 'destination', 'total_seats', 'available_seats']

    for field in required_fields:
        if field not in data:
            return False, f"{field} is required."
        
        if data[field] == "":
            return False, f"Parameter '{field}' cannot be empty."
    
    if data.get('total_seats', 0) <= 0:
        return False, "Total seats must be a positive integer."

    return True, ""


def train_number_exists(cursor, train_number):
    cursor.execute('SELECT train_number FROM trains WHERE train_number = %s', (train_number,))
    return cursor.fetchone() is not None
