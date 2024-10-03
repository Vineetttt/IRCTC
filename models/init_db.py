from .user_model import create_user_table

def initialize_database(db):
    create_user_table(db)
