import json
from src.services.openrouter_service import call_openrouter_model, get_model_config

PROMPT_TEMPLATE_PATH = "src/core/category_prompts.json"

def load_prompt_templates():
    with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_response(user_prompt: str, category: str, system_prompt: str) -> str:
    config = get_model_config()
    model = config.get("respond", "openai/gpt-4.1-nano")

    return call_openrouter_model(
        model=model,
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        temperature=0.6,
        max_tokens=500
    ) 