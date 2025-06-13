from flask import session
from src.classifier import classify_prompt
from src.responder import generate_response
from src.suggester import suggest_next_prompts

def handle_assistant_request(user_prompt: str) -> dict:
    # Track last 3 prompts
    session.setdefault("last_prompts", [])
    session["last_prompts"].append(user_prompt)
    session["last_prompts"] = session["last_prompts"][-3:]

    # Step 1: Classify via DeepSeek
    category = classify_prompt(user_prompt)
    print(f"🧠 Detected Category: {category}")

    # Step 2: Get GPT-4.1 response
    answer = generate_response(user_prompt, category)
    print(f"💬 GPT Response Preview: {answer[:100]}")

    # Step 3: Suggest next prompts via DeepSeek
    suggestions = suggest_next_prompts(session["last_prompts"])
    print(f"💡 Suggestions: {suggestions}")

    return {
        "category": category,
        "response": answer,
        "suggestions": suggestions
    } 