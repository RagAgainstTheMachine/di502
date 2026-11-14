import tempfile
import re
import unittest
from pathlib import Path
from unittest.mock import patch

from qdrant_client import QdrantClient

from src.shared.common import DIMENSIONS, load_validated_chunks
from src.ingestion.index import ensure_collection, index_document
from src.shared.payload import build_payload
from src.ingestion.prepare import prepare_document
from src.retrieval.search import format_result, search


class ParagraphMetadata(unittest.TestCase):
    def test_heading_overhead_does_not_split_a_body_that_fits_text_only_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "context.md"
            body = "Yapay zekâ uygulamaları kurumların karar alma süreçlerini güçlendirecektir. " * 19
            source.write_text("# Program\n\n## Bilgi ve iletişim teknolojileri kapsamında kurumsal kapasitenin geliştirilmesi ve dijital dönüşüm çalışmalarının yürütülmesi\n\n" + body, encoding="utf-8")
            prepare_document(source, root / "output", document_id="context", max_tokens=300, merge_peers=True, compact_payload=True)
            chunks, _ = load_validated_chunks(root / "output/context")
            self.assertEqual(len(chunks), 1)
            self.assertLessEqual(chunks[0]["token_count"], 300)
            self.assertEqual(re.sub(r"\s+", "", chunks[0]["text"]), re.sub(r"\s+", "", body))

    def test_activity_numbers_stay_with_their_text_across_chunk_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "activities.md"
            activities = [f"**{n}.** Faaliyet {n} kapsamında yapay zekâ destekli analiz altyapısı geliştirilecek ve kamu kurumlarının değerlendirme kapasitesi artırılacaktır." for n in range(1, 16)]
            source.write_text("# Program\n\n## Maliye\n\n### Tedbir 397.5\n\n**Yürütülecek Faaliyetler ve Projeler:**\n\n" + "\n\n".join(activities), encoding="utf-8")
            prepare_document(source, root / "output", document_id="activities", max_tokens=96, merge_peers=True, compact_payload=True)
            chunks, _ = load_validated_chunks(root / "output/activities")
            self.assertGreater(len(chunks), 1)
            for number in range(1, 16):
                self.assertTrue(any(re.search(rf"(?:^|\s){number}\.\s+Faaliyet {number} kapsamında", c["text"]) for c in chunks), number)
            self.assertFalse(any(re.search(r"(?:^|\n)\d+\.$", c["text"]) or c["text"].endswith(":") for c in chunks))

    def test_measure_headers_and_compact_narrative_payload_preserve_activities(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "program.md"
            source.write_text(
                "# Yıllık Program\n\n## Eğitim\n\n### a) Mevcut Durum\n\n"
                "<!-- page: pdf 278 -->\nYapay zekâ programları açılmıştır.\n\n"
                "### c) Politika ve Tedbirler\n\n#### Tedbir 665.2\n\n"
                "<!-- page: pdf 282 -->\n**Politika/Tedbir:** Tedbir 665.2. Teknolojiler kullanılacaktır.\n\n"
                "**Sorumlu:** Millî Eğitim Bakanlığı.\n\n"
                "**1.** Araştırma elektronik ortamda gerçekleştirilecektir.\n\n"
                "**2.** Yapay zekâ ile açık uçlu cevaplar puanlanacaktır.\n",
                encoding="utf-8",
            )
            prepare_document(source, root / "output", document_id="annual-program", merge_peers=True, compact_payload=True)
            chunks, _ = load_validated_chunks(root / "output/annual-program")
            self.assertEqual(len(chunks), 2)
            narrative, measure = chunks
            self.assertNotIn("paragraph_id", narrative)
            self.assertEqual(set(build_payload(narrative)), {"document_name", "section", "text", "page_start", "page_end"})
            self.assertEqual(measure["paragraph_id"], "665.2")
            self.assertEqual(measure["section"], "Eğitim / c) Politika ve Tedbirler")
            normalized = re.sub(r"\s+", " ", measure["text"])
            self.assertIn("1. Araştırma", normalized)
            self.assertIn("2. Yapay zekâ", normalized)
            self.assertEqual(measure["pages"], [282])
            self.assertEqual(set(build_payload(measure)), {"document_name", "paragraph_id", "section", "text", "page_start", "page_end"})

    def test_prepare_payload_and_search_keep_sibling_policy_numbers_distinct(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "policies.md"
            source.write_text(
                "# Plan\n\n## Bilgi ve İletişim Teknolojileri\n\n"
                "### Paragraf 591.2\n\n<!-- page: pdf 143 -->\n"
                "591.2. Uluslararası işbirlikleri artırılacaktır.\n\n"
                "### Paragraf 591.3\n\n<!-- page: pdf 144 -->\n"
                "591.3. Gerekli hukuki düzenlemeler yapılacaktır.\n",
                encoding="utf-8",
            )
            manifest = prepare_document(source, root / "output", document_id="policies", title="Örnek Politika Belgesi (2024–2028)", merge_peers=True)
            bundle = root / "output/policies"
            chunks, _ = load_validated_chunks(bundle)
            self.assertEqual([c["paragraph_id"] for c in chunks], ["591.2", "591.3"])
            self.assertEqual(len({c["parent_id"] for c in chunks}), 2)
            self.assertTrue(all(c["section"] == "Bilgi ve İletişim Teknolojileri" for c in chunks))
            self.assertEqual([c["pages"] for c in chunks], [[143], [144]])
            self.assertTrue(all(build_payload(c)["paragraph_id"] == c["paragraph_id"] for c in chunks))
            expected_fields = {"document_name", "paragraph_id", "section", "text", "page_start", "page_end"}
            self.assertTrue(all(set(build_payload(c)) == expected_fields for c in chunks))
            client = QdrantClient(":memory:")
            vector = [1.0] + [0.0] * (DIMENSIONS - 1)
            try:
                with patch("src.ingestion.index.embedding_document", return_value=vector):
                    ensure_collection(client, "policies")
                    index_document(client, "policies", chunks, manifest, bundle)
                original_query = client.query_points

                def local_query(**kwargs):
                    kwargs["query"] = vector
                    return original_query(**kwargs)

                with patch("src.retrieval.search.cloud_client", return_value=(client, "policies")), patch.object(client, "close"), patch.object(client, "query_points", side_effect=local_query):
                    hits = search("Hukuki düzenlemeler", mode="semantic", paragraph_id="591.3", document_name=manifest["title"], expand_parent=True)
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits[0]["paragraph_id"], "591.3")
                self.assertEqual(hits[0]["document_name"], manifest["title"])
                self.assertNotIn("document_id", hits[0])
                self.assertIn("hukuki düzenlemeler", hits[0]["text"])
                self.assertNotIn("parent_text", hits[0])
                self.assertEqual(set(hits[0]) - {"id", "score"}, expected_fields)
                self.assertIn("paragraf=591.3", format_result(hits[0], 1))
            finally:
                client.close()

    def test_paragraph_id_must_remain_a_string(self):
        record = {"document_id": "plan", "document_name": "Plan", "parent_id": "plan:section_1", "kind": "section",
                  "section": "Hukuk", "chunk_index": 0, "text": "Düzenlemeler yapılacak."}
        self.assertNotIn("paragraph_id", build_payload(record))
        with self.assertRaisesRegex(ValueError, "paragraph_id"):
            build_payload({**record, "paragraph_id": 591.3})

    def test_long_paragraph_retains_expansion_and_chunk_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "long.md"
            sentence = "Güvenilir yapay zekâ sistemleri düzenli olarak değerlendirilecektir. "
            source.write_text("# Plan\n\n## Güvenlik\n\n### Paragraf 591.3\n\n" + sentence * 45, encoding="utf-8")
            manifest = prepare_document(source, root / "output", document_id="long-policy", max_tokens=96, merge_peers=True)
            bundle = root / "output/long-policy"
            chunks, _ = load_validated_chunks(bundle)
            self.assertGreater(len(chunks), 1)
            self.assertTrue(all(c["paragraph_chunk_count"] == len(chunks) for c in chunks))
            self.assertTrue(all(set(build_payload(c)) == {"document_name", "paragraph_id", "section", "text", "parent_id", "chunk_index"} for c in chunks))
            client = QdrantClient(":memory:")
            vector = [1.0] + [0.0] * (DIMENSIONS - 1)
            try:
                with patch("src.ingestion.index.embedding_document", return_value=vector):
                    ensure_collection(client, "policies")
                    index_document(client, "policies", chunks, manifest, bundle)
                original_query = client.query_points

                def local_query(**kwargs):
                    kwargs["query"] = vector
                    return original_query(**kwargs)

                with patch("src.retrieval.search.cloud_client", return_value=(client, "policies")), patch.object(client, "close"), patch.object(client, "query_points", side_effect=local_query):
                    hits = search("Güvenlik", mode="semantic", paragraph_id="591.3", limit=1, expand_parent=True)
                expected = "\n\n".join(c["text"] for c in sorted(chunks, key=lambda c: c["chunk_index"]))
                self.assertEqual(hits[0]["parent_text"], expected)
            finally:
                client.close()


if __name__ == "__main__":
    unittest.main()
