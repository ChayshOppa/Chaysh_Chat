from flask import Blueprint, render_template, request, jsonify
from ..core.assistant import Assistant
import logging

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__)
assistant = Assistant()

@chat_bp.route('/')
def index():
    """Render the chat interface."""
    return render_template('chat.html')

@chat_bp.route('/api/chat', methods=['POST'])
async def chat():
    """Handle chat API requests."""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        category = data.get('category', '').strip()
        context = data.get('context', [])
        lang = data.get('lang', 'en')

        if not user_input:
            return jsonify({
                'error': 'Message is required'
            }), 400

        # Get response from assistant
        response = await assistant.get_response(
            user_input=user_input,
            context=context,
            category_override=category if category else None,
            lang=lang
        )

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500 