# 🧠 Reminder for AI tools: Follow rules in `cursor-rules.md` before making changes to this file.

from flask import Flask, request, jsonify, render_template
from src.core.assistant import Assistant
import asyncio
from functools import wraps

app = Flask(__name__)
assistant = Assistant()

def async_route(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/terms")
def terms():
    return render_template('terms.html')

@app.route("/api/ask", methods=['POST'])
@async_route
async def ask():
    try:
        data = request.get_json()
        query = data.get('query', '')
        lang = data.get('lang', 'en')  # Default to English if not specified
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
            
        result = await assistant.process_query(query, lang)
        return jsonify(result)
        
    except Exception as e:
        print(f"Error processing query: {str(e)}")  # Add logging
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) 