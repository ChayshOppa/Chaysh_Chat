from app import create_app
from dotenv import load_dotenv
import os

# Load environment variables before creating the app
env_path = "F:/Chaysh/.env"
print(f"Loading environment from: {env_path}")
load_dotenv(env_path, override=True)

# Print environment variables for debugging
print("\nEnvironment variables at startup:")
for key, value in os.environ.items():
    if 'API' in key or 'KEY' in key:
        print(f"{key}: {value}")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 