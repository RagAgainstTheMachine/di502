"""The small payload contract shared by uploads, migration, and search."""

from __future__ import annotations

import json
import re
from pathlib import Path

from src.shared.common import valid_document_name, write_jsonl

COMMON_FIELDS = (
    "document_name", "parent_id", "kind", "section", "chunk_index",
    "text",
)
PARAGRAPH_FIELDS = ("document_name", "paragraph_id", "section", "text")
MINIMAL_FIELDS = ("document_name", "section", "text")
PAYLOAD_FIELDS = COMMON_FIELDS + ("page_start", "page_end", "action_id", "paragraph_id", "document_id")
INDEX_FIELDS = {
    "document_name": "keyword",
    "parent_id": "keyword",
    "action_id": "integer",
    "kind": "keyword",
    "paragraph_id": "keyword",
}


def build_payload(record: dict) -> dict:
    """Project a preparation record onto the Cloud payload, omitting nulls."""
    is_paragraph = record.get("paragraph_id") is not None
    fields = PARAGRAPH_FIELDS if is_paragraph else MINIMAL_FIELDS if record.get("compact_payload") else COMMON_FIELDS
    parts = record.get("paragraph_chunk_count", record.get("parent_chunk_count", 1))
    if (is_paragraph or record.get("compact_payload")) and parts > 1:
        # Ordering and expansion are useful only when a paragraph really spans
        # multiple chunks. Internal preparation records retain provenance.
        fields += ("parent_id", "chunk_index")
    missing = [field for field in fields if record.get(field) is None]
    if missing:
        raise ValueError(f"Payload için zorunlu alanlar eksik: {', '.join(missing)}")
    payload = {field: record[field] for field in fields}
    payload["document_name"] = valid_document_name(payload["document_name"])
    start, end = record.get("page_start"), record.get("page_end")
    if (start is None) != (end is None):
        raise ValueError("Sayfa aralığının iki sınırı birlikte bulunmalı.")
    if start is not None:
        if type(start) is not int or type(end) is not int or not 1 <= start <= end:
            raise ValueError("Geçersiz sayfa aralığı.")
        payload.update(page_start=start, page_end=end)
    action_id = record.get("action_id")
    if record.get("kind") == "action" and action_id is None:
        raise ValueError("Eylem chunk'ında action_id eksik.")
    if action_id is not None and not is_paragraph:
        if type(action_id) is not int:
            raise ValueError("action_id sayı (integer) olmalı.")
        payload["action_id"] = action_id
    paragraph_id = record.get("paragraph_id")
    if paragraph_id is not None:
        if not isinstance(paragraph_id, str) or not re.fullmatch(r"\d+(?:\.\d+)*", paragraph_id):
            raise ValueError("paragraph_id, '591.3' gibi bir metin (string) olmalı.")
        payload["paragraph_id"] = paragraph_id
    return payload


def serialized_bytes(payloads: list[dict]) -> int:
    return sum(len(json.dumps(p, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) for p in payloads)


def write_payload_preview(directory: Path, chunks: list[dict]) -> list[dict]:
    records = [{"id": chunk["id"], "payload": build_payload(chunk)} for chunk in chunks]
    write_jsonl(directory / "qdrant_payloads.jsonl", records)
    return records
