import os
from dotenv import load_dotenv
import pathlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get absolute path to .env file
env_path = "F:/Chaysh/.env"  # Using forward slashes for Windows path
print(f"Loading .env from: {env_path}")

# Load environment variables
load_dotenv(env_path, override=True)

class Config:
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    
    # Log API key status (first 4 chars only for security)
    if OPENROUTER_API_KEY:
        logger.info(f"OpenRouter API Key loaded: {OPENROUTER_API_KEY[:4]}...")
    else:
        logger.warning("OPENROUTER_API_KEY not found in environment variables")
        
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    # Default model settings
    DEFAULT_MODEL = "openai/gpt-3.5-turbo"
    MAX_TOKENS = 600  # Maximum tokens for detailed responses
    MIN_TOKENS = 300  # Minimum tokens for basic responses
    
    # Response structure
    RESPONSE_STRUCTURE = {
        "mode": "product",
        "name": "",
        "description": [],
        "source_info": "",
        "suggestions": [],
        "actions": []
    } 