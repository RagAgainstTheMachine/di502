"""Search over passages: BM25 (keyword), dense (embedding) and hybrid (RRF).

BM25 needs only the standard library and numpy. Dense search needs
sentence-transformers and downloads the model from Hugging Face on first use.
"""
from __future__ import annotations

import math
import re
import time
import unicodedata
from collections import Counter
from pathlib import Path

import numpy as np

TOKEN_RE = re.compile(r"\w+", re.UNICODE)
# Short list of Turkish function words; content words are never removed.
STOPWORDS = set("""
ve veya ile ya da de da ki mi mı mu mü bu şu o bir için gibi olan olarak ise ancak ama hem her
daha en çok az kadar sonra önce göre ait dair üzere yönelik ilişkin nasıl ne neler nedir hangi
hangisi kim kimdir midir mıdır var yok değil ayrıca bunun buna bunlar şekilde tarafından
""".split())


def normalize(text: str) -> str:
    # NFKC turns ligatures (U+FB01, U+FB02) into plain letters; Turkish I/İ are lowered by hand.
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("I", "ı").replace("İ", "i").lower()
    return text.replace("â", "a").replace("î", "i").replace("û", "u")


def tokenize(text: str, stem: int = 0) -> list[str]:
    toks = [t for t in TOKEN_RE.findall(normalize(text)) if t not in STOPWORDS]
    if stem:
        # Fixed-prefix stemming (Can et al.): keep the first `stem` characters of each word.
        toks = [t[:stem] for t in toks]
    return toks


class BM25:
    def __init__(self, texts: list[str], stem: int = 0, k1: float = 1.5, b: float = 0.75):
        self.stem, self.k1, self.b = stem, k1, b
        self.docs = [Counter(tokenize(t, stem)) for t in texts]
        self.len = np.array([sum(d.values()) for d in self.docs], dtype=float)
        self.avg = self.len.mean()
        df = Counter(w for d in self.docs for w in d)
        n = len(texts)
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}

    def scores(self, query: str) -> np.ndarray:
        q = tokenize(query, self.stem)
        s = np.zeros(len(self.docs))
        norm = self.k1 * (1 - self.b + self.b * self.len / self.avg)
        for i, d in enumerate(self.docs):
            for w in q:
                f = d.get(w)
                if f:
                    s[i] += self.idf[w] * f * (self.k1 + 1) / (f + norm[i])
        return s


# Prefixes each model was trained with (query, passage).
PREFIXES = {
    "intfloat/multilingual-e5-small": ("query: ", "passage: "),
    "intfloat/multilingual-e5-base": ("query: ", "passage: "),
    "intfloat/multilingual-e5-large": ("query: ", "passage: "),
    "google/embeddinggemma-300m": ("task: search result | query: ", "title: none | text: "),
}


class Dense:
    def __init__(self, model_name: str, texts: list[str], cache_dir: Path | None = None, tag: str = ""):
        from sentence_transformers import SentenceTransformer  # imported here so BM25 runs without it

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.qp, self.pp = PREFIXES.get(model_name, ("", ""))
        cache = None
        if cache_dir:
            cache_dir.mkdir(parents=True, exist_ok=True)
            cache = cache_dir / f"{model_name.replace('/', '__')}__{tag}__{len(texts)}.npy"
        t0 = time.perf_counter()
        if cache and cache.exists():
            self.emb = np.load(cache)
        else:
            self.emb = self.model.encode([self.pp + t for t in texts], batch_size=16,
                                         normalize_embeddings=True, show_progress_bar=True)
            if cache:
                np.save(cache, self.emb)
        self.index_seconds = time.perf_counter() - t0

    def scores(self, query: str) -> np.ndarray:
        q = self.model.encode([self.qp + query], normalize_embeddings=True)[0]
        return self.emb @ q


def rrf(score_lists: list[np.ndarray], k: int = 60, depth: int = 50) -> np.ndarray:
    """Reciprocal rank fusion of several score vectors over the same passages."""
    fused = np.zeros(len(score_lists[0]))
    for s in score_lists:
        order = np.argsort(-s)[:depth]
        for rank, i in enumerate(order):
            fused[i] += 1.0 / (k + rank + 1)
    return fused
