import os
import httpx
from typing import Dict, Any, List
from src.core.category_detector import detect_category

# Only load .env in development
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Get API key at module level
api_key = os.getenv("OPENROUTER_API_KEY")
print("API key present:", bool(api_key))  # for logging

if not api_key:
    raise Exception("OPENROUTER_API_KEY not found")

class Assistant:
    def __init__(self):
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.model = "openai/gpt-4.1-nano"  # Updated to GPT-4.1 Nano
        self.max_tokens = 300  # Limit response length
        self.temperature = 0.7  # Balanced creativity
        self.top_p = 0.9  # Increased determinism
        
        # Base system prompts by language
        self.base_prompts = {
            'en': "You are Chaysh, a helpful AI assistant. Provide clear, concise responses and relevant suggestions in English.",
            'pl': "Jesteś Chaysh, pomocnym asystentem AI. Odpowiadaj jasno i zwięźle po polsku, dostarczając odpowiednie sugestie."
        }
        
        # Category-specific system prompts
        self.category_prompts = {
            'pricing': {
                'en': "You are a pricing assistant. Find prices of user '{focus}'. Make a big estimation number on top, then generate a list of up to 10 positions with prices, product names, and where to buy.",
                'pl': "Jesteś asystentem cenowym. Znajdź ceny dla '{focus}'. Podaj dużą liczbę szacunkową na górze, a następnie wygeneruj listę do 10 pozycji z cenami, nazwami produktów i gdzie kupić."
            },
            'timeline': {
                'en': "You are an event calendar assistant. Find the next upcoming event or performance for '{focus}' and display the earliest date. Also include a short description of who they are.",
                'pl': "Jesteś asystentem kalendarza wydarzeń. Znajdź następne nadchodzące wydarzenie lub występ dla '{focus}' i wyświetl najwcześniejszą datę. Dodaj też krótki opis kim są."
            },
            'define': {
                'en': "You are a definition expert. Provide a short and clear explanation.",
                'pl': "Jesteś ekspertem od definicji. Podaj krótkie i jasne wyjaśnienie."
            },
            'compare': {
                'en': "You are a comparison assistant. Compare the two items given.",
                'pl': "Jesteś asystentem porównawczym. Porównaj podane elementy."
            }
        }
        
        # Language-specific suggestions
        self.suggestions = {
            'en': [
                "Can you elaborate on that?",
                "What specific aspects are you interested in?",
                "Would you like more detailed information?"
            ],
            'pl': [
                "Czy możesz to rozwinąć?",
                "Jakie konkretne aspekty Cię interesują?",
                "Czy chciałbyś bardziej szczegółowe informacje?"
            ]
        }
        
    def _truncate_prompt(self, prompt: str, max_length: int = 600) -> str:
        """Truncate prompt to max length."""
        return prompt[:max_length] if len(prompt) > max_length else prompt
        
    def _get_system_prompt(self, category: str, focus: str, lang: str) -> str:
        """Get the appropriate system prompt based on category and language."""
        if category and category in self.category_prompts:
            return self.category_prompts[category][lang].format(focus=focus)
        return self.base_prompts.get(lang, self.base_prompts['en'])
        
    async def process_query(self, query: str, lang: str = 'en') -> Dict[str, Any]:
        """Process a user query and return AI response with suggestions."""
        try:
            # Detect category and focus
            category, focus = detect_category(query, lang)
            
            # Truncate user input
            truncated_query = self._truncate_prompt(query)
            
            # Get appropriate system prompt
            system_prompt = self._get_system_prompt(category, focus, lang)
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://chaysh-1.onrender.com",
                "X-Title": "Chaysh AI Assistant"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": truncated_query}
                ],
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "top_p": self.top_p
            }
            
            print(f"Making API request to {self.api_url} with model {self.model}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=data
                )
                
                if response.status_code == 401:
                    print("API Error: Unauthorized - Invalid or missing API key")
                    error_msg = "I apologize, but I'm currently unable to process requests due to an authentication issue. Please try again later."
                    if lang == 'pl':
                        error_msg = "Przepraszam, ale obecnie nie mogę przetwarzać żądań z powodu problemu z uwierzytelnianiem. Spróbuj ponownie później."
                    return {
                        "error": "Authentication failed",
                        "response": error_msg,
                        "suggestions": []
                    }
                
                response.raise_for_status()
                result = response.json()
                
                # Extract and truncate the assistant's message
                assistant_message = result['choices'][0]['message']['content']
                truncated_response = self._truncate_prompt(assistant_message, 300)
                
                # Get language-specific suggestions
                suggestions = self._generate_suggestions(truncated_query, lang)
                
                return {
                    "response": truncated_response,
                    "suggestions": suggestions,
                    "category": category  # Include detected category in response
                }
                
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            error_msg = "I apologize, but I encountered an error while processing your request. Please try again later."
            if lang == 'pl':
                error_msg = "Przepraszam, ale napotkałem błąd podczas przetwarzania Twojego żądania. Spróbuj ponownie później."
            return {
                "error": f"API request failed: {e.response.status_code}",
                "response": error_msg,
                "suggestions": []
            }
        except Exception as e:
            print(f"Error processing query: {str(e)}")
            error_msg = "I apologize, but I encountered an unexpected error. Please try again later."
            if lang == 'pl':
                error_msg = "Przepraszam, ale napotkałem nieoczekiwany błąd. Spróbuj ponownie później."
            return {
                "error": str(e),
                "response": error_msg,
                "suggestions": []
            }
    
    def _generate_suggestions(self, query: str, lang: str = 'en') -> List[str]:
        """Generate relevant follow-up suggestions based on the query and language."""
        return self.suggestions.get(lang, self.suggestions['en'])[:3]  # Return top 3 suggestions 