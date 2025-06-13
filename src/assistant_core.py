from flask import session
from src.classifier import classify_prompt
from src.responder import generate_response
from src.suggester import suggest_next_prompts
from src.services.openrouter_service import call_openrouter_model, get_model_config

def generate_system_prompt_via_deepseek(user_prompt: str) -> tuple[str, str]:
    """Returns a tuple of (category, system_prompt) using DeepSeek"""
    config = get_model_config()
    model = config.get("classify", "deepseek/deepseek-r1-0528-qwen3-8b:free")

    categories = [
        "electronics", "travel", "legal", "health", "finance",
        "entertainment", "education", "gaming", "science", "general"
    ]
    system_prompt = (
        f"You are a categorization assistant.\n"
        f"Given the user input below, do two things:\n"
        f"1. Respond with the BEST category from this list: {', '.join(categories)}\n"
        f"2. Create a system prompt (for GPT) that would help answer that input effectively.\n\n"
        f"Format:\nCATEGORY: <category>\nPROMPT: <system prompt for GPT>\n\n"
        f"Input:\n{user_prompt}"
    )

    raw = call_openrouter_model(
        model=model,
        system_prompt="Respond in the above format.",
        user_prompt=user_prompt,
        temperature=0.3,
        max_tokens=300
    )

    # Parse format
    lines = raw.strip().splitlines()
    category = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("category:")), "unknown")
    prompt = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("prompt:")), "You are a helpful assistant.")
    
    print(f"[DeepSeek-CATEGORY] {category}")
    print(f"[DeepSeek-PROMPT] {prompt}")
    return category, prompt

def handle_assistant_request(user_prompt: str) -> dict:
    # Track last 3 prompts
    session.setdefault("last_prompts", [])
    session["last_prompts"].append(user_prompt)
    session["last_prompts"] = session["last_prompts"][-3:]

    # STEP 1: DeepSeek classification + GPT system prompt generation
    category, system_prompt = generate_system_prompt_via_deepseek(user_prompt)

    # STEP 2: GPT generates answer using DeepSeek's system prompt
    answer = generate_response(user_prompt, category, system_prompt)
    print(f"💬 GPT Response Preview: {answer[:100]}")

    # STEP 3: DeepSeek generates follow-up suggestions
    suggestions = suggest_next_prompts(session["last_prompts"])
    print(f"💡 Suggestions: {suggestions}")

    return {
        "category": category,
        "system_prompt": system_prompt,
        "response": answer,
        "suggestions": suggestions
    } 