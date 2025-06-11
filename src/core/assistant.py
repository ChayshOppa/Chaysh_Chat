import os
import httpx
from typing import Dict, Any, List

# Only load .env in development
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

class Assistant:
    def __init__(self):
        # Get API key directly from environment
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print("ERROR: OPENROUTER_API_KEY not found in environment")
            raise Exception("OPENROUTER_API_KEY not found in environment")
            
        print(f"API key present: {bool(self.api_key)}")
        
        self.api_url = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
        self.model = os.getenv('MODEL', 'mistral-7b-instruct')
        
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query and return AI response with suggestions."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://chaysh-1.onrender.com",
                "X-Title": "Chaysh AI Assistant"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are Chaysh, a helpful AI assistant. Provide clear, concise responses and relevant suggestions."},
                    {"role": "user", "content": query}
                ]
            }
            
            print(f"Making API request to {self.api_url} with model {self.model}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=data, headers=headers)
                
                if response.status_code == 401:
                    print("API Error: Unauthorized - Invalid or missing API key")
                    return {
                        "error": "Authentication failed",
                        "response": "I apologize, but I'm currently unable to process requests due to an authentication issue. Please try again later.",
                        "suggestions": []
                    }
                
                response.raise_for_status()
                result = response.json()
                
                # Extract the assistant's message
                assistant_message = result['choices'][0]['message']['content']
                
                # Generate suggestions based on the query
                suggestions = self._generate_suggestions(query)
                
                return {
                    "response": assistant_message,
                    "suggestions": suggestions
                }
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            return {
                "error": f"API request failed: {e.response.status_code}",
                "response": "I apologize, but I encountered an error while processing your request. Please try again later.",
                "suggestions": []
            }
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            return {
                "error": str(e),
                "response": "I apologize, but I encountered an unexpected error. Please try again later.",
                "suggestions": []
            }
    
    def _generate_suggestions(self, query: str) -> List[str]:
        """Generate relevant follow-up suggestions based on the query."""
        # Basic suggestion generation - can be enhanced based on query context
        suggestions = [
            "Can you elaborate on that?",
            "What specific aspects are you interested in?",
            "Would you like more detailed information?"
        ]
        return suggestions[:3]  # Return top 3 suggestions 