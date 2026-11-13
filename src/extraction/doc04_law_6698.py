"""Extract Law No. 6698 (Doc04) from its PDF into data/text/doc04_law_no_6698.md.

Same output conventions as src/extraction/extract.py (front matter, one
<!-- page: pdf N | printed M --> marker per page, verbatim text):
  - '## ' for each BÖLÜM with its title, '### Madde N - <title>' for each article
    (Geçici Madde N for provisional articles);
  - a paragraph starts at an indented line (x0 > 90 pt); lines starting at the
    left margin continue the paragraph;
  - footnotes (font size < 11.5 pt at the page bottom) are kept as paragraphs
    starting with '> Dipnot N:' where they occur; footnote numbers glued to
    words in the text ('ilişkilidir.2') are kept, as in the other documents;
  - the staff table (I) Sayılı Cetvel and the amendment list are kept line by line.

Usage:
  python src/extraction/doc04_law_6698.py --pdf <path to the 21-page PDF> --out data/text/doc04_law_no_6698.md
Requires pdfplumber (pip install pdfplumber).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import re
from pathlib import Path

import pdfplumber

ARTICLE_RE = re.compile(r"^(GEÇİCİ MADDE|MADDE)\s+(\d+)\s*-")
SECTION_RE = re.compile(r"^[A-ZÇĞİÖŞÜ]+(?:\s+[A-ZÇĞİÖŞÜ]+)?\s+BÖLÜM$")
TABLE_START = ("(I) SAYILI CETVEL", "6698 SAYILI KANUNA EK VE DEĞİŞİKLİK")
INDENT_X = 90      # paragraph start
CENTER_X = 150     # centred headings
FOOTNOTE_SIZE = 11.5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, type=Path)
    ap.add_argument("--out", default="data/text/doc04_law_no_6698.md", type=Path)
    a = ap.parse_args()

    pdf = pdfplumber.open(a.pdf)
    first = pdf.pages[0].extract_text() or ""
    if len(pdf.pages) != 21 or not re.search(r"KİŞİSEL\s+VERİLERİN\s+KORUNMASI\s+KANUNU", first):
        raise SystemExit(f"Not Law 6698: {len(pdf.pages)} pages, first line {first[:60]!r}")

    out: list[str] = []
    para: list[str] = []
    pending_title: str | None = None
    table_mode = False
    n_articles = n_footnotes = 0

    def flush():
        nonlocal para
        if para:
            # a line ending in '-' is glued to the next one and keeps its hyphen ('elektrik-elektronik')
            joined = para[0]
            for part in para[1:]:
                joined += part if joined.endswith("-") else " " + part
            out.append(joined)
            out.append("")
            para = []

    for pn, page in enumerate(pdf.pages, 1):
        flush()
        out += [f"<!-- page: pdf {pn} | printed none -->", ""]
        lines = page.extract_text_lines()
        i = 0
        while i < len(lines):
            ln = lines[i]
            text = ln["text"].strip()
            size = ln["chars"][0]["size"]
            x0 = ln["x0"]
            nxt = lines[i + 1]["text"].strip() if i + 1 < len(lines) else ""

            if pn == 1 and text.startswith(("KİŞİSEL VERİLERİN KORUNMASI KANUNU",)):
                i += 1
                continue
            if size < FOOTNOTE_SIZE:                                  # footnote block
                flush()
                m = re.match(r"^(\d+)\s*(.*)$", text)
                para = [f"> Dipnot {m.group(1)}: {m.group(2)}".rstrip() if m else f"> {text}"]
                n_footnotes += 1 if m else 0
                i += 1
                while i < len(lines) and lines[i]["chars"][0]["size"] < FOOTNOTE_SIZE \
                        and not re.match(r"^\d+\s", lines[i]["text"].strip()) and lines[i]["chars"][0]["size"] > 8:
                    para.append(lines[i]["text"].strip())
                    i += 1
                flush()
                continue
            if any(text.startswith(t) for t in TABLE_START):
                flush()
                title = text
                if text.startswith("6698 SAYILI"):                     # three-line title
                    while i + 1 < len(lines) and lines[i + 1]["x0"] > CENTER_X - 60 and lines[i + 1]["text"].isupper():
                        i += 1
                        title += " " + lines[i]["text"].strip()
                out += [f"## {title}", ""]
                table_mode = True
                i += 1
                continue
            if table_mode:
                out += [text, ""]
                i += 1
                continue
            if x0 > CENTER_X and SECTION_RE.match(text):              # BİRİNCİ BÖLÜM + title line
                flush()
                title = nxt if i + 1 < len(lines) and lines[i + 1]["x0"] > CENTER_X - 30 else ""
                out += [f"## {text}" + (f" - {title}" if title else ""), ""]
                i += 2 if title else 1
                continue
            m = ARTICLE_RE.match(text)
            if m:
                flush()
                kind = "Geçici Madde" if m.group(1).startswith("GEÇİCİ") else "Madde"
                out += [f"### {kind} {m.group(2)}" + (f" - {pending_title}" if pending_title else ""), ""]
                pending_title = None
                n_articles += 1
                para = [text]
                i += 1
                continue
            if x0 > INDENT_X and len(text) < 90 and ARTICLE_RE.match(nxt) and not text.endswith((".", ",", ";", ":")):
                flush()
                pending_title = text                                  # article title line
                i += 1
                continue
            if x0 > INDENT_X:                                         # new paragraph
                flush()
            para.append(text)
            i += 1
    flush()

    # An article title left at the bottom of the previous page ('Suçlar' before MADDE 17):
    # move the short paragraph just before an untitled article heading into the heading.
    for k, line in enumerate(out):
        if re.match(r"^### Madde \d+$", line):
            j = k - 1
            while j >= 0 and (not out[j] or out[j].startswith("<!--")):
                j -= 1
            if j >= 0 and len(out[j]) < 60 and not out[j].startswith(("#", ">")) \
                    and not out[j].endswith((".", ",", ";", ":")):
                out[k] = f"{line} - {out[j]}"
                out[j] = ""
    # Footnote numbers glued to a heading ('Kabahatler1') are dropped from the heading only.
    out = [re.sub(r"(?<=[a-zçğıöşü])\d+$", "", l) if l.startswith("### ") else l for l in out]
    out = [l for n, l in enumerate(out) if not (l == "" and n and out[n - 1] == "")]

    sha = hashlib.sha256(a.pdf.read_bytes()).hexdigest()
    front = [
        "---",
        "doc_id: Doc04",
        'title: "Law No. 6698 on the Protection of Personal Data / 6698 sayılı Kişisel Verilerin Korunması Kanunu"',
        f"source_pdf: {a.pdf.name}",
        f"source_pdf_sha256: {sha}",
        f"source_pdf_pages: {len(pdf.pages)}",
        f'tool: "pdfplumber {pdfplumber.__version__}"',
        "extractor: src/extraction/doc04_law_6698.py",
        f"extraction_date: {dt.date.today().isoformat()}",
        'part_used_inventory: "All, 21 pp."',
        'pages_used: "PDF pages 1–21"',
        "selection_rule: \"All pages; '##' per BÖLÜM, '###' per article (Madde / Geçici Madde); footnotes kept as '> Dipnot N:'; staff table and amendment list kept line by line.\"",
        'page_marker_format: "<!-- page: pdf N | printed M -->  (no page numbers are printed in this PDF)"',
        'verbatim: "text-layer only; line breaks inside a paragraph become spaces"',
        'status: "ok"',
        "---",
        "",
        "# Law No. 6698 on the Protection of Personal Data / 6698 sayılı Kişisel Verilerin Korunması Kanunu",
        "",
    ]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text("\n".join(front + out).rstrip() + "\n", encoding="utf-8")
    print(f"{n_articles} articles, {n_footnotes} footnotes, {len(pdf.pages)} pages -> {a.out}")


if __name__ == "__main__":
    main()
