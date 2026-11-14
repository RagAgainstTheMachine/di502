"""Validate text-only chunks and embed/upload them with Qdrant Cloud Inference."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from qdrant_client import models
from src.shared.common import DIMENSIONS, MODEL, OUTPUT, cloud_client, load_validated_chunks, valid_document_id, select_bundle, discover_bundles, valid_document_name
from src.shared.payload import INDEX_FIELDS, build_payload, serialized_bytes, write_payload_preview


def document_filter(document_name: str) -> models.Filter:
    return models.Filter(must=[models.FieldCondition(key="document_name", match=models.MatchValue(value=valid_document_name(document_name)))])


def check_collection(info) -> None:
    vector = info.config.params.vectors
    if not isinstance(vector, models.VectorParams) or vector.size != DIMENSIONS or vector.distance != models.Distance.COSINE:
        raise ValueError("Collection, isimsiz 384 boyutlu COSINE vektör kullanmalı. Başka bir collection adı seçin.")


def ensure_payload_indexes(client, collection: str, info) -> None:
    for field, schema in INDEX_FIELDS.items():
        if field not in info.payload_schema:
            client.create_payload_index(
                collection_name=collection, field_name=field,
                field_schema=models.PayloadSchemaType(schema), wait=True,
            )
        elif info.payload_schema[field].data_type != models.PayloadSchemaType(schema):
            raise ValueError(f"{field} payload index tipi {schema} olmalı.")


def ensure_collection(client, collection: str) -> None:
    if not client.collection_exists(collection):
        client.create_collection(collection_name=collection, vectors_config=models.VectorParams(size=DIMENSIONS, distance=models.Distance.COSINE))
    info = client.get_collection(collection)
    check_collection(info)
    ensure_payload_indexes(client, collection, info)


def embedding_document(chunk):
    if chunk["embedding_text"] != chunk["text"]:
        raise ValueError("Yalnızca metin politikası gerekli: prepare.py ile yeni çıktı üretin.")
    return models.Document(text=chunk["text"], model=MODEL)


def index_document(client, collection: str, chunks: list[dict], manifest: dict,
                   output: Path, batch_size=16) -> dict:
    document_id = manifest["document_id"]
    if not chunks or {c["document_id"] for c in chunks} != {document_id}:
        raise ValueError("Belge kapsamı uyuşmuyor; yükleme durduruldu.")
    if any(c["embedding_text"] != c["text"] for c in chunks):
        raise ValueError("Başlık içeren embedding girdisi yüklenemez; prepare.py ile yeni çıktı üretin.")
    document_name = valid_document_name(manifest.get("title") or chunks[0].get("document_name"))
    if any(c.get("document_name") != document_name for c in chunks):
        raise ValueError("Belge adı ile chunk document_name alanları uyuşmuyor.")
    previous_ids, offset = set(), None
    while True:
        records, offset = client.scroll(collection_name=collection, scroll_filter=document_filter(document_name), limit=256, offset=offset, with_payload=False, with_vectors=False)
        previous_ids.update(str(record.id) for record in records)
        if offset is None:
            break
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        points = [models.PointStruct(id=c["id"], vector=embedding_document(c), payload=build_payload(c)) for c in batch]
        client.upsert(collection_name=collection, points=points, wait=True)
        print(f"{document_id}: {min(start + batch_size, len(chunks))}/{len(chunks)} yüklendi", flush=True)
    stale = previous_ids - {str(c["id"]) for c in chunks}
    if stale:
        client.delete(collection_name=collection, points_selector=models.PointIdsList(points=sorted(stale)), wait=True)
    count = client.count(collection_name=collection, count_filter=document_filter(document_name), exact=True).count
    if count != len(chunks):
        raise ValueError(f"{document_id}: Qdrant sayımı {count} != {len(chunks)}")
    result = {"collection": collection, "document_id": document_id, "document_name": document_name, "points": count,
              "model": MODEL, "dimensions": DIMENSIONS, "source_sha256": manifest["source_sha256"],
              "stale_points_removed": len(stale), "embedding_context": "text_only",
              "payload_fields": sorted({field for chunk in chunks for field in build_payload(chunk)})}
    output.mkdir(parents=True, exist_ok=True)
    (output / "index_report.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result

def run(args):
    if args.all:
        directories = discover_bundles(args.output)
    elif args.document_id:
        directories = [select_bundle(args.output, value) for value in dict.fromkeys(args.document_id)]
    else:
        directories = [select_bundle(args.output)]
    bundles = [(directory, *load_validated_chunks(directory)) for directory in directories]
    if any(c["embedding_text"] != c["text"] for _,chunks,_ in bundles for c in chunks):
        raise ValueError("Embedding girdisi yalnızca metin olmalı; prepare.py ile hazırlayın.")
    summaries = []
    for directory,chunks,manifest in bundles:
        preview = write_payload_preview(directory,chunks)
        summaries.append({"document_id":manifest["document_id"],"chunks":len(chunks),
                          "payload_json_bytes":serialized_bytes([r["payload"] for r in preview])})
    if args.dry_run:
        print(json.dumps({"dry_run":True,"documents":summaries,"model":MODEL,
                          "dimensions":DIMENSIONS,"payload_indexes":INDEX_FIELDS},ensure_ascii=False,indent=2))
        return summaries
    client,collection = cloud_client(args.collection)
    try:
        ensure_collection(client,collection)
        results = [index_document(client,collection,chunks,manifest,directory,args.batch_size)
                   for directory,chunks,manifest in bundles]
        print(json.dumps(results,ensure_ascii=False,indent=2))
        return results
    finally:
        client.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    scope = parser.add_mutually_exclusive_group()
    scope.add_argument("--document-id",action="append")
    scope.add_argument("--all",action="store_true")
    parser.add_argument("--output",type=Path,default=OUTPUT)
    parser.add_argument("--collection")
    parser.add_argument("--batch-size",type=int,default=16)
    parser.add_argument("--dry-run",action="store_true")
    args = parser.parse_args()
    if not 1 <= args.batch_size <= 64:
        parser.error("--batch-size 1-64 arasında olmalı.")
    try:
        run(args)
    except (ValueError,OSError) as exc:
        parser.exit(1,f"Hata: {exc}\n")


if __name__ == "__main__":
    main()
