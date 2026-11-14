"""Lightweight Markdown cleanup and optional PDF-page annotations."""

import json
import re
import unicodedata

import yaml

PAGE_MARKER = re.compile(r"<!--\s*page:\s*pdf\s+(\d+)\b.*?-->", re.IGNORECASE)
PREPROCESS_VERSION = 3


def prepare_markdown(markdown: str, *, exclude_footnotes=False,
                     numbered_unit_section=None, numbered_unit_label="Paragraf"):
    """Apply explicit retrieval policies while retaining source page comments.

    Numbered units are recognized only inside the named Markdown section.
    Excluded citations remain available in a separate provenance record.
    """
    excluded = []
    report = {"excluded_footnotes": 0, "removed_footnote_references": 0,
              "numbered_units": [], "numbered_unit_label": numbered_unit_label}
    if exclude_footnotes:
        definition = re.compile(r"(?m)^\[\^([^\]\n]+)\]:[^\n]*(?:\n[ \t]{4,}[^\n]*)*")
        definitions = list(definition.finditer(markdown))
        ids = {m.group(1) for m in definitions}
        references = list(re.finditer(r"\[\^([^\]\n]+)\](?!:)", markdown))
        unknown = {m.group(1) for m in references} - ids
        if unknown:
            raise ValueError("Tanımı olmayan dipnot referansları: " + ", ".join(sorted(unknown)))
        for m in definitions:
            preceding = list(PAGE_MARKER.finditer(markdown[:m.start()]))
            excluded.append({"footnote_id": m.group(1), "text": m.group(),
                             "page": int(preceding[-1].group(1)) if preceding else None,
                             "reason": "source_citation_excluded_from_retrieval"})
        markdown = definition.sub("", markdown)
        markdown, count = re.subn(r"\[\^([^\]\n]+)\](?!:)", "", markdown)
        markdown = re.sub(r"\n#{1,6} (?:Dipnotlar|Footnotes)\s*(?:(?:<!--[\s\S]*?-->)|\s)*\Z",
                          "\n", markdown, flags=re.IGNORECASE)
        report.update(excluded_footnotes=len(excluded), removed_footnote_references=count)
    if numbered_unit_section:
        if not re.fullmatch(r"[\w -]+", numbered_unit_label):
            raise ValueError("Geçersiz numaralı birim etiketi.")
        selected, level, context_level, found, ids = False, None, None, 0, []
        transformed = []
        for line in markdown.splitlines(keepends=True):
            heading = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
            if heading:
                context_level = len(heading.group(1))
                if heading.group(2) == numbered_unit_section:
                    selected, level = True, context_level
                    found += 1
                elif selected and context_level <= level:
                    selected = False
            unit = re.match(r"^(\d+)\. (.+?)\s*$", line) if selected else None
            if unit:
                id_, body = unit.groups()
                if id_ in ids:
                    raise ValueError(f"Yinelenen numaralı birim: {id_}")
                ids.append(id_)
                if context_level >= 6:
                    raise ValueError("Numaralı birim için Markdown başlık seviyesi kalmadı.")
                transformed.append("#"*(context_level+1)+f" {numbered_unit_label} {id_}\n\n**{id_}.** {body}\n")
            else:
                transformed.append(line)
        if found != 1 or not ids:
            raise ValueError("Numaralı birim bölümü tam bir kez bulunmalı ve numaralı gövde içermeli.")
        markdown = "".join(transformed)
        report["numbered_units"] = ids
    return markdown, excluded, report


def read_markdown(text: str) -> tuple[str, dict]:
    text = text.lstrip("\ufeff").replace("\r\n", "\n")
    metadata = {}
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if match:
        parsed = yaml.safe_load(match.group(1))
        if isinstance(parsed, dict):
            metadata = json.loads(json.dumps(parsed, ensure_ascii=False, default=str))
            text = text[match.end():]
    return text, metadata


def normalized(text: str) -> str:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.DOTALL)
    text = re.sub(r"(?<=\w)-[ \t]*\n\s*(?=[a-zçğıöşü])", "", text)
    text = re.sub(r"(?m)^\s*#{1,6}\s+", "", text)
    text = re.sub(r"[*_`|]", "", text)
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", text)).casefold().strip()


def conversion_input(markdown: str) -> tuple[str, int]:
    """Remove non-rendered comments and join only explicit line-end hyphens."""
    text = re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)
    return re.subn(r"(?<=\w)-[ \t]*\n\s*(?=[a-zçğıöşü])", "", text)


def annotate_pages(blocks: list[dict], markdown: str) -> int:
    """Keep page markers supplied by the source; never invent page numbers."""
    markers = list(PAGE_MARKER.finditer(markdown))
    if not markers:
        return 0
    pieces, labels = [], []
    prefix = normalized(markdown[:markers[0].start()]) + " "
    pieces.append(prefix)
    labels.extend([None] * len(prefix))
    for i, marker in enumerate(markers):
        end = markers[i+1].start() if i+1 < len(markers) else len(markdown)
        value = normalized(markdown[marker.end():end]) + " "
        pieces.append(value)
        labels.extend([int(marker.group(1))] * len(value))
    source, cursor, matched = "".join(pieces), 0, 0
    # Join a word cut exactly at a PDF page boundary, keeping per-character pages.
    removed = set()
    for match in re.finditer(r"(?<=\w)-\s+(?=\w)", source):
        if labels[match.start()-1] != labels[match.end()] and labels[match.start()-1] is not None:
            removed.update(range(match.start(), match.end()))
    if removed:
        source = "".join(char for i, char in enumerate(source) if i not in removed)
        labels = [page for i, page in enumerate(labels) if i not in removed]
    for block in blocks:
        needle = normalized(block["text"])
        start = source.find(needle, cursor)
        stop = start + len(needle)
        if start < 0 and len(needle) > 180:
            start = source.find(needle[:60], cursor)
            tail = source.find(needle[-60:], start + 60) if start >= 0 else -1
            if tail >= 0 and tail - start < 2 * len(needle) + 2000:
                stop = tail + 60
            else:
                start = -1
        if start < 0:
            continue
        cursor = stop
        pages = sorted({page for page in labels[start:stop] if page is not None})
        if pages:
            block.update(page=pages[0], pages=pages)
            matched += 1
    return matched
