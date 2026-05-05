"""
rag/gemini_client.py - Gemini LLM via Google REST API
======================================================
Handles 429 rate-limit errors with exponential backoff retry.
Also tries multiple models in order if one is quota-exhausted.
"""

import os, time, requests

# Priority order — if 2.0-flash is quota-exhausted, falls back down the list
PREFERRED_GEN_MODELS = [
    "models/gemini-2.0-flash",
    "models/gemini-2.0-flash-lite",
    "models/gemini-2.5-flash-lite",
    "models/gemini-1.5-flash",
    "models/gemini-pro",
]

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not set in .env file.")
        self.base  = None
        self.model = None
        self._discover()
        print(f"✅ Gemini client ready  model={self.model}  api={self.base}")

    def _discover(self):
        for version in ["v1", "v1beta"]:
            url  = f"https://generativelanguage.googleapis.com/{version}/models"
            resp = requests.get(url, params={"key": self.api_key}, timeout=10)
            if resp.status_code != 200:
                continue
            available = {
                m["name"]
                for m in resp.json().get("models", [])
                if "generateContent" in m.get("supportedGenerationMethods", [])
            }
            for candidate in PREFERRED_GEN_MODELS:
                if candidate in available:
                    self.base  = version
                    self.model = candidate
                    return
        raise RuntimeError("No Gemini model found. Run: python check_models.py")

    def _make_url(self, model_name):
        model_id = model_name.split("/")[-1]
        return (
            f"https://generativelanguage.googleapis.com/{self.base}"
            f"/models/{model_id}:generateContent"
        )

    def _post(self, model_name, payload, timeout=60):
        """Single POST attempt, returns (status_code, response_dict)."""
        r = requests.post(
            self._make_url(model_name),
            params={"key": self.api_key},
            json=payload,
            timeout=timeout,
        )
        return r.status_code, r.json()

    def generate(self, prompt: str) -> str:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "topP": 0.85,
                "topK": 40,
                "maxOutputTokens": 1024,
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT",        "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH",       "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
            ],
        }

        # ── Step 1: retry current model with exponential backoff ──────────
        for attempt in range(4):          # attempts: 0,1,2,3
            status, data = self._post(self.model, payload)

            if status == 200:
                return self._extract_text(data)

            if status == 429:
                wait = 2 ** attempt       # 1s, 2s, 4s, 8s
                print(f"⚠️  Gemini 429 rate-limit on {self.model} "
                      f"(attempt {attempt+1}/4) — waiting {wait}s...")
                time.sleep(wait)
                continue

            # Non-429 error — no point retrying same model
            print(f"Gemini {status} on {self.model}: {str(data)[:200]}")
            break

        # ── Step 2: try fallback models ───────────────────────────────────
        print("⚠️  Primary model failed — trying fallback models...")
        for fallback in PREFERRED_GEN_MODELS:
            if fallback == self.model:
                continue                  # already tried this one
            print(f"   Trying {fallback}...")
            status, data = self._post(fallback, payload)
            if status == 200:
                print(f"   ✅ Fallback succeeded with {fallback}")
                return self._extract_text(data)
            if status == 429:
                print(f"   429 on {fallback} too — skipping")
                time.sleep(1)
            else:
                print(f"   {status} on {fallback}")

        return self._fallback_msg()

    def _extract_text(self, data: dict) -> str:
        candidates = data.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", self._fallback_msg())
        return self._fallback_msg()

    def _fallback_msg(self):
        return (
            "I'm currently experiencing high traffic and couldn't generate a response. "
            "Please try again in a moment, or call City General Hospital at +1-800-HOSPITAL."
        )