from flask import Blueprint, jsonify, request
from src.views.http_types.http_request import HttpRequest

from src.main.composer.release_creator_composer import release_creator_composer
from src.main.composer.release_lister_composer import release_lister_composer
from src.main.composer.release_approver_composer import release_approver_composer

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

@release_route_bp.route('/releases', methods=['GET'])
def list_releases():
    try:
        http_request = HttpRequest()
        view = release_lister_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code

@release_route_bp.route('/releases/<int:release_id>/approve', methods=['POST'])
def approve_release(release_id):
    try:
        http_request = HttpRequest(
            param={"release_id": release_id},
            headers=dict(request.headers)
        )
        view = release_approver_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code
