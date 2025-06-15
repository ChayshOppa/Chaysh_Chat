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
from .category_detector import CategoryDetector

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

        self.category_detector = CategoryDetector()

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

    async def get_response(self, user_input: str, context: list = None, category_override: str = None, lang: str = 'en') -> Dict[str, Any]:
        """
        Get a response from the assistant.
        
        Args:
            user_input: The user's input text
            context: Optional list of previous messages for context
            category_override: Optional category to force
            lang: Language code for category detection
            
        Returns:
            Dictionary containing the response and metadata
        """
        try:
            # Detect category if not overridden
            category = category_override or self.category_detector.detect_category(user_input, lang)
            logger.info(f"Detected category: {category} for input: {user_input[:50]}...")

            # Get response from OpenRouter
            from ..services.openrouter_service import OpenRouterService
            openrouter = OpenRouterService()
            response = await openrouter.get_ai_response(user_input)

            # Add category to response if detected
            if category:
                response['category'] = category

            return response

        except Exception as e:
            logger.error(f"Error in get_response: {str(e)}")
            return {
                'error': 'An error occurred while processing your request',
                'category': None
            } 