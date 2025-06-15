# Cursor Rules for Chaysh AI Project

## 🔐 SECURITY
- Never push `.env` or any other secret configuration file to GitHub.
- Always use `os.getenv()` or a Config class to load environment variables.
- Local `.env` should be ignored via `.gitignore`.

## 📁 PROJECT STRUCTURE
- Code is currently split between:
  - `src/` (main functional core)
  - `app/` (UI and web serving logic)

Do not assume one structure. Respect both folders unless we explicitly migrate or merge them.

## 🎨 STYLING
- Do **not** touch or reset existing base CSS/JS styling.
- Avoid changing UI layout, dark/light modes, borders, or card categories.
- Any component that deals with chat, search, or layout blocks must **preserve the visual design** from the current deployed version: https://chaysh-1.onrender.com/

## 🛠 DEVELOPMENT FLOW
- All API keys should be loaded using environment variables only.
- Local development uses `.env`, production uses Render Environment tab.
- When creating logs, show only the first 4–6 characters of API keys for verification.
- Model switching (e.g. OpenRouter models) must use variables, not hardcoded strings.

## 🧪 TESTING + LOGGING
- Any feature involving API calls must log success/failure clearly in dev mode.
- Add fallback responses only when API is unreachable or unauthorized.

## 🧭 ASSISTANT BEHAVIOR
- Chaysh is an AI-powered assistant. It must return clear, formatted, structured answers.
- All future assistant logic should stay token-efficient and avoid verbose or bloated output.

## 🚫 NEVER DO THIS
- Never hardcode secrets or keys.
- Never overwrite `.env` or `.gitignore`.
- Never change default styling, layout, or category behavior unless explicitly requested.
- Never push unfinished or test keys/models to GitHub.
- Never push cursor-rules.md and Chaysh.zip if existing to github.