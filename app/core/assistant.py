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
from .config import settings
from src.prompt_categories import detect_category, DEFAULT_TIP, category_map

logger = logging.getLogger(__name__)

class Assistant:
    def __init__(self):
        """Initialize the assistant with OpenAI configuration."""
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
        
        # Log API key verification (first 4 chars only)
        if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
            logger.info(f"[Chaysh] Loaded API key: {settings.OPENAI_API_KEY[:4]}... ✅")

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
        
        # Add system tip if no context exists
        if not context:
            messages.append(DEFAULT_TIP)
        
        # Add conversation context if available
        if context:
            messages.extend(context)
        
        # Handle category detection or override
        if category_override and category_override in category_map:
            # Use override if valid category
            category = category_override
            template = category_map[category]["template"]
            rewritten_prompt = template.format(target=user_input)
            if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                logger.debug(f"Using category override: {category}")
        else:
            # Auto-detect category
            category_result = detect_category(user_input)
            if category_result:
                category, template = category_result
                rewritten_prompt = template.format(target=user_input)
                if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                    logger.debug(f"Detected category: {category}")
            else:
                rewritten_prompt = user_input
                category = None
        
        messages.append({"role": "user", "content": rewritten_prompt})
        return messages

    def clean_gpt_reply(self, reply: str) -> str:
        """
        Clean and format the GPT response.
        
        Args:
            reply: Raw response from GPT
            
        Returns:
            Cleaned response text
        """
        # Remove suggestion-style endings
        reply = re.sub(r'\n\nWould you like me to.*$', '', reply, flags=re.DOTALL)
        reply = re.sub(r'\n\nIs there anything else.*$', '', reply, flags=re.DOTALL)
        
        # Clean up any remaining whitespace
        reply = reply.strip()
        
        return reply

    def get_response(
        self,
        user_input: str,
        context: List[Dict[str, str]] = None,
        category_override: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get a response from the assistant.
        
        Args:
            user_input: The user's input message
            context: Optional conversation context
            category_override: Optional category to override auto-detection
            
        Returns:
            Dictionary containing response, context, tip, and category
        """
        try:
            # Build the complete prompt
            messages = self.build_prompt(user_input, context, category_override)
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract and clean the response
            reply = response.choices[0].message.content
            cleaned_reply = self.clean_gpt_reply(reply)
            
            # Get category from the last message
            category = None
            if messages[-1]["role"] == "user":
                if category_override and category_override in category_map:
                    category = category_override
                else:
                    category_result = detect_category(user_input)
                    category = category_result[0] if category_result else None
            
            # Update context with the new exchange
            new_context = messages + [{"role": "assistant", "content": cleaned_reply}]
            
            # Log success in debug mode
            if os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes"):
                logger.debug(f"Successfully generated response for category: {category}")
            
            return {
                "response": cleaned_reply,
                "context": new_context,
                "tip": DEFAULT_TIP if not context else None,
                "category": category
            }
            
        except Exception as e:
            # Log the error and return a user-friendly message
            logger.error(f"Error in get_response: {str(e)}")
            return {
                "response": "I apologize, but I encountered an error. Please try again.",
                "context": context or [],
                "tip": DEFAULT_TIP if not context else None,
                "category": None
            } 