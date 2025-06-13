import os, requests, json

def get_model_config():
    with open("src/core/models.json", "r", encoding="utf-8") as f:
        return json.load(f)

def call_openrouter_model(model=None, system_prompt="", user_prompt="", temperature=0.7, max_tokens=300):
    config = get_model_config()

    selected_model = model or config.get("default", "openai/gpt-4.1-nano")

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://chaysh-1.onrender.com",
        "Content-Type": "application/json",
    }

    payload = {
        "model": selected_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        print(f"[OpenRouter] ✅ Model used: {selected_model}")
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[OpenRouter ERROR] ❌ Model failed: {selected_model} → {e}")
        return "Sorry, the assistant is having trouble responding right now." 