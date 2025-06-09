from flask import Blueprint, request, jsonify, current_app, render_template
from app.core.assistant import Assistant
import logging

# Create two blueprints - one for the homepage and one for the API
bp = Blueprint('search', __name__)
api_bp = Blueprint('api', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@api_bp.route('/query', methods=['POST'])
async def query():
    try:
        data = request.get_json()
        
        # Validate request data
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing query parameter',
                'results': [{
                    'name': 'Error',
                    'description': ['Please provide a search query.'],
                    'source_info': 'Input validation',
                    'suggestions': [],
                    'actions': []
                }]
            }), 400

        # Get language preference (default to English)
        language = request.headers.get('X-Language', 'en')
        if language not in ['en', 'pl']:
            language = 'en'

        # Get context if provided
        context = data.get('context', None)

        # Initialize assistant with configuration
        assistant = Assistant(
            api_key=current_app.config['OPENROUTER_API_KEY'],
            api_url=current_app.config['OPENROUTER_API_URL']
        )

        # Process query
        result = await assistant.process_query(
            query=data['query'],
            context=context,
            language=language
        )

        # Clean up
        await assistant.close()

        return jsonify({
            'success': True,
            'results': [result]
        })

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': str(e),
            'results': [{
                'name': 'Error',
                'description': ['An error occurred while processing your request.'],
                'source_info': 'System error',
                'suggestions': [],
                'actions': []
            }]
        }), 500 