import json
from src.services.openrouter_service import call_openrouter_model

CATEGORIES_FILE = "src/core/categories.json"

def get_available_categories():
    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def classify_prompt(prompt: str):
    categories = get_available_categories()
    category_labels = list(categories.keys())

    system_prompt = (
        "You are a category classifier. Given the user prompt, "
        f"choose the best matching category from this list only:\n{category_labels}\n\n"
        "Respond with only one category name. If uncertain, say 'unknown'."
    )

    result = call_openrouter_model(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        system_prompt=system_prompt,
        user_prompt=prompt,
        max_tokens=10,
        temperature=0.3
    )

    return result.strip().lower() 