import json
import os
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)

class CategoryDetector:
    def __init__(self):
        self.categories: Dict[str, Dict[str, List[str]]] = {}
        self._load_categories()

    def _load_categories(self):
        """Load category keywords from JSON files."""
        try:
            categories_dir = os.path.join(os.path.dirname(__file__), '..', 'categories')
            for lang_file in os.listdir(categories_dir):
                if lang_file.endswith('.json'):
                    lang = lang_file.split('.')[0]
                    with open(os.path.join(categories_dir, lang_file), 'r', encoding='utf-8') as f:
                        self.categories[lang] = json.load(f)
            logger.info(f"Loaded categories for languages: {', '.join(self.categories.keys())}")
        except Exception as e:
            logger.error(f"Error loading categories: {str(e)}")
            # Fallback to empty dict if loading fails
            self.categories = {}

    def detect_category(self, text: str, lang: str = 'en') -> Optional[str]:
        """
        Detect the category of a text based on keywords.
        
        Args:
            text: The input text to analyze
            lang: The language code (default: 'en')
            
        Returns:
            Category name if detected, None otherwise
        """
        if not text:
            return None

        # Use English as fallback if requested language not available
        if lang not in self.categories:
            logger.warning(f"Language {lang} not found, falling back to English")
            lang = 'en'

        text = text.lower()
        categories = self.categories[lang]

        for category, keywords in categories.items():
            if any(keyword in text for keyword in keywords):
                logger.debug(f"Detected category '{category}' for text: {text[:50]}...")
                return category

        logger.debug(f"No category detected for text: {text[:50]}...")
        return None 