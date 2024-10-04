from flask import Flask
from flask_cors import CORS
from .config import Config
from utils.db import close_db, get_db
from flask_jwt_extended import JWTManager
from models.init_db import initialize_database
from routes import auth_routes, admin_routes, train_routes
import logging

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),  
                        logging.StreamHandler()  
                    ])
    logger = logging.getLogger(__name__)

    # Initialize JWT Manager
    jwt = JWTManager(app)

    # Initialize the database
    @app.before_first_request
    def setup_database():
        db = get_db()  # Get the database connection
        initialize_database(db)  # Initialize the database tables

    # Register blueprints for routes
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(train_routes.bp)

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    return app
