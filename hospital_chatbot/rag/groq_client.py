"""
rag/groq_client.py - Groq LLM Client (Primary Response Generator)
==================================================================
WHY GROQ FOR RESPONSES:
  - Free tier: 14,400 requests/day (~10x more than Gemini's 1,500/day)
  - Speed: Groq runs on custom LPU hardware — 5-10x faster than Gemini
  - Models: llama-3.3-70b, mixtral-8x7b, gemma2-9b all available free
  - REST API: simple JSON, no SDK needed

FREE TIER LIMITS (as of 2025):
  Model                  | RPM  | RPD    | TPM
  ───────────────────────┼──────┼────────┼──────────
  llama-3.3-70b-versatile| 30   | 14,400 | 131,072
  llama-3.1-8b-instant   | 30   | 14,400 | 131,072
  mixtral-8x7b-32768     | 30   | 14,400 | 131,072
  gemma2-9b-it           | 30   | 14,400 | 131,072

DUAL API STRATEGY:
  Gemini API → Embedding only (RAG retrieval phase)
  Groq API   → Response generation (answer phase)

  Result: Gemini's 1,500 req/day limit only applies to EMBEDDING (1 call/msg)
          Groq's  14,400 req/day limit applies to GENERATION (1 call/msg)
          Combined effective capacity: ~14,400 full messages/day (10x improvement)

Get your free Groq API key at: https://console.groq.com
"""

import os, time, requests
from typing import Optional

GROQ_API_BASE = "https://api.groq.com/openai/v1/chat/completions"

# Priority order — first available wins, falls down on 429
PREFERRED_GROQ_MODELS = [
    "llama-3.3-70b-versatile",    # Best quality, 70B params, free tier
    "llama-3.1-70b-versatile",    # Fallback 70B
    "llama-3.1-8b-instant",       # Faster, lighter, still very capable
    "mixtral-8x7b-32768",         # Good alternative
    "gemma2-9b-it",               # Google's Gemma on Groq infra
]


class GroqClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not set in .env file.\n"
                "Get your free key at: https://console.groq.com"
            )
        self.model = self._discover()
        print(f"✅ Groq client ready  model={self.model}")

    def _discover(self) -> str:
        """
        Query Groq's model list and pick the best available model.
        Falls back to first preferred model if list API fails.
        """
        try:
            resp = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10,
            )
            if resp.status_code == 200:
                available = {m["id"] for m in resp.json().get("data", [])}
                for candidate in PREFERRED_GROQ_MODELS:
                    if candidate in available:
                        return candidate
        except Exception as e:
            print(f"  Groq model discovery warning: {e}")

        # Default to best model without verification
        return PREFERRED_GROQ_MODELS[0]

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """
        Send prompt to Groq and return the answer.
        Uses OpenAI-compatible chat completions format.

        Args:
            prompt:        The user/context message (assembled RAG prompt)
            system_prompt: Optional separate system message for cleaner separation
        """
        # Build messages in OpenAI chat format
        # Groq uses roles: system / user / assistant
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user",   "content": prompt})
        else:
            # If no separate system prompt, send everything as user message
            messages.append({"role": "user", "content": prompt})

        payload = {
            "model"      : self.model,
            "messages"   : messages,
            "temperature": 0.3,       # Low = factual, grounded responses
            "max_tokens" : 1024,
            "top_p"      : 0.85,
            "stream"     : False,
        }

        # Retry with exponential backoff on 429
        for attempt in range(4):
            status, data = self._post(self.model, payload)

            if status == 200:
                return self._extract(data)

            if status == 429:
                wait = 2 ** attempt   # 1s, 2s, 4s, 8s
                print(f"⚠️  Groq 429 on {self.model} "
                      f"(attempt {attempt+1}/4) — waiting {wait}s...")
                time.sleep(wait)
                continue

            # Other error — try next model
            print(f"Groq {status} on {self.model}: {str(data)[:200]}")
            break

        # Try fallback models
        print("⚠️  Primary Groq model failed — trying fallbacks...")
        for fallback in PREFERRED_GROQ_MODELS:
            if fallback == self.model:
                continue
            print(f"   Trying Groq model: {fallback}...")
            payload["model"] = fallback
            status, data = self._post(fallback, payload)
            if status == 200:
                print(f"   ✅ Groq fallback succeeded: {fallback}")
                return self._extract(data)
            if status == 429:
                print(f"   429 on {fallback} — skipping")
                time.sleep(1)

        return None   # Signal to pipeline to try Gemini fallback

    def _post(self, model: str, payload: dict):
        """Single POST to Groq API. Returns (status_code, json_dict)."""
        try:
            r = requests.post(
                GROQ_API_BASE,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type" : "application/json",
                },
                json=payload,
                timeout=60,
            )
            return r.status_code, r.json()
        except Exception as e:
            print(f"Groq request exception: {e}")
            return 500, {}

    def _extract(self, data: dict) -> Optional[str]:
        """Extract text from Groq's OpenAI-format response."""
        try:
            choices = data.get("choices", [])
            if choices:
                content = choices[0].get("message", {}).get("content", "")
                if content:
                    return content
        except Exception:
            pass
        return None

    def is_available(self) -> bool:
        """Quick connectivity check."""
        try:
            r = requests.get(
                "https://api.groq.com/openai/v1/models",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=5,
            )
            return r.status_code == 200
        except Exception:
            return False