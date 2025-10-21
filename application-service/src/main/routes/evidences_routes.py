import os
from flask import Blueprint, send_file, jsonify

evidence_route_bp = Blueprint('evidence_route', __name__, url_prefix='/audit')


@evidence_route_bp.route('/evidences/<filename>', methods=['GET'])
def download_evidence(filename):
    """Download evidence file"""
    try:
        uploads_dir = '/app/uploads'
        filepath = os.path.join(uploads_dir, filename)

        if not os.path.exists(filepath):
            return jsonify({"error": "Evidence file not found"}), 404

        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
