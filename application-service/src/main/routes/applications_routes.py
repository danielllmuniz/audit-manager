from flask import Blueprint, jsonify, request
from src.views.http_types.http_request import HttpRequest

from src.main.composer.application_creator_composer import application_creator_composer
from src.main.composer.application_lister_composer import application_lister_composer

from src.errors.error_handler import handle_errors

application_route_bp = Blueprint('applications_routes', __name__)

@application_route_bp.route('/applications', methods=['POST'])
def create_applications():
    try:
        http_request = HttpRequest(body=request.json, headers=dict(request.headers))
        view = application_creator_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code

@application_route_bp.route('/applications', methods=['GET'])
def list_applications():
    try:
        http_request = HttpRequest(headers=dict(request.headers))
        view = application_lister_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code
