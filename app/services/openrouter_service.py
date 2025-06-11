import httpx
import json
from app.config import Config

class OpenRouterService:
    def __init__(self):
        self.api_key = Config.OPENROUTER_API_KEY
        self.api_url = Config.OPENROUTER_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Chaysh Search",
            "Content-Type": "application/json"
        }

    async def get_ai_response(self, query: str) -> dict:
        try:
            if not self.api_key:
                return self._get_error_response("API key is not configured")

            # Use a fixed max_tokens of 288 (maximum allowed by current credits)
            max_tokens = 288
            char_limit = 600  # Limit the generated answer to 600 characters

            system_prompt = f"""You are a structured assistant that provides detailed information about products and topics.\nAnalyze the query and provide information in the following JSON format:\n{{\n    \"mode\": \"product\",\n    \"name\": \"Main topic/product name\",\n    \"description\": [\n        \"Key point 1\",\n        \"Key point 2\",\n        \"Key point 3\",\n        \"Key point 4\",\n        \"Summary\"\n    ],\n    \"source_info\": \"Brief source information\",\n    \"suggestions\": [\n        {{\"text\": \"Related topic 1\", \"category\": \"related\"}},\n        {{\"text\": \"Related topic 2\", \"category\": \"related\"}}\n    ],\n    \"actions\": [\n        {{\"type\": \"chat\", \"label\": \"Ask More\", \"query\": \"Related question\"}}\n    ]\n}}\n\nProvide detailed information (up to 600 characters) and include suggestions.\nAlways return valid JSON matching this structure.\n\nIMPORTANT: Use the suggestions as new keywords to generate a new response when clicked."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ]

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=self.headers,
                    json={
                        "model": Config.DEFAULT_MODEL,
                        "messages": messages,
                        "max_tokens": max_tokens,
                        "temperature": 0.7
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result['choices'][0]['message']['content']
                    return self._format_response(ai_response, char_limit)
                else:
                    error_detail = response.text
                    return self._get_error_response(f"API Error {response.status_code}: {error_detail}")

        except Exception as e:
            return self._get_error_response(f"Error: {str(e)}")

    def _format_response(self, ai_response: str, char_limit: int = 600) -> dict:
        try:
            # Try to parse the AI response as JSON
            parsed_response = json.loads(ai_response)
            
            # Ensure all required fields are present
            response = Config.RESPONSE_STRUCTURE.copy()
            response.update(parsed_response)
            
            # Validate and clean up the response
            if not isinstance(response['description'], list):
                response['description'] = [response['description']]
            # Limit each description entry to char_limit
            response['description'] = [str(d)[:char_limit] for d in response['description']]
            
            if not isinstance(response['suggestions'], list):
                response['suggestions'] = []
            # Ensure each suggestion has a default action if none is provided
            for suggestion in response['suggestions']:
                if 'actions' not in suggestion:
                    suggestion['actions'] = [{"type": "chat", "label": "Ask More", "query": suggestion.get('text', '')}]
            
            if not isinstance(response['actions'], list):
                response['actions'] = []
            
            return response
            
        except json.JSONDecodeError:
            # If the response isn't valid JSON, create a structured response
            return {
                "mode": "product",
                "name": "Response",
                "description": [ai_response[:char_limit]],  # Limit to char_limit chars
                "source_info": "AI Response",
                "suggestions": [{"text": "Try a more specific query", "category": "refinement", "actions": [{"type": "chat", "label": "Ask More", "query": "Try a more specific query"}]}],
                "actions": [{"type": "chat", "label": "Ask More", "query": ""}]
            }
        except Exception as e:
            return self._get_error_response(f"Formatting Error: {str(e)}")

    def _get_error_response(self, error_message: str) -> dict:
        return {
            "mode": "error",
            "name": "Error",
            "description": [error_message],
            "source_info": "System Error",
            "suggestions": [{"text": "Try again", "category": "retry"}],
            "actions": [{"type": "retry", "label": "Retry", "query": ""}]
        } 