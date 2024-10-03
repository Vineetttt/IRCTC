import os

class Config:
    MYSQL_USER = os.environ.get('MYSQL_USER')  
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') 
    MYSQL_DB = os.environ.get('MYSQL_DB') 
    MYSQL_HOST = os.environ.get('MYSQL_HOST') 
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306)) 
    API_KEY = os.getenv('API_KEY') 
    SECRET_KEY = os.getenv('SECRET_KEY')
