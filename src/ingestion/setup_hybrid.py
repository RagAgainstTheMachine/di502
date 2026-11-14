"""Mevcut metin payload'ına BM25 indeksi ekle; point ve E5 vektörlerini koru."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from qdrant_client import models

from src.shared.common import BM25_INDEX, OUTPUT, cloud_client
from src.shared.qdrant import bm25_ready


def ensure_bm25_index(client, collection: str) -> None:
    info = client.get_collection(collection)
    if bm25_ready(info):
        return
    if "text" in info.payload_schema:
        raise ValueError("text alanında farklı bir indeks var; otomatik olarak üzerine yazılmadı.")
    client.create_payload_index(
        collection_name=collection, field_name="text",
        field_schema=models.TextIndexParams(**BM25_INDEX), wait=True,
    )
    if not bm25_ready(client.get_collection(collection)):
        raise ValueError("BM25 indeksi doğrulanamadı. Sunucu BM25 text scoring desteği gerektirir.")


def point_fingerprint(client, collection: str) -> tuple[int, str]:
    """Hash point IDs, complete payloads and vectors without logging their content."""
    digests, offset = {}, None
    while True:
        points, offset = client.scroll(
            collection_name=collection, offset=offset, limit=256,
            with_payload=True, with_vectors=True,
        )
        for point in points:
            value = json.dumps(
                {"payload": point.payload, "vector": point.vector},
                sort_keys=True, separators=(",", ":"), allow_nan=False,
            ).encode()
            digests[str(point.id)] = hashlib.sha256(value).hexdigest()
        if offset is None:
            break
    value = json.dumps(digests, sort_keys=True, separators=(",", ":")).encode()
    return len(digests), hashlib.sha256(value).hexdigest()


def setup(client, collection: str) -> dict:
    before = point_fingerprint(client, collection)
    ensure_bm25_index(client, collection)
    after = point_fingerprint(client, collection)
    if before != after:
        raise ValueError("Kurulum sırasında point içeriği değişti; eşzamanlı yüklemeleri kontrol edin.")
    return {
        "collection": collection, "points": after[0],
        "payloads_and_vectors_unchanged": True, "points_sha256": after[1],
        "text_index": client.get_collection(collection).payload_schema["text"].model_dump(mode="json"),
        "retrieval": "E5 dense + text BM25 + RRF",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection")
    parser.add_argument("--report", type=Path, default=OUTPUT / "hybrid_setup.json")
    args = parser.parse_args()
    client, collection = cloud_client(args.collection)
    try:
        result = setup(client, collection)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        client.close()


if __name__ == "__main__":
    main()
