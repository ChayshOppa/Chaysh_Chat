from flask import Flask, request, jsonify, render_template
from src.core.assistant import Assistant
import asyncio

app = Flask(__name__)
assistant = Assistant()

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/api/ask", methods=['POST'])
async def ask():
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({"error": "No query provided"}), 400
            
        result = await assistant.process_query(query)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True) 