import os
from dotenv import load_dotenv
import pathlib
import logging
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get absolute path to .env file
env_path = "F:/Chaysh/.env"  # Using forward slashes for Windows path
print(f"Loading .env from: {env_path}")

# Load environment variables
load_dotenv(env_path, override=True)

class Settings(BaseModel):
    # API Configuration
    OPENROUTER_API_KEY: str = os.getenv('OPENROUTER_API_KEY', '')
    OPENROUTER_API_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    
    # OpenAI Configuration (for assistant)
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 600
    OPENAI_TEMPERATURE: float = 0.7
    
    # Model settings
    DEFAULT_MODEL: str = "openai/gpt-3.5-turbo"
    MAX_TOKENS: int = 600  # Maximum tokens for detailed responses
    MIN_TOKENS: int = 300  # Minimum tokens for basic responses
    
    # Response structure
    RESPONSE_STRUCTURE: dict = {
        "mode": "product",
        "name": "",
        "description": [],
        "source_info": "",
        "suggestions": [],
        "actions": []
    }

# Create settings instance
settings = Settings()

# Log API key status (first 4 chars only for security)
if settings.OPENROUTER_API_KEY:
    logger.info(f"OpenRouter API Key loaded: {settings.OPENROUTER_API_KEY[:4]}...")
else:
    logger.warning("OPENROUTER_API_KEY not found in environment variables")

# For backward compatibility
Config = settings 