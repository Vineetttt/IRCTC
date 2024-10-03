def create_booking_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            booking_id INT AUTO_INCREMENT PRIMARY KEY,  
            username VARCHAR(50) NOT NULL,             
            train_number VARCHAR(20) NOT NULL,        
            seats_booked INT NOT NULL,                 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
            FOREIGN KEY (train_number) REFERENCES trains(train_number) ON DELETE CASCADE  
        );
    ''')
    db.commit()
    cursor.close()