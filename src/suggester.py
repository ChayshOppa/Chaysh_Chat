from src.services.openrouter_service import call_openrouter_model, get_model_config

def suggest_next_prompts(last_prompts: list[str]) -> list[str]:
    context = "\n".join(last_prompts[-3:])
    config = get_model_config()
    model = config.get("suggest", "deepseek/deepseek-r1-0528-qwen3-8b:free")
    print(f"[Suggester] Model selected: {model}")

    system_prompt = (
        "Based on the user's recent conversation:\n"
        f"{context}\n\n"
        "Suggest 3 helpful, specific follow-up questions. Only return the list."
    )

    raw_output = call_openrouter_model(
        model=model,
        system_prompt=system_prompt,
        user_prompt="What should I ask next?",
        temperature=0.5,
        max_tokens=150
    )

    return [line.strip("-• ").strip() for line in raw_output.strip().split("\n") if line.strip()] 