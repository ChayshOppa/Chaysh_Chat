import json
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def detect_category(prompt: str, lang: str = "en") -> tuple[str, str]:
    """
    Detect the category of a user prompt based on keywords.
    
    Args:
        prompt (str): The user's input text
        lang (str): Language code ('en' or 'pl')
        
    Returns:
        tuple[str, str]: (category, focus) where category is the detected category
        and focus is the main subject of the query
    """
    try:
        category_file = Path(f"src/categories/{lang}.json")
        if not category_file.exists():
            logger.warning(f"Category file for {lang} not found, falling back to English")
            category_file = Path("src/categories/en.json")
            
        keywords = json.loads(category_file.read_text(encoding="utf-8"))
        lower_prompt = prompt.lower()

        for category, keys in keywords.items():
            for key in keys:
                if key in lower_prompt:
                    words = prompt.split()
                    focus = words[-1]  # fallback logic
                    logger.info(f"Detected category: {category} for prompt: {prompt}")
                    return category, focus
                    
        logger.info(f"No category detected for prompt: {prompt}")
        return None, prompt
        
    except Exception as e:
        logger.error(f"Error detecting category: {str(e)}")
        return None, prompt 