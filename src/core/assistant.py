# 🧠 Reminder for AI tools: Follow rules in `cursor-rules.md` before making changes to this file.

import os
import httpx
from typing import Dict, Any, List

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
        
        # Language-specific system prompts
        self.system_prompts = {
            'en': "You are a helpful AI assistant. Please provide clear and concise responses in English.",
            'pl': "Jesteś pomocnym asystentem AI. Proszę udzielaj jasnych i zwięzłych odpowiedzi po polsku."
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
        
    async def process_query(self, query: str, lang: str = 'en') -> Dict[str, Any]:
        """Process a user query and return AI response with suggestions."""
        try:
            # Get language-specific system prompt
            system_prompt = self.system_prompts.get(lang, self.system_prompts['en'])
            
            # Add language-specific prefix to query
            lang_prefix = {
                'en': "Answer this in English:\n",
                'pl': "Odpowiedz po polsku:\n"
            }.get(lang, "")
            
            prefixed_query = f"{lang_prefix}{query}"
            
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
                    {"role": "user", "content": prefixed_query}
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
                suggestions = self._generate_suggestions(prefixed_query, lang)
                
                return {
                    "response": truncated_response,
                    "suggestions": suggestions
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