"""
rag/embedder.py - Text Embedding via Google REST API
=====================================================
Auto-discovers the available embedding model.
Retries on 429 with exponential backoff.
"""

import os, time, requests
from typing import List

PREFERRED_EMBED_MODELS = [
    "models/gemini-embedding-001",
    "models/gemini-embedding-2-preview",
    "models/text-embedding-004",
    "models/embedding-001",
]

class Embedder:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not set in .env file.")
        self.base  = None
        self.model = None
        self._discover()
        print(f"✅ Embedder ready  model={self.model}  api={self.base}")

    def _discover(self):
        for version in ["v1beta", "v1"]:
            url  = f"https://generativelanguage.googleapis.com/{version}/models"
            resp = requests.get(url, params={"key": self.api_key}, timeout=10)
            if resp.status_code != 200:
                continue
            available = {
                m["name"]
                for m in resp.json().get("models", [])
                if "embedContent" in m.get("supportedGenerationMethods", [])
            }
            for candidate in PREFERRED_EMBED_MODELS:
                if candidate in available:
                    self.base  = version
                    self.model = candidate
                    return
        raise RuntimeError(
            "No supported embedding model found.\nRun: python check_models.py"
        )

    def _call(self, text: str, task_type: str) -> List[float]:
        model_id = self.model.split("/")[-1]
        url = (
            f"https://generativelanguage.googleapis.com/{self.base}"
            f"/models/{model_id}:embedContent"
        )
        payload = {
            "model"   : self.model,
            "content" : {"parts": [{"text": text}]},
            "taskType": task_type,
        }
        # Retry up to 4 times on 429
        for attempt in range(4):
            r = requests.post(url, params={"key": self.api_key}, json=payload, timeout=30)
            if r.status_code == 200:
                return r.json()["embedding"]["values"]
            if r.status_code == 429:
                wait = 2 ** attempt      # 1s, 2s, 4s, 8s
                print(f"⚠️  Embed 429 rate-limit (attempt {attempt+1}/4) — waiting {wait}s...")
                time.sleep(wait)
                continue
            raise RuntimeError(f"Embed API {r.status_code}: {r.text[:400]}")
        raise RuntimeError("Embedding failed after 4 retries (429 quota exceeded).")

    def embed(self, text: str) -> List[float]:
        return self._call(text, "RETRIEVAL_QUERY")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        out, total = [], len(texts)
        for i, text in enumerate(texts):
            out.append(self._call(text, "RETRIEVAL_DOCUMENT"))
            if (i + 1) % 10 == 0:
                print(f"  Embedded {i+1}/{total} chunks...")
            time.sleep(0.05)   # stay within free-tier rate limits
        return out

    def dimension(self) -> int:
        return 3072