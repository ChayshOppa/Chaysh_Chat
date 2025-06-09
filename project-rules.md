# Cursor Project Rules (v2 - June 2025)

## 🧠 Project Purpose

Cursor is a code-generation assistant tool that builds and updates a Python Flask web application. The final product is a web and mobile-friendly AI search engine that:

* Accepts natural language input like ChatGPT
* Returns structured, helpful answers
* Uses OpenRouter API as the backend AI model
* Provides categorized, token-efficient, suggestion-rich responses

Cursor only writes files — it does not execute logic or answer users.

---

## 🎯 Assistant Behavior (Inside Flask)

### Default Flow:

1. User enters any prompt.
2. Assistant tries to identify: What is the query about?
3. It builds a structured AI prompt and sends it to OpenRouter.
4. Receives structured JSON in return.
5. Returns formatted, styled answer blocks.

### Query Types (Future Modes):

* Product → specs, models, reviews
* Person → bio, events, news
* Place → highlights, travel tips, seasons
* Concept → explanation, opinions, applications

For now: **Focus on products only**.

---

## 📦 Assistant Output Format (JSON)

```json
{
  "mode": "product",        // optional for future
  "name": "iPhone 14 Pro",
  "description": [
    "What it is",
    "Public opinion",
    "Recent update",
    "Extra insight",
    "Final summary"
  ],
  "source_info": "Compiled from Apple.com and tech sources",
  "suggestions": [
    {"text": "Compare with iPhone 15", "category": "comparison"},
    {"text": "See camera details", "category": "spec"}
  ],
  "actions": [
    {"type": "chat", "label": "Ask More", "query": "Battery life?"}
  ]
}
```

Always return valid JSON. Never return Markdown, HTML, or plain text.

---

## 🌍 Language

* Detect input language automatically
* Default support: English 🇬🇧 and Polish 🇵🇱 (menu toggles)
* User can type: "change language to Polish"
* All answers respond in the detected/requested language

---

## 🧠 Tone

* Balanced: expert but not robotic
* Honest if unsure
* No jokes, slang, or fluff
* Compact but useful

---

## ✂️ Restrictions & Token Logic

* Ignore illegal or unsafe topics; respond with warning
* Suggest clarification for vague inputs
* Limit tokens per response: **40–400**, dynamically estimated
* Long/complex answers include message: “This is a big topic...”
* Invalid or empty queries return fallback message

---

## 🖼️ Display Rules

* All responses shown as **elegant card blocks**
* Styling based on [https://www.grzegorzbartos.pl/](https://www.grzegorzbartos.pl/)
* Cards use nested box layout with readable contrast
* Mobile-first layout, grid expansion on desktop
* Light/dark toggle in top corner

---

## 🧰 Dev Stack Summary

* Backend: Python Flask
* Frontend: HTML + Tailwind CSS
* AI: OpenRouter (GPT-3.5 / Claude 3)
* Hosting: Render (via render.yaml)
* Memory: JavaScript localStorage (future: DB)
* API keys: Loaded via `.env` or Render Secrets

---

## 🧠 Prompt System Logic

System prompt (in `assistant.py`) will always:

* Classify the query
* Pick the best mode (`product` for now)
* Request short, clear, structured response
* Warn about vague or risky queries
* Return fallback structure on AI failure

Sample internal system prompt:

```
You are a structured assistant. Identify the topic and generate up to 5 short insights about it.
Respond only in the JSON format shown. Never output plain text or markdown. If the prompt is vague, request clarification.
```

---

## 🔁 Cursor's Role

Cursor only generates files — it does not respond to user prompts.
You (ChatGPT) are the planner, prompt engineer, and memory keeper.
The Flask app is the actual assistant.

All future logic updates will be documented in this file.

---

## ✅ Initial Logic Locked

You may now begin creating the base Flask app using this structure.
