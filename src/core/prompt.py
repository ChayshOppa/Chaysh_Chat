from typing import Optional, Tuple

category_map = {
    "price": {
        "description": "Generate price comparisons or diagrams of up to 5 variants.",
        "template": "Create a list or diagram (or both) of prices for {target}. Use up to 500 tokens for explanation. No character limit for output.",
        "keywords": ["price", "cost", "value", "worth", "cena", "koszt", "wartość"]
    },
    "event": {
        "description": "Find information about the next event including time, place, and name.",
        "template": "Check soonest event that {target} will attend or organize. Include the event name, date, location, and a short context if available.",
        "keywords": [
            "event", "match", "concert", "game", "festival", "fight", "tournament", "wydarzenie",
            "mecz", "koncert", "turniej", "kiedy", "kiedy gra", "kiedy będzie"
        ]
    }
}

def detect_category(prompt: str) -> Optional[Tuple[str, str]]:
    lowered = prompt.lower()
    for category, config in category_map.items():
        for kw in config["keywords"]:
            if kw in lowered:
                return category, config["template"]
    return None

def build_prompt(user_input: str) -> str:
    result = detect_category(user_input)
    if result:
        category, template = result
        # Clean category word from input to isolate the target
        cleaned = user_input.replace(category, "", 1).strip()
        return template.format(target=cleaned)
    return user_input

BASE_PROMPT = """You are a structured assistant that provides accurate and concise information about products and manuals.
Your task is to analyze the user's query and generate a structured response in JSON format.

Rules:
1. Focus on product-related queries
2. Keep responses concise (40-400 tokens)
3. Be honest if unsure
4. No jokes or slang
5. Use a balanced, expert tone
6. Ignore illegal/unsafe topics
7. Request clarification for vague inputs

Required JSON structure:
{
  "mode": "product",
  "name": "Product name or query topic",
  "description": [
    "What it is",
    "Key features",
    "Public opinion",
    "Recent updates",
    "Final summary"
  ],
  "source_info": "Source attribution",
  "suggestions": [
    {"text": "Related query", "category": "comparison|spec|help"}
  ],
  "actions": [
    {"type": "chat", "label": "Ask More", "query": "Follow-up question"}
  ]
}

If the query is unclear or unsafe, return a fallback response:
{
  "mode": "fallback",
  "name": "Unknown topic",
  "description": ["I couldn't understand your query."],
  "source_info": "No matching logic",
  "suggestions": [
    {"text": "Try asking about a product", "category": "help"}
  ],
  "actions": []
}

Always respond in valid JSON format. Never output plain text or markdown."""

DEFAULT_TIP = {
    "role": "system",
    "content": (
        "💡 You should provide a category or description of what you're looking for to have a better experience.\n\n"
        "**Examples:**\n"
        "`price` – for product comparisons\n"
        "`event` or `timetable` (Polish: kiedy gra / kiedy będzie) – for sports, music, or game schedules\n"
        "`compare`, `define`, `summary`, `contact`, etc."
    )
} 