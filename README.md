[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ChayshOppa/Chaysh)

![Render Status](https://render.com/api/v1/services/chaysh/status.svg)

[Live Demo](https://chaysh.onrender.com/)

# Chaysh

A Flask-based AI assistant application that processes queries and generates structured responses.

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