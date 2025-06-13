from flask import Blueprint, request, jsonify
from src.assistant_core import handle_assistant_request
from src.services.openrouter_service import get_model_config

bp = Blueprint('search', __name__)

@bp.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    user_prompt = data.get("prompt")

    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    result = handle_assistant_request(user_prompt)
    result["model"] = get_model_config().get("respond", "openai/gpt-4.1-nano")  # debug info
    return jsonify(result) 