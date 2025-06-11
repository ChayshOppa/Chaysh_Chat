import logging
import os
import json
import re
import httpx
from typing import Dict, Optional
from app.core.prompt import BASE_PROMPT

logger = logging.getLogger(__name__)

class Assistant:
    """AI Assistant for processing queries and generating structured responses."""
    
    def __init__(self):
        """Initialize the assistant with configuration."""
        self.mode = "product"  # Default mode as per project rules
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        flask_debug = os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes")

        if not self.api_key:
            print("[Chaysh] ❌ Missing OPENROUTER_API_KEY")
            raise ValueError("OPENROUTER_API_KEY is not set. Add it to your .env file for local development or as a secret in Render's dashboard.")
        elif flask_debug:
            print("[Chaysh] Loaded OPENROUTER_API_KEY ✅")
    
    async def process_query(self, query: str, context: Optional[Dict] = None, language: str = 'en') -> Dict:
        """
        Process a user query and return structured response.
        
        Args:
            query: User's search query
            context: Optional context from previous interactions
            language: Language code ('en' or 'pl')
            
        Returns:
            Dict containing structured response
        """
        # Real call to OpenRouter API
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        body = {
            "model": os.getenv("MODEL", "mistral-7b-instruct"),
            "messages": [
                {"role": "system", "content": BASE_PROMPT},
                {"role": "user", "content": query}
            ],
            "temperature": 0.7,
            "max_tokens": 400
        }
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)
                response.raise_for_status()
                raw_response = response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error("OpenRouter API request failed: %s", e)
            return self._get_fallback_response(query)

        flask_debug = os.getenv("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
        if flask_debug:
            logger.debug("Raw AI response: %s", raw_response)

        # Extract the first valid JSON object from the raw response
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', raw_response, re.DOTALL)
        if not json_match:
            logger.warning("No valid JSON found in raw response. Using fallback.")
            return self._get_fallback_response(query)

        try:
            parsed_json = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON from raw response. Using fallback.")
            return self._get_fallback_response(query)

        # Validate and ensure required fields
        validated_response = self._validate_response(parsed_json, query)
        if flask_debug:
            logger.debug("Parsed and validated JSON: %s", json.dumps(validated_response, indent=2))

        return validated_response

    def _validate_response(self, parsed_json: Dict, original_query: str) -> Dict:
        """Validate and ensure required fields in the parsed JSON response."""
        validated = {
            "name": parsed_json.get("name", "Unknown result"),
            "description": parsed_json.get("description", ["No information available."]),
            "source_info": parsed_json.get("source_info", "No source info."),
            "suggestions": parsed_json.get("suggestions", [])
        }
        # Ensure suggestions have at least a 'text' field
        validated["suggestions"] = [s for s in validated["suggestions"] if isinstance(s, dict) and "text" in s]
        # Inject default action if missing
        if "actions" not in parsed_json:
            validated["actions"] = [{"type": "chat", "label": "Chaysh Assistant", "query": original_query}]
        else:
            validated["actions"] = parsed_json["actions"]
        return validated

    def _get_fallback_response(self, query: str) -> Dict:
        """Return a fallback response if parsing fails."""
        return {
            "name": "Unknown result",
            "description": ["No information available."],
            "source_info": "No source info.",
            "suggestions": [],
            "actions": [{"type": "chat", "label": "Chaysh Assistant", "query": query}]
        } 