import os
from dotenv import load_dotenv
import pathlib

# Get absolute path to .env file
env_path = "F:/Chaysh/.env"  # Using forward slashes for Windows path
print(f"Loading .env from: {env_path}")

# Load environment variables
load_dotenv(env_path, override=True)

class Config:
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    print(f"API Key loaded: {'Yes' if OPENROUTER_API_KEY else 'No'}")
    
    if not OPENROUTER_API_KEY:
        print("Warning: OPENROUTER_API_KEY not found in environment variables")
    else:
        print("OpenRouter API key loaded successfully")
        
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