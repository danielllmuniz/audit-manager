from flask import Blueprint, jsonify, request
from src.views.http_types.http_request import HttpRequest

from src.main.composer.release_creator_composer import release_creator_composer
from src.main.composer.release_lister_composer import release_lister_composer
from src.main.composer.release_get_composer import release_get_composer
from src.main.composer.release_approver_composer import release_approver_composer
from src.main.composer.release_disapprover_composer import release_disapprover_composer
from src.main.composer.release_promoter_composer import release_promoter_composer

from src.errors.error_handler import handle_errors

release_route_bp = Blueprint('releases_routes', __name__, url_prefix='/audit')

@release_route_bp.route('/releases', methods=['POST'])
def create_release():
    try:
        http_request = HttpRequest(body=request.json, headers=dict(request.headers))
        view = release_creator_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code

@release_route_bp.route('/releases', methods=['GET'])
def list_releases():
    try:
        http_request = HttpRequest(
            headers=dict(request.headers),
            query=dict(request.args)
        )
        view = release_lister_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code

@release_route_bp.route('/releases/<int:release_id>', methods=['GET'])
def get_release(release_id):
    try:
        http_request = HttpRequest(
            param={"release_id": release_id},
            headers=dict(request.headers)
        )
        view = release_get_composer()

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

@release_route_bp.route('/releases/<int:release_id>/disapprove', methods=['POST'])
def disapprove_release(release_id):
    try:
        http_request = HttpRequest(
            param={"release_id": release_id},
            headers=dict(request.headers)
        )
        view = release_disapprover_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code

@release_route_bp.route('/releases/<int:release_id>/promote', methods=['POST'])
def promote_release(release_id):
    try:
        http_request = HttpRequest(
            param={"release_id": release_id},
            headers=dict(request.headers)
        )
        view = release_promoter_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code
