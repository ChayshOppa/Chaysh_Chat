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

def detect_category(prompt: str) -> tuple[str, str] | None:
    lowered = prompt.lower()
    for category, config in category_map.items():
        for kw in config["keywords"]:
            if kw in lowered:
                return category, config["template"]
    return None 