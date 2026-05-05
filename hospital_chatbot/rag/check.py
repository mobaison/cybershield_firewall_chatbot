"""
check_models.py — Run this to find your exact available model names.
Usage: python check_models.py
"""
import os, requests
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("GOOGLE_API_KEY")
if not key:
    print("ERROR: GOOGLE_API_KEY not found in .env"); exit(1)

for version in ["v1", "v1beta"]:
    url = f"https://generativelanguage.googleapis.com/{version}/models?key={key}"
    r = requests.get(url, timeout=10)
    data = r.json()
    if "error" in data:
        print(f"[{version}] Error: {data['error']['message']}")
        continue

    models = data.get("models", [])
    embed = [m["name"] for m in models if "embedContent" in m.get("supportedGenerationMethods", [])]
    gen   = [m["name"] for m in models if "generateContent" in m.get("supportedGenerationMethods", [])]

    print(f"\n=== {version} EMBEDDING models ===")
    for n in embed: print(f"  {n}")

    print(f"\n=== {version} GENERATION models ===")
    for n in gen: print(f"  {n}")