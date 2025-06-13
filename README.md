[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/ChayshOppa/Chaysh)

![Render Status](https://render.com/api/v1/services/chaysh/status.svg)

[Live Demo](https://chaysh-1.onrender.com/)

# Chaysh AI Assistant

## 🧠 Project Summary
Chaysh is a lightweight Flask AI assistant deployed on Render. It uses OpenRouter and GPT models to provide fast, cost-efficient answers and suggestions based on user input.

## ✅ Features
- Clean, modern chat interface
- Real-time AI responses
- Smart suggestions
- Token-efficient processing
- Mobile-responsive design
- Error handling + environment-based config

## 🚀 Tech Stack
- Python 3.11 + Flask
- Gunicorn w/ UvicornWorker
- OpenRouter API
- Render for hosting
- JavaScript frontend with HTML/CSS

## 📁 Project Structure
The project is organized into two main directories:

```
app/                    # Main application directory
├── core/              # Core functionality
├── routes/            # API routes and endpoints
├── services/          # Business logic and services
├── static/            # Static assets (CSS, JS)
├── templates/         # HTML templates
├── config.py          # Configuration settings
└── __init__.py       # Application initialization

src/                   # Legacy/backup code
├── core/             # Core functionality
├── templates/        # HTML templates
├── main.py          # Flask application entry
└── __init__.py      # Package initialization
```

## 🔧 Setup

### Local Development
1. Clone the repository:
```bash
git clone https://github.com/ChayshOppa/Chaysh.git
cd Chaysh
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Create `.env` file:
```bash
OPENROUTER_API_KEY=your-key
SECRET_KEY=your-secret
FLASK_DEBUG=true
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run locally:
```bash
python app/__init__.py
```

### 🌍 Deployment
The app is configured for deployment on Render with:

1. `render.yaml` - Service configuration
2. `Procfile` - Process management
3. Environment variables managed via Render Secrets panel

## 🔒 Environment Variables
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `SECRET_KEY`: Flask secret key
- `FLASK_DEBUG`: Set to true for development
- `MODEL`: AI model to use (default: mistral-7b-instruct)

## 📝 License
MIT License

## Security Notes

- Never commit the `.env` file to version control
- Keep your API keys secure and rotate them regularly
- The application will fail to start if required environment variables are missing

## Development Guidelines

1. **Environment Variables**
   - Store sensitive keys in `.env` file
   - Use `python-dotenv` for loading environment variables
   - Never commit sensitive data to version control

2. **API Integration**
   - Uses OpenRouter API for AI-powered responses
   - Implements proper error handling and rate limiting
   - Maintains token efficiency

3. **Code Organization**
   - Follow the established project structure
   - Keep UI components consistent with deployed version
   - Maintain separation of concerns between modules

4. **Testing & Deployment**
   - Test locally before pushing changes
   - Verify environment variables are properly set
   - Monitor API usage and token consumption

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and feature requests, please use the GitHub issue tracker. 