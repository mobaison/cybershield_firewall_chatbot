# debug_env.py
import os
from pathlib import Path

print("Current working directory:", os.getcwd())
print("Script location:", Path(__file__).parent)

# Check if .env exists
env_path = Path(".env")
print(f".env exists: {env_path.exists()}")

if env_path.exists():
    print("\n.env content (first 20 chars):")
    with open(".env", "r") as f:
        content = f.read().strip()
        print(f"First 20 chars: {content[:20]}...")
        print(f"Length: {len(content)}")
        print(f"Contains '=': {'=' in content}")
        
        # Check for quotes
        if '"' in content:
            print("⚠️ WARNING: .env contains double quotes!")
        if "'" in content:
            print("⚠️ WARNING: .env contains single quotes!")
        if " " in content:
            print("⚠️ WARNING: .env contains spaces!")
else:
    print("❌ .env file not found!")

# Try loading with dotenv
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
print(f"\nAPI key loaded: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API key starts with: {api_key[:15]}...")
    print(f"API key length: {len(api_key)}")
    print(f"Valid format: {api_key.startswith('AIzaSy') }")
else:
    print("❌ API key not loaded!")