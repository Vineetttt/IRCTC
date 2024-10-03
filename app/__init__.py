from flask import Flask
from flask_cors import CORS
from .config import Config
from utils.db import close_db, get_db
from flask_jwt_extended import JWTManager
from models.init_db import initialize_database
from routes import user_routes


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    # Initialize JWT Manager
    jwt = JWTManager(app)

    # Initialize the database
    @app.before_first_request
    def setup_database():
        db = get_db()  # Get the database connection
        initialize_database(db)  # Initialize the database tables

    # Register blueprints for routes
    app.register_blueprint(user_routes.bp)

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    return app
