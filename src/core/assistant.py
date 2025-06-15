"""
Core assistant functionality for Chaysh.
Handles prompt rewriting, context management, and response formatting.
"""

import json
import re
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import openai
from src.config import settings
from src.prompt_categories import detect_category, category_map
from src.utils.cleaner import clean_gpt_reply, format_table_response

logger = logging.getLogger(__name__)

class Assistant:
    def __init__(self):
        """Initialize the assistant with OpenAI configuration."""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
        
        # Language-specific system prompts
        self.system_prompts = {
            'en': "You are Chaysh, a helpful AI assistant. Provide clear, concise responses based on the detected category.",
            'pl': "Jesteś Chaysh, pomocnym asystentem AI. Odpowiadaj jasno i zwięźle zgodnie z wykrytą kategorią."
        }
        
        # Log API key verification (first 4 chars only)
        if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
            logger.info(f"[Chaysh] API key: {settings.OPENAI_API_KEY[:4]}... ✅")

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

    def get_response(
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
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract and clean the response
            reply = response.choices[0].message.content
            cleaned_reply = clean_gpt_reply(reply)
            
            # Log cleaned output in debug mode
            if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                logger.debug(f"🧹 Cleaned GPT output: {cleaned_reply}")
            
            # Format table response if needed
            if category_override in ["compare", "price"] or (category_result := detect_category(user_input)) and category_result[0] in ["compare", "price"]:
                formatted_reply = format_table_response(cleaned_reply)
                if formatted_reply:
                    cleaned_reply = formatted_reply
            
            # Get category from the last message
            category = None
            if messages[-1]["role"] == "user":
                if category_override and category_override in category_map:
                    category = category_override
                else:
                    category_result = detect_category(user_input)
                    category = category_result[0] if category_result else None
            
            # Update context with the new exchange (keep last 5 messages total)
            new_context = messages[-4:] + [{"role": "assistant", "content": cleaned_reply}]
            
            # Get token usage
            usage = response.usage
            tokens = {
                "prompt": usage.prompt_tokens,
                "completion": usage.completion_tokens,
                "total": usage.total_tokens
            }
            
            # Log success in debug mode
            if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                logger.debug(f"Category: {category}, Tokens: {tokens['total']}")
            
            return {
                "response": cleaned_reply,
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