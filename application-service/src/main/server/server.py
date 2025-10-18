from flask import Flask
from flask_cors import CORS
from src.models.mysql.settings.connection import db_connection_handler

from src.main.routes.applications_routes import application_route_bp

db_connection_handler.connect_to_db()

app = Flask(__name__)
CORS(app)

app.register_blueprint(application_route_bp)
