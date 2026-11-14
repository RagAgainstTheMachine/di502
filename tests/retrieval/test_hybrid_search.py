import unittest
from unittest.mock import patch

from qdrant_client import QdrantClient, models

from src.retrieval.search import search
from src.ingestion.setup_hybrid import setup


class LocalClient:
    """Local mode runs real BM25/RRF but omits index metadata from get_collection."""

    def __init__(self):
        self.client = QdrantClient(":memory:")
        self.schema = {}

    def __getattr__(self, name):
        return getattr(self.client, name)

    def get_collection(self, name):
        return self.client.get_collection(name).model_copy(update={"payload_schema": self.schema})

    def create_payload_index(self, **kwargs):
        result = self.client.create_payload_index(**kwargs)
        self.schema[kwargs["field_name"]] = models.PayloadIndexInfo(
            data_type=models.PayloadSchemaType.TEXT, params=kwargs["field_schema"], points=4,
        )
        return result

    def query_points(self, **kwargs):
        # Replace only the remote E5 inference boundary, keeping actual retrieval.
        if isinstance(kwargs.get("query"), models.Document):
            kwargs["query"] = [1.0, 0.0]
        for prefetch in kwargs.get("prefetch", []):
            if isinstance(prefetch.query, models.Document):
                prefetch.query = [1.0, 0.0]
        return self.client.query_points(**kwargs)

    def close(self):
        pass  # search closes its client; test tearDown owns this in-memory store.


class HybridSearchTests(unittest.TestCase):
    def setUp(self):
        self.client = LocalClient()
        self.client.create_collection("docs", vectors_config=models.VectorParams(size=2, distance=models.Distance.COSINE))
        self.client.upsert("docs", points=[
            models.PointStruct(id=1, vector=[1.0, 0.0], payload={"document_name": "A", "section": "Genel", "text": "Verilerin ülke kontrolünde tutulması."}),
            models.PointStruct(id=2, vector=[0.0, 1.0], payload={"document_name": "A", "section": "D12", "text": "Veri Egemenliği Data Sovereignty", "parent_id": "a:p", "chunk_index": 0, "paragraph_id": "12"}),
            models.PointStruct(id=3, vector=[0.0, 1.0], payload={"document_name": "A", "section": "D12", "text": "Kurumsal uygulama açıklaması.", "parent_id": "a:p", "chunk_index": 1, "paragraph_id": "12"}),
            models.PointStruct(id=4, vector=[1.0, 0.0], payload={"document_name": "B", "section": "Genel", "text": "Data Sovereignty Data Sovereignty", "paragraph_id": "12"}),
        ])
        self.cloud = patch("src.retrieval.search.cloud_client", return_value=(self.client, "docs"))
        self.cloud.start()

    def tearDown(self):
        self.cloud.stop()
        self.client.client.close()

    def test_setup_is_idempotent_and_preserves_all_point_content(self):
        first = setup(self.client, "docs")
        second = setup(self.client, "docs")
        self.assertEqual(first["points_sha256"], second["points_sha256"])
        self.assertEqual(first["points"], 4)
        self.assertTrue(first["payloads_and_vectors_unchanged"])

    def test_hybrid_unions_lexical_and_semantic_candidates_with_document_filter(self):
        setup(self.client, "docs")
        # The two branches each select a different A chunk; B must never enter.
        hits = search("Data Sovereignty", candidates=1, limit=2, document_name="A")
        self.assertEqual({h["id"] for h in hits}, {"1", "2"})
        self.assertTrue(all(h["document_name"] == "A" for h in hits))
        self.assertEqual(search("Data Sovereignty", mode="semantic", document_name="A", limit=1)[0]["id"], "1")

    def test_bm25_alias_and_paragraph_filter_and_parent_expansion(self):
        setup(self.client, "docs")
        hits = search("Data Sovereignty", mode="bm25", document_name="A", paragraph_id="12", expand_parent=True)
        self.assertEqual([h["id"] for h in hits], ["2"])
        self.assertIn("Kurumsal uygulama", hits[0]["parent_text"])
        self.assertNotIn("Data Sovereignty Data Sovereignty", hits[0]["parent_text"])

    def test_no_keyword_matches_still_returns_dense_results(self):
        setup(self.client, "docs")
        self.assertEqual(search("eşleşmeyensözcük", mode="bm25"), [])
        self.assertEqual(search("eşleşmeyensözcük", mode="hybrid", document_name="A", limit=1)[0]["id"], "1")

    def test_missing_index_has_actionable_error_but_semantic_still_works(self):
        with self.assertRaisesRegex(ValueError, "src.ingestion.setup_hybrid"):
            search("veri")
        self.assertTrue(search("veri", mode="semantic"))
        with self.assertRaises(ValueError):
            search("veri", mode="wrong")
        with self.assertRaises(ValueError):
            search("veri", candidates=0)


if __name__ == "__main__":
    unittest.main()
