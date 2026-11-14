"""Structure-aware generic segmentation and token-bounded chunking."""

from __future__ import annotations

import re
import unicodedata
import uuid
from collections import defaultdict

from src.shared.common import MODEL


def clean(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    # Join line-wrapped words, without removing real in-line hyphens (GPU-saat).
    text = re.sub(r"(?<=\w)[-‐]\s*\n\s*(?=\w)", "", text)
    return re.sub(r"\s+", " ", text).strip()



def extract_blocks(document) -> list[dict]:
    from docling_core.types.doc import TableItem, TextItem

    blocks = []
    for item, _ in document.iterate_items(traverse_pictures=True):
        if not hasattr(item, "prov") or str(item.label) in {"page_header", "page_footer"}:
            continue
        page, coordinates = None, None
        if item.prov:
            page = item.prov[0].page_no
            bbox = item.prov[0].bbox.to_top_left_origin(document.pages[page].size.height)
            coordinates = [bbox.l, bbox.t, bbox.r, bbox.b]
        base = {"page": page, "pages": sorted({p.page_no for p in item.prov}), "bbox": coordinates, "source_ref": item.self_ref, "label": str(item.label), "level": getattr(item, "level", 1)}
        if isinstance(item, TextItem):
            if clean(item.text):
                blocks.append({**base, "text": clean(item.text)})
        elif isinstance(item, TableItem):
            for row_no, row in enumerate(item.data.grid):
                cells, seen = [], set()
                for cell in row:
                    key = (cell.start_row_offset_idx, cell.start_col_offset_idx)
                    if key not in seen and clean(cell.text):
                        cells.append(clean(cell.text))
                        seen.add(key)
                if cells:
                    blocks.append({**base, "text": " | ".join(cells), "table_row": row_no})
    return blocks



def segment_generic(blocks: list[dict], document_id: str, title: str) -> list[dict]:
    """Use headings as context; create a section only when it has body content."""
    parents, current, headings = [], None, []
    for block in blocks:
        is_heading = block["label"] in {"section_header", "title"}
        if is_heading:
            level = max(1, int(block.get("level", 1)))
            headings = [(n, text) for n, text in headings if n < level]
            headings.append((level, block["text"]))
            # A contents-page number such as "3-6", or any empty heading,
            # must not become an independent retrieval point. Keep headings
            # in the path for subsequent content instead of indexing them as text.
            current = None
            continue
        if current is None:
            paragraph = re.fullmatch(r"(?:Paragraf|Tedbir|Politika|Öneri)\s+(\d+(?:\.\d+)*)", headings[-1][1], re.IGNORECASE) if headings else None
            context = headings[:-1] if paragraph else headings
            section = " / ".join(text for _, text in context) or title
            current = {
                "document_id": document_id,
                "parent_id": f"{document_id}:section_{len(parents)+1:04d}",
                "title": section, "kind": "section", "action_id": None, "axis": None,
                "blocks": [],
            }
            if paragraph:
                current["paragraph_id"] = paragraph[1]
            parents.append(current)
        current["blocks"].append({**block, "section": current["title"]})
    if not parents:
        raise ValueError("İndekslenecek gövde metni bulunamadı; yalnızca başlıklardan chunk üretilmez. Taranmış PDF için --ocr deneyin.")
    return parents


def shorten_context(text: str, tokenizer, limit: int) -> str:
    words = text.split()
    while words and len(tokenizer.encode(" ".join(words), add_special_tokens=False)) > limit:
        words.pop()
    return " ".join(words)


def chunk_parents(parents: list[dict], tokenizer, max_tokens: int, title: str,
                  merge_peers: bool = False, attach_numbers: bool = False,
                  bound_headings: bool = True) -> tuple[list[dict], list[dict]]:
    from docling.chunking import HybridChunker
    from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
    from docling_core.types.doc import DocItemLabel, DoclingDocument

    # Leave room for the server's passage prefix and the tokenizer's special tokens.
    reserve = len(tokenizer.encode("passage: ", add_special_tokens=False)) + tokenizer.num_special_tokens_to_add(pair=False) + 4
    chunker = HybridChunker(tokenizer=HuggingFaceTokenizer(tokenizer=tokenizer, max_tokens=max_tokens-reserve), merge_peers=merge_peers)
    chunks, summaries = [], []
    for parent in parents:
        parent_chunk_start = len(chunks)
        groups = []
        for block in parent["blocks"]:
            if not groups or groups[-1][0] != block["section"]:
                groups.append((block["section"], []))
            groups[-1][1].append(block)
        chunk_index = 0
        for section, group in groups:
            doc = DoclingDocument(name=parent["parent_id"])
            headings = [title]
            if parent["axis"]:
                headings.append(f"Eksen: {parent['axis']}")
            headings.append(parent["title"])
            if section != parent["title"]:
                headings.append(section)
            # Bound heading overhead for arbitrary documents with very long titles.
            per_heading = max(8, max_tokens // (3 * len(headings)))
            headings = list(dict.fromkeys((shorten_context(h, tokenizer, per_heading) if bound_headings else h) for h in headings if h))
            for level, heading in enumerate(headings, 1):
                doc.add_heading(text=heading, level=level)
            references = {}
            bundles, pending = [], []
            for block in group:
                numeric_label = re.fullmatch(r"\d+\.?(?:\s*[-–—]\s*\d+\.?)?", block["text"])
                field_label = block["text"].endswith(":") and len(block["text"].split()) <= 8
                if attach_numbers and (numeric_label or field_label):
                    pending.append(block)
                else:
                    bundles.append(pending + [block])
                    pending = []
            if pending:
                if bundles:
                    bundles[-1].extend(pending)
                else:
                    bundles.append(pending)
            for bundle in bundles:
                item = doc.add_text(label=DocItemLabel.TEXT, text="\n\n".join(b["text"] for b in bundle))
                references[item.self_ref] = bundle
            for child in chunker.chunk(dl_doc=doc):
                text = child.text
                # Headings guide structural chunking and remain in metadata.
                # The selected retrieval policy embeds only the original body.
                embedding_text = text
                count = len(tokenizer.encode("passage: " + embedding_text, add_special_tokens=True, truncation=False))
                if count > max_tokens:
                    raise ValueError(f"Token sınırı aşıldı: {parent['parent_id']} {count}>{max_tokens}")
                sources = [block for i in child.meta.doc_items if i.self_ref in references for block in references[i.self_ref]]
                pages = sorted({p for b in sources for p in b["pages"]})
                if not sources:
                    raise ValueError("Chunk'ın kaynak blok referansları kayboldu.")
                identity = f"{parent['parent_id']}:{chunk_index}:{text}"
                chunks.append({"id": str(uuid.uuid5(uuid.NAMESPACE_URL, identity)), "document_id": parent["document_id"], "parent_id": parent["parent_id"], "action_id": parent["action_id"], "axis": parent["axis"], "kind": parent["kind"], "title": parent["title"], "section": section, "chunk_index": chunk_index, "text": text, "embedding_text": embedding_text, "embedding_model": MODEL, "token_count": count, "pages": pages, "page_start": min(pages) if pages else None, "page_end": max(pages) if pages else None, "source_refs": list(dict.fromkeys(b["source_ref"] for b in sources))})
                if "paragraph_id" in parent:
                    chunks[-1]["paragraph_id"] = parent["paragraph_id"]
                chunk_index += 1
        # HybridChunker budgets structural headings too. In text-only generic
        # mode a whole section may therefore fit the real embedding budget
        # even though heading overhead caused multiple children. Merge those
        # children when peer merging was requested and the actual body fits.
        if merge_peers and attach_numbers and len(groups) == 1 and chunk_index > 1:
            children = chunks[parent_chunk_start:]
            joined = "\n\n".join(c["text"] for c in children)
            joined_count = len(tokenizer.encode("passage: " + joined, add_special_tokens=True, truncation=False, verbose=False))
            if joined_count <= max_tokens:
                merged = dict(children[0])
                merged.update(text=joined, embedding_text=joined, token_count=joined_count,
                              source_refs=list(dict.fromkeys(ref for c in children for ref in c["source_refs"])))
                merged_pages = sorted({p for c in children for p in c["pages"]})
                merged.update(pages=merged_pages, page_start=min(merged_pages) if merged_pages else None,
                              page_end=max(merged_pages) if merged_pages else None)
                merged["id"] = str(uuid.uuid5(uuid.NAMESPACE_URL, f"{parent['parent_id']}:0:{joined}"))
                chunks[parent_chunk_start:] = [merged]
                chunk_index = 1
        if "paragraph_id" in parent and chunk_index > 1:
            for chunk in chunks[parent_chunk_start:]:
                chunk["paragraph_chunk_count"] = chunk_index
        pages = sorted({p for b in parent["blocks"] for p in b["pages"]})
        summaries.append({k: v for k, v in parent.items() if k != "blocks"} | {"text": "\n\n".join(b["text"] for b in parent["blocks"]), "page_start": min(pages) if pages else None, "page_end": max(pages) if pages else None, "chunk_count": chunk_index})
    return chunks, summaries



def validate(chunks: list[dict], parents: list[dict], tokenizer, max_tokens: int) -> dict:
    errors = []
    by_parent = defaultdict(list)
    for chunk in chunks:
        by_parent[chunk["parent_id"]].append(chunk)
        actual = len(tokenizer.encode("passage: " + chunk["embedding_text"], add_special_tokens=True, truncation=False))
        if actual != chunk["token_count"] or actual > max_tokens:
            errors.append(f"Token sayımı hatalı: {chunk['id']}")
        markers = {int(m) for m in re.findall(r"(?:^|\n)Eylem\s+(\d+)\s*[-–—]", chunk["text"])}
        if chunk["kind"] == "action" and markers and markers != {chunk["action_id"]}:
            errors.append(f"Eylem sınırı karışmış: {chunk['id']}")
    for parent in parents:
        children = by_parent[parent["parent_id"]]
        # Lossless text check: splitting must neither omit nor duplicate source text.
        original = re.sub(r"\s+", "", parent["text"])
        reconstructed = re.sub(r"\s+", "", "".join(c["text"] for c in children))
        if original != reconstructed:
            errors.append(f"Parent metni child'lardan yeniden oluşturulamıyor: {parent['parent_id']}")
        if parent["kind"] == "glossary" and (len(children) != 1 or not children[0]["text"].startswith(parent["title"] + ":")):
            errors.append(f"Sözlük kavram/tanım çifti bölünmüş: {parent['title']}")
    if len({c["id"] for c in chunks}) != len(chunks):
        errors.append("Yinelenen chunk ID.")
    if not chunks:
        errors.append("Chunk üretilemedi.")
    return {"errors": errors, "actions": sum(p["kind"] == "action" for p in parents), "glossary_terms": sum(p["kind"] == "glossary" for p in parents), "max_observed_tokens": max((c["token_count"] for c in chunks), default=0), "parent_text_reconstruction": not errors}

