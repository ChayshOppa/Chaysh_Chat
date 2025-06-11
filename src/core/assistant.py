import os
import httpx
from typing import Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

class Assistant:
    def __init__(self):
        self.api_key = os.getenv('OPENROUTER_API_KEY')
        self.api_url = os.getenv('OPENROUTER_API_URL', 'https://openrouter.ai/api/v1/chat/completions')
        self.model = os.getenv('MODEL', 'mistral-7b-instruct')
        
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query and return AI response with suggestions."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are Chaysh, a helpful AI assistant. Provide clear, concise responses and relevant suggestions."},
                    {"role": "user", "content": query}
                ]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(self.api_url, json=data, headers=headers)
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
                
        except Exception as e:
            return {
                "error": str(e),
                "response": "I apologize, but I encountered an error processing your request.",
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