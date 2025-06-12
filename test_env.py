import os
from dotenv import load_dotenv

# Try to read the file directly first
env_path = "F:/Chaysh/.env"
print(f"Testing .env file at: {env_path}")

try:
    with open(env_path, 'r', encoding='utf-8') as f:
        print("File contents:")
        print(f.read())
except Exception as e:
    print(f"Error reading file directly: {e}")

# Now try loading with python-dotenv
print("\nTrying to load with python-dotenv:")
load_dotenv(env_path, override=True)
print(f"OPENROUTER_API_KEY: {os.getenv('OPENROUTER_API_KEY')}") 