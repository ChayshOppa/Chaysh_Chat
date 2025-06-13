from flask import session
from src.classifier import classify_prompt
from src.responder import generate_response
from src.suggester import suggest_next_prompts

def handle_assistant_request(user_prompt: str) -> dict:
    # Store last 3 prompts
    session.setdefault("last_prompts", [])
    session["last_prompts"].append(user_prompt)
    session["last_prompts"] = session["last_prompts"][-3:]

    # Step 1: Categorize
    category = classify_prompt(user_prompt)

    # Step 2: Generate main answer
    answer = generate_response(user_prompt, category)

    # Step 3: Suggest next 3 prompts
    suggestions = suggest_next_prompts(session["last_prompts"])

    return {
        "category": category,
        "response": answer,
        "suggestions": suggestions
    } 