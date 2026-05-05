"""
rag/bm25_index.py — BM25 Keyword Search Index
===============================================
BM25 is a classic information retrieval algorithm (TF-IDF variant).
While FAISS finds semantically similar chunks, BM25 finds chunks
with exact keyword matches. Combining both = Hybrid Search.

WHY HYBRID:
  FAISS alone fails when:  "What is Dr. Sharma's fee?" 
    → semantic similarity finds "fees" chunks but may miss Dr. Sharma
  BM25 alone fails when:   "heart problem costs"
    → misses chunks about "cardiology fees" (different words, same meaning)
  Hybrid catches both cases.

NO EXTRA DEPENDENCIES: Pure Python implementation of BM25.
"""

import math, re
from collections import defaultdict
from typing import List, Dict, Tuple


def _tokenize(text: str) -> List[str]:
    """Lowercase, remove punctuation, split into words."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return [w for w in text.split() if len(w) > 1]


class BM25Index:
    """
    Pure-Python BM25 index. No external dependencies.
    Parameters k1=1.5, b=0.75 are standard BM25 defaults.
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1   = k1
        self.b    = b
        self.docs : List[Dict]         = []
        self.tf   : List[Dict[str,int]] = []   # term freq per doc
        self.df   : Dict[str,int]       = defaultdict(int)  # doc freq
        self.idf  : Dict[str,float]     = {}
        self.avgdl: float               = 0.0
        self.N    : int                 = 0

    def build(self, documents: List[Dict]):
        """Index all documents."""
        self.docs = documents
        self.N    = len(documents)
        total_len = 0

        for doc in documents:
            tokens    = _tokenize(doc["text"])
            total_len += len(tokens)
            freq: Dict[str,int] = defaultdict(int)
            for t in tokens:
                freq[t] += 1
            self.tf.append(dict(freq))
            for term in set(tokens):
                self.df[term] += 1

        self.avgdl = total_len / max(self.N, 1)

        # Precompute IDF for all terms
        for term, df in self.df.items():
            self.idf[term] = math.log(
                (self.N - df + 0.5) / (df + 0.5) + 1
            )
        print(f"  BM25 index built: {self.N} docs, "
              f"{len(self.idf)} unique terms")

    def search(self, query: str, top_k: int = 10) -> List[Tuple[int, float]]:
        """
        Returns list of (doc_index, bm25_score), sorted descending.
        """
        if not self.docs:
            return []

        query_terms = _tokenize(query)
        scores = []

        for i, tf_doc in enumerate(self.tf):
            dl    = sum(tf_doc.values())
            score = 0.0
            for term in query_terms:
                if term not in tf_doc:
                    continue
                idf = self.idf.get(term, 0.0)
                tf  = tf_doc[term]
                # BM25 formula
                numerator   = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (
                    1 - self.b + self.b * dl / max(self.avgdl, 1)
                )
                score += idf * numerator / denominator
            if score > 0:
                scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]