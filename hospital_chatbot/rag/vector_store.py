"""
rag/vector_store.py — Hybrid Vector Store (FAISS + BM25)
=========================================================
HYBRID SEARCH STRATEGY:
  1. FAISS semantic search  → top-10 by vector similarity
  2. BM25 keyword search    → top-10 by keyword relevance
  3. Reciprocal Rank Fusion → merge both lists into unified ranking
  4. Re-ranker (Groq)       → re-score top-10, return best 4

RECIPROCAL RANK FUSION (RRF):
  For each document in both result lists:
    RRF score = 1/(rank_in_faiss + 60) + 1/(rank_in_bm25 + 60)
  Higher score = appeared highly in BOTH lists = most relevant

  The constant 60 is standard RRF tuning parameter.
"""

import os, pickle
import numpy as np
import faiss
from typing import List, Dict, Optional
from rag.bm25_index import BM25Index
from rag.reranker   import Reranker

INDEX_PATH    = "data/faiss_index.bin"
METADATA_PATH = "data/faiss_metadata.pkl"


class VectorStore:
    def __init__(self, groq_api_key: str = ""):
        self.index     = None
        self.metadata  = []
        self.dimension = None
        self.bm25      = BM25Index()
        self.reranker  = Reranker(api_key=groq_api_key)

    def build_index(self, documents: List[Dict], embedder):
        """Build FAISS + BM25 index from documents."""
        if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
            print("💾 Loading cached FAISS index...")
            self._load_index()
            # Always rebuild BM25 (in-memory, fast, no API calls)
            print("  Building BM25 index...")
            self.bm25.build(self.metadata)
            return

        print("🔨 Building new FAISS + BM25 index...")
        texts      = [doc["text"] for doc in documents]
        embeddings = embedder.embed_documents(texts)
        emb_np     = np.array(embeddings, dtype=np.float32)

        self.dimension = emb_np.shape[1]
        print(f"  Detected embedding dimension: {self.dimension}")

        faiss.normalize_L2(emb_np)
        self.index = faiss.IndexFlatIP(self.dimension)
        self.index.add(emb_np)
        self.metadata = documents

        # Build BM25 index
        self.bm25.build(documents)

        os.makedirs("data", exist_ok=True)
        self._save_index()
        print(f"✅ Hybrid index built: {self.index.ntotal} vectors "
              f"(dim={self.dimension})")

    def search(self, query: str, embedder, top_k: int = 4) -> List[Dict]:
        """
        Hybrid search: FAISS + BM25 → RRF merge → re-rank → top_k.
        """
        if self.index is None or self.index.ntotal == 0:
            return []

        retrieve_k = min(10, self.index.ntotal)  # retrieve more, then re-rank

        # ── FAISS semantic search ─────────────────────────────────
        q_np = np.array([embedder.embed(query)], dtype=np.float32)
        faiss.normalize_L2(q_np)
        faiss_scores, faiss_indices = self.index.search(q_np, retrieve_k)

        faiss_results: Dict[int, float] = {}
        for rank, (score, idx) in enumerate(
                zip(faiss_scores[0], faiss_indices[0])):
            if idx != -1:
                faiss_results[idx] = (rank, float(score))

        # ── BM25 keyword search ───────────────────────────────────
        bm25_raw = self.bm25.search(query, top_k=retrieve_k)
        bm25_results: Dict[int, float] = {
            idx: (rank, score)
            for rank, (idx, score) in enumerate(bm25_raw)
        }

        # ── Reciprocal Rank Fusion ────────────────────────────────
        all_indices = set(faiss_results.keys()) | set(bm25_results.keys())
        rrf_scores: Dict[int, float] = {}

        for idx in all_indices:
            score = 0.0
            if idx in faiss_results:
                rank = faiss_results[idx][0]
                score += 1.0 / (rank + 60)
            if idx in bm25_results:
                rank = bm25_results[idx][0]
                score += 1.0 / (rank + 60)
            rrf_scores[idx] = score

        # Sort by RRF score, take top retrieve_k
        sorted_indices = sorted(
            rrf_scores.keys(),
            key=lambda i: rrf_scores[i],
            reverse=True
        )[:retrieve_k]

        candidates = []
        for idx in sorted_indices:
            chunk = dict(self.metadata[idx])
            # Combine scores for transparency
            faiss_s = faiss_results.get(idx, (99, 0.0))[1]
            bm25_s  = bm25_results.get(idx,  (99, 0.0))[1]
            chunk["faiss_score"] = round(faiss_s, 4)
            chunk["bm25_score"]  = round(bm25_s, 4)
            chunk["rrf_score"]   = round(rrf_scores[idx], 6)
            candidates.append(chunk)

        # ── Re-rank with Groq ─────────────────────────────────────
        final = self.reranker.rerank(query, candidates, top_k=top_k)
        return final

    def _save_index(self):
        faiss.write_index(self.index, INDEX_PATH)
        with open(METADATA_PATH, "wb") as f:
            pickle.dump({
                "metadata" : self.metadata,
                "dimension": self.dimension
            }, f)

    def _load_index(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(METADATA_PATH, "rb") as f:
            saved = pickle.load(f)
            if isinstance(saved, list):
                self.metadata  = saved
                self.dimension = self.index.d
            else:
                self.metadata  = saved["metadata"]
                self.dimension = saved["dimension"]
        print(f"✅ Loaded FAISS: {self.index.ntotal} vectors "
              f"(dim={self.dimension})")