import os
import httpx
from typing import Dict, Any, List
from src.prompt_categories import detect_category, category_map
from src.utils.cleaner import clean_gpt_reply

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
            'en': "You are Chaysh, a helpful AI assistant. Provide clear, concise responses based on the detected category.",
            'pl': "Jesteś Chaysh, pomocnym asystentem AI. Odpowiadaj jasno i zwięźle zgodnie z wykrytą kategorią."
        }
        
    def _truncate_prompt(self, prompt: str, max_length: int = 600) -> str:
        """Truncate prompt to max length."""
        return prompt[:max_length] if len(prompt) > max_length else prompt
        
    async def process_query(self, query: str, lang: str = 'en') -> Dict[str, Any]:
        """Process a user query and return a response."""
        try:
            # Detect category and get template
            category_result = detect_category(query)
            if category_result:
                category, template = category_result
                rewritten_prompt = template.format(target=query.strip())
            else:
                category = None
                rewritten_prompt = query.strip()
            
            # Prepare messages for API
            messages = [
                {"role": "system", "content": self.system_prompts[lang]},
                {"role": "user", "content": rewritten_prompt}
            ]
            
            # Call OpenRouter API
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": self.max_tokens,
                        "temperature": self.temperature,
                        "top_p": self.top_p
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"API error: {response.text}")
                    
                result = response.json()
                raw_response = result['choices'][0]['message']['content']
                
                # Clean the response
                cleaned_response = clean_gpt_reply(raw_response)
                
                # Get token usage
                usage = result.get('usage', {})
                tokens = {
                    "prompt": usage.get('prompt_tokens', 0),
                    "completion": usage.get('completion_tokens', 0),
                    "total": usage.get('total_tokens', 0)
                }
                
                return {
                    "response": cleaned_response,
                    "category": category,
                    "tokens": tokens
                }
                
        except Exception as e:
            print(f"Error in process_query: {str(e)}")
            return {
                "response": "I encountered an error. Please try again with a specific category.",
                "category": None,
                "error": str(e)
            } 