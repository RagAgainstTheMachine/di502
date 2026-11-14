"""Question -> hybrid search -> language model -> cited answer or a fixed decline.

The result is the JSON the web page renders (see docs/deploy/app-deploy-guide.md).
Search and the language model are passed in as functions so tests can replace them.
"""
from __future__ import annotations

import re
import time
from typing import Callable

from src.app.catalog import document_facts
from src.shared.common import CONFIG, ROOT, TOP_K

PROMPT = (ROOT / "prompts" / f"{CONFIG['prompt_variant']}.txt").read_text(encoding="utf-8")
QUOTE_CHARS = CONFIG["app"]["quote_chars"]

# Fixed decline texts (US-10, US-12, C-06).
NOTICE = ("Kurumunuza özel değerlendirme veya güncel bilgi için Sanayi ve Teknoloji Bakanlığı "
          "Millî Teknoloji ve Yapay Zekâ Genel Müdürlüğüne başvurabilirsiniz.")
DECLINES = {
    "compliance": ("Kurumunuza özel bir değerlendirme yapamıyorum",
                   "Belirli bir kurumun, sistemin veya uygulamanın kurallara uyup uymadığına evet ya da "
                   "hayır diyemiyorum. Belgelerin bu konuda söylediklerini genel bir soru olarak "
                   "sorabilirsiniz."),
    "no_answer": ("Bu soruya belgelerden cevap veremiyorum",
                  "Yüklü belgelerde bu sorunun cevabını bulamadım. Asistan yalnızca koleksiyondaki "
                  "Türkiye yapay zekâ politikası belgelerinden cevap verir; tahmin yapmaz."),
}

# "Is our institution / system compliant?" questions: a first-person owner plus a judgement.
_OWNER = re.compile(r"\b(bizim|benim|kurumum\w*|kurumumuz\w*|bakanlığım\w*|şirketim\w*|"
                    r"belediyem\w*|\w+(?:imiz|ımız|umuz|ümüz)\w*)\b")
_JUDGEMENT = re.compile(r"(uygun\s+mu|uygun\s+mudur|uyumlu\s+mu|uyumlu\s+mudur|uyuyor\s+mu|"
                        r"aykırı\s+mı|ihlal|sayılır\s+mı|yasal\s+mı|hukuka\s+uygun|kurallara\s+uy)")


def lower_tr(text: str) -> str:
    return text.replace("I", "ı").replace("İ", "i").lower()


def asks_for_compliance(question: str) -> bool:
    q = lower_tr(question)
    return bool(_OWNER.search(q) and _JUDGEMENT.search(q))


def _location(hit: dict) -> str:
    parts = []
    if hit.get("action_id") is not None:
        parts.append(f"Eylem {hit['action_id']}")
    if hit.get("paragraph_id"):
        parts.append(f"Paragraf {hit['paragraph_id']}")
    if hit.get("section"):
        parts.append(hit["section"])
    start, end = hit.get("page_start"), hit.get("page_end")
    if start is not None:
        parts.append(f"PDF s. {start}" if start == end else f"PDF s. {start}–{end}")
    return " · ".join(parts)


def _context(hits: list[dict]) -> str:
    blocks = []
    for n, hit in enumerate(hits, 1):
        facts = document_facts(hit.get("document_name", ""))
        blocks.append(f"[{n}] Belge: {facts['title']} | Bölüm: {_location(hit)} | "
                      f"Hukuki statü: {facts['legal_status']}\n{hit['text']}")
    return "\n\n".join(blocks)


def renumber(raw: str, count: int) -> tuple[str, list[int]]:
    """Keep only valid citations and number them 1..m in order of first use.

    Returns the rewritten text and the original (1-based) source numbers in new order.
    """
    text = re.sub(r"\[(\d+(?:\s*,\s*\d+)+)\]",
                  lambda m: "".join(f"[{x.strip()}]" for x in m.group(1).split(",")), raw)
    order: list[int] = []
    for x in re.findall(r"\[(\d+)\]", text):
        n = int(x)
        if 1 <= n <= count and n not in order:
            order.append(n)
    new = {old: i for i, old in enumerate(order, 1)}
    text = re.sub(r"\[(\d+)\]", lambda m: f"[{new[int(m.group(1))]}]" if int(m.group(1)) in new else "", text)
    text = re.sub(r"(\[\d+\])(?:\1)+", r"\1", text)  # [1][1] -> [1]
    return text.strip(), order


def _source_card(n: int, hit: dict) -> dict:
    facts = document_facts(hit.get("document_name", ""))
    quote = " ".join(hit["text"].split())
    if len(quote) > QUOTE_CHARS:
        quote = quote[:QUOTE_CHARS].rsplit(" ", 1)[0] + " …"
    return {"n": n, "document": facts["title"], "doc_id": facts["doc_id"], "location": _location(hit),
            "legal_status": facts["legal_status"], "legal_category": facts["legal_category"],
            "date": facts["date"], "url": facts["url"], "domain": facts["domain"], "quote": quote}


def _decline(reason: str, started: float, **timing) -> dict:
    title, body = DECLINES[reason]
    return {"status": "decline", "reason": reason, "title": title, "answer": body, "notice": NOTICE,
            "sources": [], "timing": {**timing, "total_ms": round((time.perf_counter() - started) * 1000)}}


def _default_search(question: str) -> list[dict]:
    from src.retrieval.search import search  # imported here so tests do not need Qdrant
    return search(question, limit=TOP_K)


def _default_generate(prompt: str) -> str:
    from src.app.llm import generate
    return generate(prompt)


def answer(question: str, search_fn: Callable[[str], list[dict]] = _default_search,
           generate_fn: Callable[[str], str] = _default_generate) -> dict:
    started = time.perf_counter()
    question = " ".join(question.split())
    if asks_for_compliance(question):
        return _decline("compliance", started)

    t0 = time.perf_counter()
    hits = [h for h in search_fn(question) if h.get("text")]
    search_ms = round((time.perf_counter() - t0) * 1000)
    if not hits:
        return _decline("no_answer", started, search_ms=search_ms)

    t0 = time.perf_counter()
    raw = generate_fn(PROMPT.replace("{sources}", _context(hits)).replace("{question}", question))
    llm_ms = round((time.perf_counter() - t0) * 1000)
    text, order = renumber(raw, len(hits))
    if "CEVAP_YOK" in raw or not order:
        return _decline("no_answer", started, search_ms=search_ms, llm_ms=llm_ms)

    return {"status": "answer", "reason": None, "title": None, "answer": text, "notice": None,
            "sources": [_source_card(i, hits[old - 1]) for i, old in enumerate(order, 1)],
            "timing": {"search_ms": search_ms, "llm_ms": llm_ms,
                       "total_ms": round((time.perf_counter() - started) * 1000)}}
