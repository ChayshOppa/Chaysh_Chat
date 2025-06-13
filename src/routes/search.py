from flask import Blueprint, request, jsonify
from src.assistant_core import handle_assistant_request

bp = Blueprint('search', __name__)

@bp.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    result = handle_assistant_request(user_prompt)

    return jsonify(result), 200 