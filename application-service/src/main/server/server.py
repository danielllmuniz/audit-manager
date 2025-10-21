from flask import Flask
# from flask_cors import CORS
from src.models.mysql.settings.connection import db_connection_handler

from src.main.routes.applications_routes import application_route_bp
from src.main.routes.releases_routes import release_route_bp
from src.main.routes.evidences_routes import evidence_route_bp

db_connection_handler.connect_to_db()

app = Flask(__name__)
# CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'service': 'audit-manager-application-service'
    }, 200

app.register_blueprint(application_route_bp)
app.register_blueprint(release_route_bp)
app.register_blueprint(evidence_route_bp)
