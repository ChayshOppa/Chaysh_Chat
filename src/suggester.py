from src.services.openrouter_service import call_openrouter_model

def suggest_next_prompts(last_prompts: list[str]) -> list[str]:
    context = "\n".join(last_prompts[-3:])

    system_prompt = (
        "Based on the user's recent conversation:\n"
        f"{context}\n\n"
        "Suggest 3 specific, helpful follow-up questions they might want to ask next. "
        "Only return the suggestions as a list."
    )

    raw_output = call_openrouter_model(
        model="deepseek/deepseek-r1-0528-qwen3-8b:free",
        system_prompt=system_prompt,
        user_prompt="What should I ask next?",
        temperature=0.4,
        max_tokens=120
    )

    return [s.strip("-• ") for s in raw_output.strip().split("\n") if s.strip()] 