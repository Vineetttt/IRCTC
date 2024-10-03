def create_train_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trains (
            train_number VARCHAR(20) NOT NULL PRIMARY KEY,  
            name VARCHAR(100) NOT NULL,  
            source VARCHAR(100) NOT NULL, 
            destination VARCHAR(100) NOT NULL, 
            total_seats INT NOT NULL, 
            available_seats INT NOT NULL  
        );
    ''')
    db.commit()
    cursor.close()
