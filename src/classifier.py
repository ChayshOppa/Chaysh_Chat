import os
import json
from src.services.openrouter_service import call_openrouter_model

CATEGORIES_PATH = "src/core/categories.json"

def load_categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return list(json.load(f).keys())

def classify_prompt(prompt: str) -> str:
    categories = load_categories()
    system_prompt = (
        "You are a strict category classifier. "
        "Choose ONE category from the list below that best fits the user input:\n"
        f"{', '.join(categories)}\n\n"
        "If none apply, respond only with 'unknown'."
    )

    response = call_openrouter_model(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        system_prompt=system_prompt,
        user_prompt=prompt,
        max_tokens=10,
        temperature=0.2
    )

    return response.strip().lower() 