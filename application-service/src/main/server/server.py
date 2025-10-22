from flask import Flask
# from flask_cors import CORS
from flasgger import Swagger
from src.models.mysql.settings.connection import db_connection_handler

from src.main.routes.applications_routes import application_route_bp
from src.main.routes.releases_routes import release_route_bp
from src.main.routes.evidences_routes import evidence_route_bp

db_connection_handler.connect_to_db()

app = Flask(__name__)
# CORS(app)

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Audit Manager API",
        "description": "API documentation for the Audit Manager Application Service",
        "version": "1.0.0"
    },
    "basePath": "/audit",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "x-user-role",
            "in": "header",
            "description": "User role (DEV, APPROVER, DEVOPS)"
        }
    }
}

Swagger(app, config=swagger_config, template=swagger_template)

@app.route('/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'service': 'audit-manager-application-service'
    }, 200

app.register_blueprint(application_route_bp)
app.register_blueprint(release_route_bp)
app.register_blueprint(evidence_route_bp)
