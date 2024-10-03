from .user_model import create_user_table
from .train_model import create_train_table
from .booking_model import create_booking_table

def initialize_database(db):
    create_user_table(db)
    create_train_table(db)
    create_booking_table(db)
