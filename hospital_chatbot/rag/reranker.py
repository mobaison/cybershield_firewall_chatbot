"""
rag/reranker.py — Cross-Encoder Re-Ranker
==========================================
After FAISS + BM25 retrieve top-10 candidate chunks, the re-ranker
scores each (question, chunk) pair together and picks the best 4.

WHY RE-RANKING MATTERS:
  Vector search: embeds question and chunk SEPARATELY, compares vectors
    → fast but misses nuanced relevance
  Cross-encoder:  reads question + chunk TOGETHER in one pass
    → slow but much more accurate relevance scoring

IMPLEMENTATION:
  We use Groq (llama-3.1-8b-instant) as our cross-encoder.
  For each candidate chunk, ask: "Does this text answer the question? Score 0-10"
  Pick top-4 by score.

  Falls back gracefully: if Groq unavailable, returns FAISS/BM25 order as-is.

COST: ~100 tokens × 10 chunks = ~1000 tokens per re-rank call
  On Groq free tier: negligible (131,072 TPM limit)
"""

import os, requests, re
from typing import List, Dict, Optional

GROQ_API_BASE = "https://api.groq.com/openai/v1/chat/completions"
RERANK_MODEL  = "llama-3.1-8b-instant"   # Fast + cheap for scoring task


class Reranker:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.enabled = bool(api_key)
        if self.enabled:
            print(f"  ✅ Re-ranker enabled (model: {RERANK_MODEL})")
        else:
            print("  ⚠️  Re-ranker disabled (no GROQ_API_KEY)")

    def rerank(self, query: str, candidates: List[Dict],
               top_k: int = 4) -> List[Dict]:
        """
        Re-score candidates and return top_k most relevant.
        Falls back to original order if Groq unavailable.
        """
        if not self.enabled or len(candidates) <= top_k:
            return candidates[:top_k]

        # Build batch scoring prompt — score all candidates in one API call
        chunk_list = "\n\n".join([
            f"CHUNK {i+1}:\n{c['text'][:400]}"
            for i, c in enumerate(candidates)
        ])

        prompt = f"""Question: {query}

Below are {len(candidates)} text chunks. For each chunk, give a relevance score
from 0 to 10 (10 = perfectly answers the question, 0 = completely irrelevant).

{chunk_list}

Respond ONLY with scores in this exact format (one per line):
CHUNK 1: <score>
CHUNK 2: <score>
...
CHUNK {len(candidates)}: <score>"""

        try:
            r = requests.post(
                GROQ_API_BASE,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type" : "application/json",
                },
                json={
                    "model"      : RERANK_MODEL,
                    "messages"   : [{"role": "user", "content": prompt}],
                    "temperature": 0.0,
                    "max_tokens" : 100,
                    "stream"     : False,
                },
                timeout=8,
            )

            if r.status_code == 200:
                response_text = (
                    r.json()
                    .get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "")
                )
                scores = self._parse_scores(response_text, len(candidates))
                if scores:
                    # Attach scores and sort
                    scored = []
                    for i, (chunk, score) in enumerate(zip(candidates, scores)):
                        c = dict(chunk)
                        c["rerank_score"] = score
                        scored.append(c)
                    scored.sort(key=lambda x: x["rerank_score"], reverse=True)
                    return scored[:top_k]

        except Exception as e:
            pass  # Fail gracefully — return original order

        return candidates[:top_k]

    def _parse_scores(self, text: str, n: int) -> Optional[List[float]]:
        """Parse 'CHUNK N: score' lines from response."""
        scores = []
        for i in range(1, n + 1):
            pattern = rf'CHUNK\s+{i}\s*:\s*([0-9]+(?:\.[0-9]+)?)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                scores.append(float(match.group(1)))
            else:
                scores.append(0.0)
        return scores if len(scores) == n else None