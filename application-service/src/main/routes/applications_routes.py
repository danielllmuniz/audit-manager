from flask import Blueprint, jsonify, request
from src.views.http_types.http_request import HttpRequest

from src.main.composer.person_creator_composer import person_creator_composer

from src.errors.error_handler import handle_errors

application_route_bp = Blueprint('applications_routes', __name__)

@application_route_bp.route('/applications', methods=['POST'])
def create_applications():
    try:
        http_request = HttpRequest(body=request.json)
        view = person_creator_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code
