from flask import Blueprint, jsonify, request
from src.views.http_types.http_request import HttpRequest

from src.main.composer.application_creator_composer import application_creator_composer
from src.main.composer.application_lister_composer import application_lister_composer
from src.main.composer.application_get_composer import application_get_composer

from src.errors.error_handler import handle_errors

application_route_bp = Blueprint('applications_routes', __name__, url_prefix='/audit')

@application_route_bp.route('/applications', methods=['POST'])
def create_applications():
    """
    Create a new application
    ---
    tags:
      - Applications
    parameters:
      - name: x-user-role
        in: header
        type: string
        required: true
        enum: [DEV, APPROVER, DEVOPS]
        description: User role (requires DEV)
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - owner_team
            - repo_url
          properties:
            name:
              type: string
              example: "application_name"
            owner_team:
              type: string
              example: "team_name"
            repo_url:
              type: string
              example: "https://github.com/user/repo"
    responses:
      201:
        description: Application created successfully
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                owner_team:
                  type: string
                repo_url:
                  type: string
      400:
        description: Invalid data
      403:
        description: User does not have DEV permission
    """
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
    """
    List all applications
    ---
    tags:
      - Applications
    parameters:
      - name: x-user-role
        in: header
        type: string
        required: true
        enum: [DEV, APPROVER, DEVOPS]
        description: User role
    responses:
      200:
        description: List of applications
        schema:
          type: object
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  owner_team:
                    type: string
                  repo_url:
                    type: string
    """
    try:
        http_request = HttpRequest(headers=dict(request.headers))
        view = application_lister_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code

@application_route_bp.route('/applications/<int:application_id>', methods=['GET'])
def get_application(application_id):
    """
    Get application by ID
    ---
    tags:
      - Applications
    parameters:
      - name: application_id
        in: path
        type: integer
        required: true
        description: Application ID
      - name: x-user-role
        in: header
        type: string
        required: true
        enum: [DEV, APPROVER, DEVOPS]
        description: User role
    responses:
      200:
        description: Application found
        schema:
          type: object
          properties:
            data:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                owner_team:
                  type: string
                repo_url:
                  type: string
      404:
        description: Application not found
    """
    try:
        http_request = HttpRequest(
            param={"application_id": application_id},
            headers=dict(request.headers)
        )
        view = application_get_composer()

        http_response = view.handle(http_request)
        return jsonify(http_response.body), http_response.status_code
    except Exception as e:
        http_response = handle_errors(e)
        return jsonify(http_response.body), http_response.status_code
