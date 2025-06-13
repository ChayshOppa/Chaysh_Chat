"""
Category-based prompt rewriting system for Chaysh assistant.
Defines categories, their keywords, and templates for prompt rewriting.
"""

from typing import Dict, Tuple, Optional

# Category configuration with templates and keywords
category_map: Dict[str, Dict] = {
    "weather": {
        "description": "Returns the current weather in a given location.",
        "template": "Get the current weather in {target}. Include temperature, humidity, and general conditions.",
        "keywords": ["weather", "forecast", "pogoda", "prognoza", "temperatura", "deszcz", "śnieg"]
    },
    "person": {
        "description": "Returns a short biography for a person.",
        "template": "Explain who {target} is. Provide a brief, relevant biography.",
        "keywords": ["who is", "kto to", "kim jest", "czy znasz", "biografia", "życiorys"]
    },
    "compare": {
        "description": "Compares two items or concepts side-by-side.",
        "template": "Compare {target} with a clear breakdown of features.",
        "keywords": ["compare", "porównaj", "powownaj", "różnice", "podobieństwa"]
    },
    "define": {
        "description": "Defines or explains a term clearly.",
        "template": "Give a concise definition of {target}.",
        "keywords": ["define", "what is", "co to", "opisz", "wyjaśnij", "znaczenie"]
    },
    "summary": {
        "description": "Summarizes input up to 500 characters, max 600 token output.",
        "template": "Summarize the following content: {target}. Use up to 600 tokens.",
        "keywords": ["summarize", "skroc", "skróć", "streść", "stresc", "podsumuj"]
    },
    "timeline": {
        "description": "Answers when something is happening or happened.",
        "template": "Tell when {target} is happening. Include name, date, and description if possible.",
        "keywords": ["when", "kiedy", "kiedy gra", "termin", "data", "godzina"]
    },
    "location": {
        "description": "Detects if a place (city/country/state) is mentioned and gives facts.",
        "template": "Provide useful facts and context about {target} as a place.",
        "keywords": ["where is", "gdzie jest", "lokalizacja", "miasto", "kraj"]
    },
    "price": {
        "description": "Compares prices or provides cost information.",
        "template": "Find and compare prices for {target}. Include current market rates if available.",
        "keywords": ["price", "cost", "cena", "koszt", "ile kosztuje", "cennik"]
    },
    "contact": {
        "description": "Provides contact information or communication details.",
        "template": "Find contact information for {target}. Include official channels if available.",
        "keywords": ["contact", "email", "phone", "kontakt", "telefon", "adres"]
    },
    "event": {
        "description": "Provides information about events, schedules, or timetables.",
        "template": "Find event details for {target}. Include date, time, and location if available.",
        "keywords": ["event", "schedule", "wydarzenie", "harmonogram", "terminarz"]
    }
}

def detect_category(prompt: str) -> Optional[Tuple[str, str]]:
    """
    Detect the category of a prompt based on keywords.
    
    Args:
        prompt: The user's input prompt
        
    Returns:
        Tuple of (category_name, template) if a category is detected, None otherwise
    """
    lowered = prompt.lower()
    
    # First check for exact keyword matches
    for category, config in category_map.items():
        for kw in config["keywords"]:
            if kw in lowered:
                return category, config["template"]
    
    # If no category is detected, return None
    return None

def get_category_examples() -> str:
    """
    Generate a formatted string of category examples for the system tip.
    
    Returns:
        Formatted string with category examples
    """
    examples = []
    for category, config in category_map.items():
        # Get first English and Polish keywords
        en_keywords = [k for k in config["keywords"] if not any(c in k for c in "ąćęłńóśźż")]
        pl_keywords = [k for k in config["keywords"] if any(c in k for c in "ąćęłńóśźż")]
        
        en_kw = en_keywords[0] if en_keywords else ""
        pl_kw = pl_keywords[0] if pl_keywords else ""
        
        if en_kw and pl_kw:
            examples.append(f"`{en_kw}` / `{pl_kw}` – {config['description']}")
    
    return "\n".join(examples)

# Default system tip with category examples
DEFAULT_TIP = {
    "role": "system",
    "content": (
        "💡 You can use these categories to get better responses:\n\n"
        f"{get_category_examples()}\n\n"
        "Just include one of these keywords in your question!"
    )
} 