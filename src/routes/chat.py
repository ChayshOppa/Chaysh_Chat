from flask import Blueprint, render_template, request, jsonify
from ..core.assistant import Assistant
import logging
import asyncio

logger = logging.getLogger(__name__)
chat_bp = Blueprint('chat', __name__)
assistant = Assistant()

@chat_bp.route('/')
def index():
    """Render the chat interface."""
    return render_template('chat.html')

@chat_bp.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat API requests."""
    try:
        data = request.get_json()
        print("Received chat input:", data)  # Debug log
        logger.info(f"Received chat request: {data}")

        user_input = data.get('message', '').strip()
        category = data.get('category', '').strip()
        context = data.get('context', [])
        lang = data.get('lang', 'en')

        if not user_input:
            logger.warning("Empty message received")
            return jsonify({
                'error': 'Message is required'
            }), 400

        # Get response from assistant
        logger.debug(f"Getting response from assistant for input: {user_input}")
        response = asyncio.run(assistant.get_response(
            user_input=user_input,
            context=context,
            category_override=category if category else None,
            lang=lang
        ))
        logger.debug(f"Assistant response: {response}")

        return jsonify(response)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request'
        }), 500 