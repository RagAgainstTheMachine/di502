"""Shared configuration and small IO helpers. Never log credentials."""

from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from pathlib import Path

from dotenv import load_dotenv
import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config/rag.yaml"
CONFIG = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
OUTPUT = ROOT / CONFIG["paths"]["processed"]
MODEL = CONFIG["models"]["embedding"]["name"]
DIMENSIONS = CONFIG["models"]["embedding"]["dimensions"]
TOKEN_LIMIT = CONFIG["chunking"]["size"]
MODEL_CONTEXT = CONFIG["models"]["embedding"]["context_tokens"]
SEARCH_MODE = CONFIG["retrieval"]["mode"]
TOP_K = CONFIG["retrieval"]["top_k"]
CANDIDATES = CONFIG["retrieval"]["candidates"]
EXPAND_PARENT = CONFIG["retrieval"]["expand_parent"]
BM25_FIELD = CONFIG["retrieval"]["bm25"]["field"]
BM25_INDEX = {"type": "text", "scoring": True,
              "tokenizer": CONFIG["retrieval"]["bm25"]["tokenizer"],
              "lowercase": CONFIG["retrieval"]["bm25"]["lowercase"]}
if CONFIG["chunking"]["overlap"] != 0 or BM25_FIELD != "text":
    raise ValueError("Bu akış overlap=0 ve yalnızca text alanında BM25 kullanır.")


def valid_document_id(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}", value) or value in {".", ".."}:
        raise ValueError("document_id 1-128 karakter olmalı; harf, sayı, nokta, alt çizgi ve tire kullanılabilir.")
    return value


def valid_document_name(value: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("document_name boş olmayan bir belge adı olmalı.")
    return value.strip()


def default_document_id(source: Path) -> str:
    """Stable logical ID across edits; paths below data/ survive repo moves."""
    try:
        key = source.resolve().relative_to((ROOT / "data").resolve()).as_posix()
    except ValueError:
        key = source.name
    slug = unicodedata.normalize("NFKD", source.stem).encode("ascii", "ignore").decode().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")[:60] or "document"
    return f"{slug}-{hashlib.sha256(key.encode()).hexdigest()[:10]}"


def select_bundle(output: Path, document_id: str | None = None) -> Path:
    if document_id:
        valid_document_id(document_id)
        nested = output / document_id
        if (nested / "manifest.json").is_file():
            return nested
    if (output / "manifest.json").is_file():
        chunks, manifest = load_validated_chunks(output)
        if document_id is None or manifest["document_id"] == document_id:
            return output
    raise ValueError("Hazırlanmış belge bulunamadı. --document-id seçin veya önce prepare.py çalıştırın.")


def discover_bundles(output: Path) -> list[Path]:
    paths = ([output] if (output / "manifest.json").is_file() else [])
    paths += sorted(p.parent for p in output.glob("*/manifest.json"))
    seen = {}
    for path in paths:
        _, manifest = load_validated_chunks(path)
        doc_id = manifest["document_id"]
        if doc_id in seen:
            raise ValueError(f"Aynı document_id için iki çıktı var: {seen[doc_id]} ve {path}; açıkça --document-id seçin.")
        seen[doc_id] = path
    if not paths:
        raise ValueError("Hazırlanmış belge bulunamadı.")
    return paths


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}:{line_number}: geçersiz JSON") from exc
    return records


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records), encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cloud_settings() -> tuple[str, str, str]:
    load_dotenv(ROOT / ".env", override=False)
    url = os.getenv("QDRANT_URL", "").strip()
    key = os.getenv("QDRANT_API_KEY", "").strip()
    collection = os.getenv("QDRANT_COLLECTION", CONFIG["qdrant"]["collection"]).strip()
    if not url.startswith("https://") or not key or "YOUR-CLUSTER" in url:
        raise ValueError(".env içinde geçerli QDRANT_URL (https) ve QDRANT_API_KEY gerekli.")
    if not collection:
        raise ValueError("QDRANT_COLLECTION boş olamaz.")
    return url, key, collection


def cloud_client(collection_name: str | None = None):
    from qdrant_client import QdrantClient

    url, key, collection = cloud_settings()
    return QdrantClient(url=url, api_key=key, cloud_inference=True, timeout=120), collection_name or collection


def load_validated_chunks(directory: Path) -> tuple[list[dict], dict]:
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("model") != MODEL or manifest.get("dimensions") != DIMENSIONS or manifest.get("validation", {}).get("errors") != []:
        raise ValueError("Hazırlama raporu geçerli değil; prepare.py çalıştırın.")
    for filename in ("chunks.jsonl", "parents.jsonl"):
        if sha256(directory / filename) != manifest["files"][filename]:
            raise ValueError(f"{filename} doğrulamadan sonra değişmiş; prepare.py ile yeniden üretin.")
    for filename in ("excluded_chunks.jsonl", "excluded_parents.jsonl", "chunking_source.md", "excluded_footnotes.jsonl", "markdown_preprocessing.json", "retrieval_input.md", "guide_preprocessing.json", "source_exclusions.jsonl"):
        if filename in manifest["files"] and sha256(directory / filename) != manifest["files"][filename]:
            raise ValueError(f"{filename} inceleme kaydı değişmiş; yeniden hazırlayın.")
    chunks = read_jsonl(directory / "chunks.jsonl")
    if not chunks or len(chunks) != manifest["chunk_count"]:
        raise ValueError("Chunk sayısı manifest ile uyuşmuyor.")
    ids = set()
    document_ids = {chunk.get("document_id") for chunk in chunks}
    if len(document_ids) != 1 or None in document_ids:
        raise ValueError("Bir hazırlama çıktısı tam olarak bir document_id içermeli.")
    document_id = valid_document_id(next(iter(document_ids)))
    if manifest.get("document_id", document_id) != document_id:
        raise ValueError("Manifest document_id ile chunk'lar uyuşmuyor.")
    manifest["document_id"] = document_id  # Old single-document bundles remain readable.
    document_name = valid_document_name(manifest["title"])
    for chunk in chunks:
        chunk.setdefault("document_name", document_name)
        if chunk["document_name"] != document_name:
            raise ValueError("Chunk document_name ile belge başlığı uyuşmuyor.")
        if manifest.get("embedding_context") == "text_only" and chunk.get("embedding_text") != chunk.get("text"):
            raise ValueError("text_only çıktısında embedding_text, text ile birebir aynı olmalı.")
        if chunk["id"] in ids:
            raise ValueError("Yinelenen ID veya yanlış document_id.")
        ids.add(chunk["id"])
        if not chunk["parent_id"].startswith(document_id + ":"):
            raise ValueError("Parent kimliği farklı bir belgeye ait.")
        if chunk.get("embedding_model") != MODEL or not chunk["text"].strip() or not 0 < chunk["token_count"] <= min(manifest["max_tokens"], MODEL_CONTEXT):
            raise ValueError("Boş metin veya token sınırını aşan chunk.")
    return chunks, manifest
