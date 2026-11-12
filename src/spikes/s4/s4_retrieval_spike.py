"""Spike S4: compare passage splitting and search methods on the development set.

For each configuration (strategy x method) every development question is
searched, and the result counts as a hit when a retrieved passage covers the
line of the gold anchor in the source .md file.

Metrics: hit@1, recall@5 (gold in top 5), MRR@10, mean query time.

Methods:
  bm25            BM25 on whole words
  bm25s5          BM25 on 5-letter word prefixes (simple Turkish stemming)
  dense:<model>   embedding search (sentence-transformers model name)
  hybrid:<model>  reciprocal rank fusion of bm25s5 and dense:<model>
  <method>+id     the same, plus an exact lookup when the question names
                  "Eylem N", "Tedbir N.N", "Paragraf N" or "Madde N"

Usage (BM25 only, no downloads):
  python src/spikes/s4/s4_retrieval_spike.py
With embeddings:
  python src/spikes/s4/s4_retrieval_spike.py --methods bm25,bm25s5,dense:intfloat/multilingual-e5-base,hybrid:intfloat/multilingual-e5-base
"""
from __future__ import annotations

import argparse
import csv
import re
import datetime as dt
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chunking  # noqa: E402
import retrieval  # noqa: E402


def load_dev(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig") as f:
        return [r for r in csv.DictReader(f) if r["id"].strip()]


def gold_lines(docs: dict, row: dict) -> set[int]:
    """Lines in the gold document that contain any of the anchors (separated by ' || ').

    When an anchor is on a heading line, the whole section under that heading
    (up to the next heading) is gold, so every passage of that section counts.
    """
    d = docs[row["gold_doc"]]
    out = set()
    for anchor in row["gold_anchor"].split(" || "):
        a = retrieval.normalize(anchor.strip())
        for i, l in enumerate(d.lines):
            if a not in retrieval.normalize(l):
                continue
            out.add(i + 1)
            if chunking.HEAD_RE.match(l):
                j = i + 1
                while j < len(d.lines) and not chunking.HEAD_RE.match(d.lines[j]):
                    out.add(j + 1)
                    j += 1
    return out


ID_RE = re.compile(r"\b(eylem|tedbir|paragraf|madde)\s+(\d+(?:\.\d+)?)", re.IGNORECASE)


def id_boost(query: str, chunks, scores: np.ndarray) -> np.ndarray:
    """Exact lookup: if the question names 'Eylem 16', 'Tedbir 688.2' etc., move the
    passages whose section heading carries that label to the top (US-4)."""
    m = ID_RE.search(retrieval.normalize(query))
    if not m:
        return scores
    label = re.compile(rf"\b{m.group(1)}\s+{re.escape(m.group(2))}(?![\d.]*\d)", re.IGNORECASE)
    bonus = np.array([1e6 if label.search(retrieval.normalize(c.section)) else 0.0 for c in chunks])
    return scores + bonus


def run(chunks, docs, dev, method: str, cache_dir: Path, tag: str, bm25_cache: dict):
    texts = [c.text for c in chunks]
    use_id = method.endswith("+id")
    method = method.removesuffix("+id")
    t0 = time.perf_counter()
    if method in ("bm25", "bm25s5"):
        key = (tag, method)
        if key not in bm25_cache:
            bm25_cache[key] = retrieval.BM25(texts, stem=5 if method == "bm25s5" else 0)
        scorers = [bm25_cache[key]]
    else:
        kind, model = method.split(":", 1)
        dense = retrieval.Dense(model, texts, cache_dir, tag)
        if kind == "dense":
            scorers = [dense]
        else:
            key = (tag, "bm25s5")
            if key not in bm25_cache:
                bm25_cache[key] = retrieval.BM25(texts, stem=5)
            scorers = [bm25_cache[key], dense]
    index_s = time.perf_counter() - t0

    rows, qtimes = [], []
    for q in dev:
        gl = gold_lines(docs, q)
        t1 = time.perf_counter()
        score_lists = [s.scores(q["question"]) for s in scorers]
        s = score_lists[0] if len(score_lists) == 1 else retrieval.rrf(score_lists)
        if use_id:
            s = id_boost(q["question"], chunks, s)
        qtimes.append(time.perf_counter() - t1)
        top = np.argsort(-s)[:10]
        rank = next((r + 1 for r, i in enumerate(top)
                     if chunks[i].doc_id == q["gold_doc"]
                     and any(chunks[i].line_start <= l <= chunks[i].line_end for l in gl)), None)
        rows.append({"id": q["id"], "type": q["type"], "rank": rank or "",
                     "top1": f"{chunks[top[0]].chunk_id} {chunks[top[0]].section[:60]}",
                     "question": q["question"]})
    ranks = [r["rank"] or 99 for r in rows]
    summary = {
        "hit@1": sum(r == 1 for r in ranks) / len(ranks),
        "recall@5": sum(r <= 5 for r in ranks) / len(ranks),
        "mrr@10": sum(1 / r for r in ranks if r <= 10) / len(ranks),
        "query_ms": 1000 * float(np.mean(qtimes)),
        "index_s": index_s,
    }
    return summary, rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-dir", default="data/text", type=Path)
    ap.add_argument("--dev-set", default="docs/eval/dev-set-v0.csv", type=Path)
    ap.add_argument("--strategies", default="structure,fixed")
    ap.add_argument("--methods", default="bm25,bm25s5")
    ap.add_argument("--max-chars", type=int, default=1000)
    ap.add_argument("--overlap", type=int, default=200)
    ap.add_argument("--out-dir", default="docs/spikes/results", type=Path)
    ap.add_argument("--cache-dir", default="data/emb_cache", type=Path)
    a = ap.parse_args()

    corpus = chunking.load_corpus(a.text_dir)
    docs = {d.doc_id: d for d in corpus}
    dev = load_dev(a.dev_set)
    missing = [q["id"] for q in dev if not gold_lines(docs, q)]
    if missing:
        sys.exit(f"Gold anchor not found in the corpus for: {', '.join(missing)}")

    a.out_dir.mkdir(parents=True, exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M")
    table, details, bm25_cache = [], [], {}
    for strategy in a.strategies.split(","):
        chunks = []
        for d in corpus:
            chunks += (chunking.chunk_structure(d, a.max_chars) if strategy == "structure"
                       else chunking.chunk_fixed(d, a.max_chars, a.overlap))
        tag = f"{strategy}{a.max_chars}"
        for method in a.methods.split(","):
            print(f"== {strategy} / {method} ({len(chunks)} passages)")
            summary, rows = run(chunks, docs, dev, method, a.cache_dir, tag, bm25_cache)
            table.append({"strategy": strategy, "method": method, "passages": len(chunks), **summary})
            for r in rows:
                details.append({"strategy": strategy, "method": method, **r})

    lines = [f"Development set: {a.dev_set} ({len(dev)} questions); max chars {a.max_chars}, overlap {a.overlap}; run {stamp}", "",
             "| Strategy | Method | Passages | Hit@1 | Recall@5 | MRR@10 | Query ms | Index s |",
             "|---|---|---|---|---|---|---|---|"]
    for t in table:
        lines.append(f"| {t['strategy']} | {t['method']} | {t['passages']} | {t['hit@1']:.2f} | {t['recall@5']:.2f} | "
                     f"{t['mrr@10']:.2f} | {t['query_ms']:.0f} | {t['index_s']:.1f} |")
    md = "\n".join(lines)
    print("\n" + md)
    (a.out_dir / f"s4-summary-{stamp}.md").write_text(md + "\n", encoding="utf-8")
    with (a.out_dir / f"s4-per-question-{stamp}.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(details[0]))
        w.writeheader()
        w.writerows(details)
    print(f"\nSaved to {a.out_dir}")


if __name__ == "__main__":
    main()
