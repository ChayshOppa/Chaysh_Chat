import json
from src.services.openrouter_service import call_openrouter_model

PROMPT_TEMPLATE_PATH = "src/core/category_prompts.json"

def load_prompt_templates():
    with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_response(prompt: str, category: str) -> str:
    templates = load_prompt_templates()
    system_prompt = templates.get(category, templates.get("default"))

    response = call_openrouter_model(
        model="openai/gpt-4.1-nano",
        system_prompt=system_prompt,
        user_prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )

    return response.strip() 