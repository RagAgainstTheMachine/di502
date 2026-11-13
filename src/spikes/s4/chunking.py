"""Split the extracted corpus (data/text/*.md) into passages.

Two strategies:
  structure  one passage per heading (action, Tedbir, paragraph, glossary term,
             section); sections longer than --max-chars are split at paragraph
             or sentence boundaries. Every passage starts with the document
             title and its section path.
  fixed      fixed windows of --max-chars characters with --overlap characters
             of overlap, cut at whitespace, no title or section prefix.

Each passage keeps its document, section, legal status, PDF pages and the line
range in the source .md file (used to check retrieval against gold sources).

Usage:
  python src/spikes/s4/chunking.py --text-dir data/text --strategy structure --out data/chunks/structure.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

# Legal status per document. Source of truth is the document inventory;
# this copy must be kept equal to it.
LEGAL_STATUS = {
    "Doc01": "policy/plan",
    "Doc02": "policy/plan",
    "Doc03": "policy/plan",
    "Doc04": "binding law",
    "Doc05": "report",
    "Doc06": "guidance",
    "Doc07": "institutional policy",
    "Doc08": "guidance",
}

PAGE_RE = re.compile(r"<!--\s*page:\s*pdf\s*(\d+)\s*\|\s*printed\s*([^\s>]+)\s*-->")
CONTEXT_RE = re.compile(r"<!--\s*section heading:\s*(.*?)-->")
COMMENT_RE = re.compile(r"<!--.*?-->")
HEAD_RE = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
SENT_RE = re.compile(r"(?<=[.!?;:])\s+")


@dataclass
class Para:
    line: int          # 1-based line number in the .md file
    page: int | None   # PDF page
    text: str


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    title: str
    section: str
    legal_status: str
    pdf_pages: list[int]
    line_start: int
    line_end: int
    text: str                      # what is embedded / searched
    n_chars: int = field(default=0)


@dataclass
class Doc:
    doc_id: str
    title: str
    status: str
    lines: list[str]               # file lines, index 0 = line 1
    body_start: int                # first line after the front matter (1-based)


def load_doc(path: Path) -> Doc:
    lines = path.read_text(encoding="utf-8").splitlines()
    meta, start = {}, 1
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                start = i + 2
                break
            k, _, v = lines[i].partition(":")
            meta[k.strip()] = v.strip().strip('"')
    return Doc(meta.get("doc_id", path.stem), meta.get("title", path.stem),
               meta.get("status", "ok"), lines, start)


def load_corpus(text_dir: Path) -> list[Doc]:
    docs = []
    for p in sorted(text_dir.glob("doc*.md")):
        d = load_doc(p)
        if "BLOCKED" in d.status.upper():
            print(f"skip {p.name}: {d.status}")
            continue
        docs.append(d)
    return docs


def _sections(doc: Doc):
    """Yield (path, context, paragraphs, heading line) for every heading that has body text."""
    stack: list[tuple[int, str]] = []
    context, page = "", None
    paras: list[Para] = []

    def path():
        # level-1 heading is the document title, already in the prefix
        return " > ".join(t for lvl, t in stack if lvl > 1)

    cur_path, head_line = "", doc.body_start
    for ln in range(doc.body_start, len(doc.lines) + 1):
        raw = doc.lines[ln - 1]
        m = PAGE_RE.search(raw)
        if m:
            page = int(m.group(1))
        c = CONTEXT_RE.search(raw)
        if c:
            context = " | ".join(s.strip() for s in c.group(1).split("|"))
        h = HEAD_RE.match(raw)
        if h:
            if paras:
                yield cur_path, context, paras, head_line
            paras, context, head_line = [], "", ln
            lvl = len(h.group(1))
            while stack and stack[-1][0] >= lvl:
                stack.pop()
            stack.append((lvl, h.group(2)))
            cur_path = path()
            continue
        text = COMMENT_RE.sub("", raw).strip()
        if text:
            paras.append(Para(ln, page, text))
    if paras:
        yield cur_path, context, paras, head_line


def _split_long(p: Para, max_chars: int) -> list[Para]:
    if len(p.text) <= max_chars:
        return [p]
    pieces = []
    for s in SENT_RE.split(p.text):
        while len(s) > max_chars:                       # one very long sentence: cut at a space
            cut = s.rfind(" ", 0, max_chars)
            cut = cut if cut > 0 else max_chars
            pieces.append(s[:cut].strip())
            s = s[cut:].strip()
        if s:
            pieces.append(s)
    out, buf = [], ""
    for s in pieces:                                    # pack sentences up to max_chars
        if buf and len(buf) + 1 + len(s) > max_chars:
            out.append(Para(p.line, p.page, buf))
            buf = s
        else:
            buf = (buf + " " + s).strip()
    if buf:
        out.append(Para(p.line, p.page, buf))
    return out


def chunk_structure(doc: Doc, max_chars: int = 1000) -> list[Chunk]:
    chunks: list[Chunk] = []
    for path, context, paras, head_line in _sections(doc):
        section = path + (f" [{context}]" if context else "")
        pieces = [q for p in paras for q in _split_long(p, max_chars)]
        groups, cur, size = [], [], 0
        for q in pieces:
            if cur and size + len(q.text) + 1 > max_chars:
                groups.append(cur)
                cur, size = [], 0
            cur.append(q)
            size += len(q.text) + 1
        if cur:
            groups.append(cur)
        for gi, g in enumerate(groups):
            body = "\n".join(q.text for q in g)
            text = f"{doc.title}\n{section}\n\n{body}"
            pages = sorted({q.page for q in g if q.page is not None})
            chunks.append(Chunk(f"{doc.doc_id}-s{len(chunks) + 1:04d}", doc.doc_id, doc.title, section,
                                LEGAL_STATUS.get(doc.doc_id, "unknown"), pages,
                                head_line if gi == 0 else g[0].line, g[-1].line, text, len(text)))
    return chunks


def chunk_fixed(doc: Doc, max_chars: int = 1000, overlap: int = 200) -> list[Chunk]:
    # Join all text lines (headings kept as plain text), remembering where each line starts.
    parts, starts, page_of_line, page = [], [], {}, None
    pos = 0
    for ln in range(doc.body_start, len(doc.lines) + 1):
        raw = doc.lines[ln - 1]
        m = PAGE_RE.search(raw)
        if m:
            page = int(m.group(1))
        text = COMMENT_RE.sub("", raw).strip().lstrip("#").strip()
        if not text:
            continue
        starts.append((pos, ln))
        page_of_line[ln] = page
        parts.append(text)
        pos += len(text) + 1
    full = "\n".join(parts)

    def line_at(offset: int) -> int:
        lo = 0
        for i, (s, _) in enumerate(starts):
            if s <= offset:
                lo = i
            else:
                break
        return starts[lo][1]

    chunks, i = [], 0
    while i < len(full):
        end = min(len(full), i + max_chars)
        if end < len(full):
            sp = full.rfind(" ", i + max_chars // 2, end)
            end = sp if sp > 0 else end
        body = full[i:end].strip()
        a, b = line_at(i), line_at(max(i, end - 1))
        pages = sorted({page_of_line[l] for l in page_of_line if a <= l <= b and page_of_line[l] is not None})
        chunks.append(Chunk(f"{doc.doc_id}-f{len(chunks) + 1:04d}", doc.doc_id, doc.title, "",
                            LEGAL_STATUS.get(doc.doc_id, "unknown"), pages, a, b, body, len(body)))
        if end >= len(full):
            break
        nxt = end - overlap
        sp = full.find(" ", nxt)
        i = sp + 1 if 0 <= sp < end else nxt
    return chunks


def build(text_dir: Path, strategy: str, max_chars: int, overlap: int) -> list[Chunk]:
    out = []
    for d in load_corpus(text_dir):
        out += chunk_structure(d, max_chars) if strategy == "structure" else chunk_fixed(d, max_chars, overlap)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-dir", default="data/text", type=Path)
    ap.add_argument("--strategy", choices=["structure", "fixed"], default="structure")
    ap.add_argument("--max-chars", type=int, default=1000)
    ap.add_argument("--overlap", type=int, default=200)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    chunks = build(a.text_dir, a.strategy, a.max_chars, a.overlap)
    out = a.out or Path(f"data/chunks/{a.strategy}.jsonl")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")
    by_doc = {}
    for c in chunks:
        by_doc.setdefault(c.doc_id, []).append(c.n_chars)
    print(f"{len(chunks)} passages -> {out}")
    for k, v in by_doc.items():
        print(f"  {k}: {len(v):4d} passages, mean {sum(v) / len(v):5.0f} chars, max {max(v)}")


if __name__ == "__main__":
    main()
