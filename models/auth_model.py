def create_user_table(db):
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username VARCHAR(50) NOT NULL PRIMARY KEY,
            email VARCHAR(100) NOT NULL UNIQUE,  
            password VARCHAR(255) NOT NULL,
            role ENUM('user', 'admin') NOT NULL DEFAULT 'user'
        );
    ''')
    db.commit()
