"""Qdrant schema checks shared by ingestion and retrieval."""
from qdrant_client import models


def bm25_ready(info) -> bool:
    field = info.payload_schema.get("text")
    return bool(field and field.data_type == models.PayloadSchemaType.TEXT
                and field.params and field.params.scoring)


