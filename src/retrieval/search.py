"""Qdrant'taki doküman chunk'larını ara; bulunan metinleri ve kaynaklarını göster."""

from __future__ import annotations

import argparse
import json

from qdrant_client import models

from src.shared.common import (BM25_FIELD, CANDIDATES, EXPAND_PARENT, MODEL, SEARCH_MODE, TOP_K,
                               cloud_client, valid_document_id, valid_document_name)
from src.shared.payload import PAYLOAD_FIELDS
from src.shared.qdrant import bm25_ready


def search(query: str, action: int | None = None, limit: int = TOP_K, expand_parent: bool = EXPAND_PARENT,
           kind: str | None = None, document_id: str | list[str] | None = None,
           collection: str | None = None, paragraph_id: str | None = None,
           document_name: str | list[str] | None = None,
           mode: str = SEARCH_MODE, candidates: int = CANDIDATES) -> list[dict]:
    if not query.strip() or not 1 <= limit <= 100:
        raise ValueError("Sorgu boş olamaz; limit 1-100 arasında olmalı.")
    if mode not in {"semantic", "bm25", "hybrid"}:
        raise ValueError("mode semantic, bm25 veya hybrid olmalı.")
    if not 1 <= candidates <= 1000:
        raise ValueError("candidates 1-1000 arasında olmalı.")
    conditions = []
    if document_name:
        names = [document_name] if isinstance(document_name, str) else document_name
        conditions.append(models.FieldCondition(key="document_name", match=models.MatchAny(any=[valid_document_name(x) for x in names])))
    if document_id:
        ids = [document_id] if isinstance(document_id, str) else document_id
        conditions.append(models.FieldCondition(key="document_id", match=models.MatchAny(any=[valid_document_id(x) for x in ids])))
    if action is not None:
        conditions.append(models.FieldCondition(key="action_id", match=models.MatchValue(value=action)))
    if kind is not None:
        conditions.append(models.FieldCondition(key="kind", match=models.MatchValue(value=kind)))
    if paragraph_id is not None:
        if not isinstance(paragraph_id, str) or not paragraph_id.strip():
            raise ValueError("paragraph_id boş olmayan bir metin olmalı.")
        conditions.append(models.FieldCondition(key="paragraph_id", match=models.MatchValue(value=paragraph_id)))
    client, collection = cloud_client(collection)
    try:
        query_filter = models.Filter(must=conditions) if conditions else None
        request = dict(collection_name=collection, query_filter=query_filter,
                       limit=limit, with_payload=list(PAYLOAD_FIELDS), with_vectors=False)
        if mode != "semantic" and not bm25_ready(client.get_collection(collection)):
            raise ValueError("BM25 indeksi yok. Önce python -m src.ingestion.setup_hybrid --collection ile bu collection'ı hazırlayın.")
        if mode == "semantic":
            request["query"] = models.Document(text=query, model=MODEL)
        elif mode == "bm25":
            request.update(query=models.TextQuery(text=query), using=BM25_FIELD)
        else:
            candidate_limit = max(limit, candidates)
            request.update(
                prefetch=[
                    models.Prefetch(query=models.Document(text=query, model=MODEL),
                                    filter=query_filter, limit=candidate_limit),
                    models.Prefetch(query=models.TextQuery(text=query), using=BM25_FIELD,
                                    filter=query_filter, limit=candidate_limit),
                ],
                query=models.RrfQuery(rrf=models.Rrf()),
            )
        response = client.query_points(**request)
        results = [{"id": str(point.id), "score": point.score, **(point.payload or {})} for point in response.points]
        if expand_parent:
            parents = {}
            for result in results:
                parent_id = result.get("parent_id")
                if parent_id is None:
                    continue
                document_key = "document_name" if result.get("document_name") else "document_id"
                parent_key = (result[document_key], parent_id)
                if parent_key not in parents:
                    records, offset = [], None
                    while True:
                        page, offset = client.scroll(collection_name=collection, scroll_filter=models.Filter(must=[models.FieldCondition(key=document_key, match=models.MatchValue(value=result[document_key])), models.FieldCondition(key="parent_id", match=models.MatchValue(value=parent_id))]), limit=256, offset=offset, with_payload=["text", "chunk_index"], with_vectors=False)
                        records.extend(p.payload for p in page)
                        if offset is None:
                            break
                    parents[parent_key] = "\n\n".join(p["text"] for p in sorted(records, key=lambda p: p["chunk_index"]))
                result["parent_text"] = parents[parent_key]
        return results
    finally:
        client.close()


def format_result(item: dict, rank: int) -> str:
    details = [f"{rank}. skor={item['score']:.4f}", f"belge={item.get('document_name', item.get('document_id', ''))}"]
    if item.get("action_id") is not None:
        details.append(f"eylem={item['action_id']}")
    if item.get("paragraph_id") is not None:
        details.append(f"paragraf={item['paragraph_id']}")
    start, end = item.get("page_start"), item.get("page_end")
    if start is not None and end is not None:
        pages = str(start) if start == end else f"{start}-{end}"
        details.append(f"kaynak PDF s.{pages}")
    lines = [" | ".join(details)]
    if item.get("section"):
        lines.append(f"Bölüm: {item['section']}")
    if "parent_text" in item:
        lines.append("Genişletilmiş bölüm metni:")
    lines.append(item.get("parent_text", item["text"]))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--action", type=int, help="action_id içeren eylem profili verileri için filtre; genel MD akışında bu alan üretilmez.")
    parser.add_argument("--document-name", action="append", help="Tam belge adıyla filtre; tekrarlanabilir. Verilmezse tüm belgeler.")
    parser.add_argument("--document-id", action="append", help="Eski document_id payload'ları için arşiv filtresi.")
    parser.add_argument("--collection")
    parser.add_argument("--paragraph-id", help="Paragraf/politika numarası filtresi; örneğin 591.3.")
    parser.add_argument("--kind", choices=("action", "section", "glossary"), help="Yalnızca belirtilen türdeki chunk'ları ara.")
    parser.add_argument("--limit", type=int, default=TOP_K)
    parser.add_argument("--mode", choices=("semantic", "bm25", "hybrid"), default=SEARCH_MODE,
                        help="Varsayılan hybrid: E5 ve yalnızca text alanındaki BM25 sıralarını RRF ile birleştirir.")
    parser.add_argument("--candidates", type=int, default=CANDIDATES,
                        help="Hybrid aramada her koldan alınacak aday sayısı (1-1000, en az limit).")
    parser.add_argument("--expand-parent", action=argparse.BooleanOptionalAction, default=EXPAND_PARENT, help="Aynı parent_id'ye bağlı child metinlerini sırasıyla getir.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not args.query.strip() or not 1 <= args.limit <= 100:
        parser.error("Sorgu boş olamaz; --limit 1-100 arasında olmalı.")
    try:
        results = search(args.query, action=args.action, limit=args.limit,
                         expand_parent=args.expand_parent, kind=args.kind,
                         document_id=args.document_id, collection=args.collection,
                         paragraph_id=args.paragraph_id, document_name=args.document_name,
                         mode=args.mode, candidates=args.candidates)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for rank, item in enumerate(results, 1):
                print("\n" + format_result(item, rank))
            if not results:
                print("Sonuç bulunamadı.")
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Hata: {exc}\n")


if __name__ == "__main__":
    main()
