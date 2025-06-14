"""
Core assistant functionality for Chaysh.
Handles prompt rewriting, context management, and response formatting.
"""

import os
import httpx
import logging
from typing import Dict, Any, List, Optional
from src.prompt_categories import detect_category, category_map
from src.utils.cleaner import clean_gpt_reply, format_table_response

# Configure logging
logger = logging.getLogger(__name__)

# Only load .env in development
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv
    load_dotenv()

# Get API key at module level
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise Exception("OPENROUTER_API_KEY not found")

class Assistant:
    def __init__(self):
        """Initialize the assistant with OpenRouter configuration."""
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
        
        # Log API key verification (first 4 chars only)
        if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
            logger.info(f"[Chaysh] API key: {api_key[:4]}... ✅")

    def _truncate_prompt(self, prompt: str, max_length: int = 600) -> str:
        """Truncate prompt to max length."""
        return prompt[:max_length] if len(prompt) > max_length else prompt

    def build_prompt(self, user_input: str, context: List[Dict[str, str]] = None, category_override: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Build a complete prompt with context and category-based rewriting.
        
        Args:
            user_input: The user's input message
            context: Optional conversation context
            category_override: Optional category to override auto-detection
            
        Returns:
            List of message dictionaries for the API
        """
        messages = []
        
        # Add conversation context if available (keep last 4 messages)
        if context:
            messages.extend(context[-4:])
        
        # Handle category detection or override
        if category_override and category_override in category_map:
            # Use override if valid category
            category = category_override
            template = category_map[category]["template"]
            rewritten_prompt = template.format(target=user_input.strip())
            if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                logger.debug(f"Category override: {category}")
        else:
            # Auto-detect category
            category_result = detect_category(user_input)
            if category_result:
                category, template = category_result
                rewritten_prompt = template.format(target=user_input.strip())
                if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                    logger.debug(f"Detected category: {category}")
            else:
                rewritten_prompt = user_input.strip()
                category = None
        
        messages.append({"role": "user", "content": rewritten_prompt})
        return messages

    async def get_response(
        self,
        user_input: str,
        context: List[Dict[str, str]] = None,
        category_override: Optional[str] = None,
        lang: str = 'en'
    ) -> Dict[str, Any]:
        """
        Get a response from the assistant.
        
        Args:
            user_input: The user's input message
            context: Optional conversation context
            category_override: Optional category to override auto-detection
            lang: Language code ('en' or 'pl')
            
        Returns:
            Dictionary containing response, context, and category
        """
        try:
            # Build the complete prompt
            messages = self.build_prompt(user_input, context, category_override)
            
            # Add system prompt
            messages.insert(0, {"role": "system", "content": self.system_prompts[lang]})
            
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
                
                # Log cleaned output in debug mode
                if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                    logger.debug(f"🧹 Cleaned GPT output: {cleaned_response}")
                
                # Format table response if needed
                if category_override in ["compare", "price"] or (category_result := detect_category(user_input)) and category_result[0] in ["compare", "price"]:
                    formatted_reply = format_table_response(cleaned_response)
                    if formatted_reply:
                        cleaned_response = formatted_reply
                
                # Get category from the last message
                category = None
                if messages[-1]["role"] == "user":
                    if category_override and category_override in category_map:
                        category = category_override
                    else:
                        category_result = detect_category(user_input)
                        category = category_result[0] if category_result else None
                
                # Update context with the new exchange (keep last 5 messages total)
                new_context = messages[-4:] + [{"role": "assistant", "content": cleaned_response}]
                
                # Get token usage
                usage = result.get('usage', {})
                tokens = {
                    "prompt": usage.get('prompt_tokens', 0),
                    "completion": usage.get('completion_tokens', 0),
                    "total": usage.get('total_tokens', 0)
                }
                
                # Log success in debug mode
                if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                    logger.debug(f"Category: {category}, Tokens: {tokens['total']}")
                
                return {
                    "response": cleaned_response,
                    "context": new_context,
                    "category": category,
                    "tokens": tokens if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes") else None
                }
                
        except Exception as e:
            # Log the error and return a user-friendly message
            logger.error(f"Error: {str(e)}")
            return {
                "response": "I encountered an error. Please try again with a specific category like 'compare' or 'price'.",
                "context": context or [],
                "category": None,
                "error": str(e) if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes") else None
            } 