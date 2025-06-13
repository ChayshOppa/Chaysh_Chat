import os
import json
from src.services.openrouter_service import call_openrouter_model, get_model_config

CATEGORIES_PATH = "src/core/categories.json"

def load_categories():
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return list(json.load(f).keys())

def classify_prompt(prompt: str) -> str:
    config = get_model_config()
    model = config.get("classify", "deepseek/deepseek-r1-0528-qwen3-8b:free")
    categories = load_categories()

    system_prompt = (
        "You are a strict category classifier. "
        "Choose ONE category that best matches the user request from:\n"
        f"{', '.join(categories)}\n\n"
        "If nothing fits, respond only with 'unknown'."
    )

    return call_openrouter_model(
        model=model,
        system_prompt=system_prompt,
        user_prompt=prompt,
        max_tokens=10,
        temperature=0.3
    ).strip().lower() 