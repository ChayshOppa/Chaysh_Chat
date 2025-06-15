from flask import Blueprint, request, jsonify, render_template
from src.services.openrouter_service import OpenRouterService
import asyncio
from src.services.search_service import search_service

# Create a single blueprint for all routes
bp = Blueprint('main', __name__)
openrouter_service = OpenRouterService()

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@bp.route('/terms')
def terms():
    return render_template('terms.html')

@bp.route('/api/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                "error": "Query is required",
                "suggestions": [{"text": "Please enter a search term", "category": "input"}]
            }), 400

        # Run the async function in the event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(openrouter_service.get_ai_response(query))
        loop.close()
        
        return jsonify(response)

    except Exception as e:
        return jsonify({
            "error": str(e),
            "suggestions": [{"text": "Try again", "category": "retry"}]
        }), 500 