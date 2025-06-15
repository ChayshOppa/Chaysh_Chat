[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ChayshOppa/Chaysh)

![Render Status](https://render.com/api/v1/services/chaysh/status.svg)

[Live Demo](https://chaysh.onrender.com/)

# Chaysh_Chat (v1.0)

Chaysh_Chat is a category-aware AI assistant frontend powered by OpenRouter + GPT 4.1-nano.

---

## 🚀 Features

- 🔍 **Category Detection**:  
  Automatically detects the user's intent (pricing, timeline, define, etc.) using multilingual keyword sets.

- 🧠 **Custom System Prompts**:  
  Injects dynamic system messages based on category to improve GPT response quality.

- 📦 **Keyword Logic from JSON**:  
  Category triggers are defined in editable files:  
  - `src/categories/en.json`  
  - `src/categories/pl.json`

- 🌍 **Multilingual**:  
  Detects categories using both English and Polish triggers.

- 🎨 **UI**:  
  - Simple, clean interface  
  - Working dark/light toggle  
  - Floating control menu  
  - Responsive on mobile and desktop

---

## 🔧 Current Deployment

- 🌐 Render URL: [https://chaysh-1.onrender.com](https://chaysh-1.onrender.com)
- 🧠 Model: `openai/gpt-4.1-nano` via OpenRouter
- ✅ API Key loaded and validated
- 🛠 Logs confirm backend prompt logic works per category

---

## 🗂 Structure

- `src/core/assistant.py`: OpenRouter handling + category prompt injection  
- `src/core/category_detector.py`: Keyword matcher for categories  
- `src/routes/chat.py`: Chat endpoint  
- `src/templates/chat.html`: Chat UI  
- `src/categories/`: Keyword triggers  
- `src/locales/`: UI translations

---

## ✅ Status: STABLE

This is the working release of `Chaysh_Chat v1.0`.

## 🧠 Project Summary
Chaysh is a lightweight Flask AI assistant deployed on Render. It uses OpenRouter and GPT-4.1 Nano to provide fast, cost-efficient answers and suggestions based on user input.

## ✅ Features
- Prompt and respond using `openai/gpt-4-1106-preview`
- Optimized for low token usage (600 input, 300 output)
- Auto-deployed via GitHub to Render
- Mobile/PC-friendly with simple UI
- Error handling + environment-based config
- Live link: [https://chaysh-1.onrender.com](https://chaysh-1.onrender.com)

## 🚀 Tech Stack
- Python 3.11 + Flask
- Gunicorn w/ UvicornWorker
- OpenRouter API
- Render for hosting
- JavaScript frontend with HTML/CSS

## 📁 Folder Structure
```
src/
├── core/
│   ├── assistant.py    # AI assistant implementation
│   └── __init__.py
├── templates/
│   └── chat.html      # Frontend interface
├── static/
│   └── styles.css     # Styling
└── main.py           # Flask application entry
```

## 🔧 Setup

### Local Development
1. Clone the repository:
```bash
git clone https://github.com/ChayshOppa/Chaysh.git
cd Chaysh
```

2. Create `.env` file:
```bash
OPENROUTER_API_KEY=your-key
SECRET_KEY=your-secret
FLASK_DEBUG=true
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run locally:
```bash
python src/main.py
```

### 🌍 Deployment
The app is configured for deployment on Render with:

1. `render.yaml` - Service configuration
2. `Procfile` - Process management
3. Environment variables managed via Render Secrets panel

The backend is deployed using:
```bash
gunicorn src.main:app -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT
```

## 🔒 Environment Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `SECRET_KEY`: Flask secret key
- `FLASK_DEBUG`: Set to true for development
- `MODEL`: AI model to use (default: mistral-7b-instruct)

## 📝 License
MIT License

## Features

- Clean, modern chat interface
- Real-time AI responses
- Smart suggestions
- Token-efficient processing
- Mobile-responsive design

## Technical Details

- **Assistant Model**: openai/gpt-4.1-nano via OpenRouter
- **Token Optimization**:
  - Input limit: 600 characters
  - Output limit: 300 characters
  - Temperature: 0.7 (balanced creativity)
  - Top-p: 0.9 (increased determinism)

## Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `FLASK_DEBUG`: Set to true for development
4. Run the app: `python src/main.py`

## Deployment

The app is configured for deployment on Render with:
- Python 3.11
- Gunicorn WSGI server
- Environment variable management
- Automatic HTTPS

## License

MIT License

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd chaysh
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```env
OPENROUTER_API_KEY=your-key-here
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

5. Run the application:
```bash
python run.py
```

The application will be available at http://localhost:5000

## Environment Variables

- `OPENROUTER_API_KEY`: Your OpenRouter API key (required)
- `FLASK_DEBUG`: Set to True for development mode
- `SECRET_KEY`: Flask secret key for session security

## Security Notes

- Never commit the `.env` file to version control
- Keep your API keys secure and rotate them regularly
- The application will fail to start if required environment variables are missing

## Deploying to Render

1. Fork this repository to your GitHub account
2. Create a new Web Service on Render and connect your repository
3. In the Render dashboard, set the following environment variables manually:
   - `OPENROUTER_API_KEY=your-production-key`
   - `SECRET_KEY=secure-app-key`
   - (Optional) `FLASK_DEBUG=false`
   - (Optional) `MODEL=mistral-7b-instruct`

The application will automatically deploy when you push changes to your repository. Render will use the environment variables set in the dashboard, so no `.env` file is needed in production.

### Environment Variable Handling

- Local Development: Uses `.env` file for configuration
- Production: Uses environment variables set in Render dashboard
- No code changes needed between environments
- Sensitive values are never committed to the repository 

# Chaysh Project Rules & Progress

## Project Rules

1. **Environment Variables**
   - Store sensitive keys (e.g., `OPENROUTER_API_KEY`) in a `.env` file at the project root.
   - Use `python-dotenv` to load environment variables in both development and production.

2. **API Integration**
   - The backend uses the OpenRouter API for AI-powered search.
   - The API key is required and must be valid for requests to succeed.

3. **Model Selection**
   - The default model is now `openai/gpt-3.5-turbo` (previously `anthropic/claude-3-opus:beta`).
   - To change the model, update `DEFAULT_MODEL` in `app/config.py`.

4. **Token and Character Limits**
   - `max_tokens` is set to the maximum allowed by your OpenRouter credits (currently 288).
   - The AI response is limited to 600 characters for the main description.
   - Suggestions are always included and are clickable.

5. **Frontend/Backend Interaction**
   - The frontend sends search queries to the Flask backend.
   - Clicking a suggestion triggers a new backend request using the suggestion as the new query.
   - All suggestions are guaranteed to work and generate new responses.

6. **Error Handling**
   - If the API returns a 402 error (insufficient credits), the backend will not attempt to exceed the allowed `max_tokens`.
   - The frontend should display a user-friendly message if credits are exhausted.

7. **Development Workflow**
   - All changes are saved and committed after successful testing.
   - The backend and frontend are kept in sync regarding API endpoints and expected data formats.

---

## Progress So Far

- Environment variable loading and debugging completed.
- `.env` file is now reliably loaded and used by the backend.
- OpenRouter API integration is working, with dynamic handling of token limits based on available credits.
- Model switched from Claude 3 to GPT-3.5-turbo for improved compatibility and cost control.
- Frontend search and clickable suggestions are fully functional.
- All suggestions now trigger new backend requests and generate new answers.
- Error handling for API credit limits is in place.
- Project rules and documentation updated to reflect current state and best practices.

---

For further changes, update this file and keep the rules and progress in sync with the codebase. 