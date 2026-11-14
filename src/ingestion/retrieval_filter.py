"""Exclude table-of-contents and proven heading-only chunks from retrieval.

Short facts and glossary definitions are retained. Exclusions are archived.
"""
import re
import unicodedata

POLICY_VERSION = 1
HEADING_LABELS = {"title", "section_header"}


def normalized(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text).casefold().replace("\u0307", "")).strip()


def filter_chunks(chunks, parents, blocks):
    """Exclude contents sections and proven heading-only section chunks.

    No word-count threshold is used. Unknown or partial provenance fails open:
    retain the content rather than guess that a short answer is disposable.
    """
    sources = {b["source_ref"]: b for b in blocks}
    kept, excluded = [], []
    for chunk in chunks:
        reason = None
        if chunk["kind"] == "section":
            path = [normalized(p) for p in chunk["section"].split(" / ")]
            if any(p in {"içindekiler", "table of contents", "contents"} for p in path):
                reason = "table_of_contents"
            else:
                refs = chunk.get("source_refs", [])
                origin = [sources[r] for r in refs if r in sources]
                if (refs and len(origin) == len(refs)
                        and all(b["label"] in HEADING_LABELS for b in origin)
                        and normalized(chunk["text"]) == normalized(" ".join(b["text"] for b in origin))):
                    reason = "heading_only"
        if reason:
            excluded.append({"reason": reason, "chunk": chunk})
        else:
            kept.append(chunk)
    if not kept:
        raise ValueError("Review sonrasında indekslenecek bilgi içeren chunk kalmadı.")
    by_parent = {}
    for c in kept:
        by_parent.setdefault(c["parent_id"], []).append(c)
    removed_ids = {e["chunk"]["parent_id"] for e in excluded}
    retained_parents, excluded_parents = [], []
    for parent in parents:
        children = by_parent.get(parent["parent_id"], [])
        if not children:
            excluded_parents.append(parent)
            continue
        if parent["parent_id"] in removed_ids:
            children = sorted(children, key=lambda c: c["chunk_index"])
            pages = sorted({p for c in children for p in c["pages"]})
            parent = {**parent, "text":"\n\n".join(c["text"] for c in children),
                      "chunk_count":len(children), "page_start":min(pages) if pages else None,
                      "page_end":max(pages) if pages else None}
        retained_parents.append(parent)
    return kept, retained_parents, excluded, excluded_parents
