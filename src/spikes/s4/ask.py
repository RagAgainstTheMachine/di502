"""Smoke test of the whole answer path on a laptop: question -> search -> local LLM
(Ollama) -> citation check -> answer with sources, or the fixed decline notice.

Needs Ollama running locally (https://ollama.com) with a model pulled, e.g.
  ollama pull qwen2.5:3b
Search uses BM25 with 5-letter prefixes and the exact-ID lookup (no downloads).

Usage:
  python src/spikes/s4/ask.py "Kamu kurumları yapay zekâ yol haritasını ne zamana kadar hazırlamalı?"
  python src/spikes/s4/ask.py --model qwen2.5:7b --k 5 "..."
  python src/spikes/s4/ask.py --dev-set docs/eval/dev-set-v0.csv     # all development questions, saved to CSV
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import chunking  # noqa: E402
import retrieval  # noqa: E402
from s4_retrieval_spike import id_boost  # noqa: E402

DECLINE = ("Bu soruya yüklü belgelerden cevap veremiyorum. Kurumunuza özel değerlendirme veya güncel "
           "bilgi için Millî Teknoloji ve Yapay Zekâ Genel Müdürlüğüne başvurabilirsiniz.")

PROMPT = """Sen Türkiye'nin yapay zekâ politikası belgeleri hakkında soruları cevaplayan bir asistansın.
Kurallar:
1. Yalnızca aşağıdaki KAYNAKLAR'daki bilgiyi kullan. Kendi bilgini ekleme.
2. Türkçe ve kısa cevap ver (en fazla 5 cümle).
3. Her cümlenin sonuna dayandığı kaynağın numarasını köşeli parantezle yaz, örneğin [2].
4. Kaynaklar soruyu cevaplamıyorsa yalnızca CEVAP_YOK yaz.

KAYNAKLAR:
{sources}

SORU: {question}
CEVAP:"""


def ollama(model: str, prompt: str, url: str) -> str:
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0}}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.loads(r.read())["response"].strip()


def answer(question: str, chunks, bm25, k: int, model: str, url: str) -> dict:
    t0 = time.perf_counter()
    scores = id_boost(question, chunks, bm25.scores(question))
    top = [chunks[i] for i in np.argsort(-scores)[:k]]
    t_search = time.perf_counter() - t0
    sources = "\n\n".join(f"[{n}] {c.text}" for n, c in enumerate(top, 1))
    raw = ollama(model, PROMPT.format(sources=sources, question=question), url)
    t_total = time.perf_counter() - t0

    cited = sorted({int(x) for x in re.findall(r"\[(\d+)\]", raw)})
    valid = [n for n in cited if 1 <= n <= len(top)]
    invalid = [n for n in cited if n not in valid]
    declined = "CEVAP_YOK" in raw or not valid
    return {
        "question": question,
        "answer": DECLINE if declined else re.sub(r"\s*CEVAP_YOK\s*", " ", raw).strip(),
        "declined": declined,
        "raw": raw,
        "invalid_citations": invalid,
        "sources": [] if declined else [top[n - 1] for n in valid],
        "retrieved": [c.chunk_id for c in top],
        "search_s": t_search,
        "total_s": t_total,
    }


def show(r: dict):
    print(f"\nSORU: {r['question']}\n\n{r['answer']}\n")
    for n, c in enumerate(r["sources"], 1):
        pages = f"PDF s. {c.pdf_pages[0]}" if c.pdf_pages else ""
        print(f"  Kaynak: {c.title} | {c.section[:90]} | {pages} | Hukuki statü: {c.legal_status}")
    if r["invalid_citations"]:
        print(f"  UYARI: getirilmeyen kaynak numarası atfedildi: {r['invalid_citations']}")
    print(f"  (arama {r['search_s'] * 1000:.0f} ms, toplam {r['total_s']:.1f} s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("question", nargs="?")
    ap.add_argument("--text-dir", default="data/text", type=Path)
    ap.add_argument("--model", default="qwen2.5:3b")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--url", default="http://localhost:11434/api/generate")
    ap.add_argument("--dev-set", type=Path)
    ap.add_argument("--out", default="docs/spikes/results/ask-dev-set.csv", type=Path)
    a = ap.parse_args()

    chunks = []
    for d in chunking.load_corpus(a.text_dir):
        chunks += chunking.chunk_structure(d)
    bm25 = retrieval.BM25([c.text for c in chunks], stem=5)

    if a.dev_set:
        rows = [r for r in csv.DictReader(a.dev_set.open(encoding="utf-8-sig"))]
        out = []
        for q in rows:
            r = answer(q["question"], chunks, bm25, a.k, a.model, a.url)
            show(r)
            out.append({"id": q["id"], "question": q["question"], "answer": r["answer"],
                        "declined": r["declined"], "invalid_citations": r["invalid_citations"],
                        "sources": "; ".join(f"{c.chunk_id} {c.section[:60]}" for c in r["sources"]),
                        "total_s": round(r["total_s"], 1), "model": a.model,
                        "correct (judge)": "", "citation supports (judge)": ""})
        a.out.parent.mkdir(parents=True, exist_ok=True)
        with a.out.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(out[0]))
            w.writeheader()
            w.writerows(out)
        times = sorted(o["total_s"] for o in out)
        print(f"\nSaved {len(out)} answers to {a.out}; median {times[len(times) // 2]} s; "
              f"declined {sum(o['declined'] for o in out)}")
    elif a.question:
        show(answer(a.question, chunks, bm25, a.k, a.model, a.url))
    else:
        ap.error("give a question or --dev-set")


if __name__ == "__main__":
    main()
