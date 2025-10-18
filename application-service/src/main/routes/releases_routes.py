from flask import Blueprint, jsonify, request
from src.views.http_types.http_request import HttpRequest

from src.main.composer.release_creator_composer import release_creator_composer

from src.errors.error_handler import handle_errors

release_route_bp = Blueprint('releases_routes', __name__)

@release_route_bp.route('/releases', methods=['POST'])
def create_release():
    try:
        http_request = HttpRequest(body=request.json)
        view = release_creator_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code
