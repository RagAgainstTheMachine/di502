"""Answer layer checks with a fake search and a fake language model (no Qdrant, no Ollama)."""
import unittest

from src.app.answer import answer, asks_for_compliance, renumber
from src.app.catalog import collection_date, document_facts, turkish_date

PLAN = "Türkiye Yapay Zekâ Eylem Planı 2026-2030"
REPORT = "TBMM Yapay Zekâ Araştırma Komisyonu Raporu (Sıra Sayısı 260)"
HITS = [
    {"document_name": PLAN, "section": "EKSEN 2", "action_id": 7, "page_start": 28, "page_end": 28,
     "text": "Tüm kurumlar 12 hafta içinde üç yıllık Yapay Zekâ Yol Haritası'nı hazırlayacaktır."},
    {"document_name": PLAN, "section": "EKSEN 1", "page_start": 10, "page_end": 11, "text": "Başka bir metin."},
    {"document_name": REPORT, "section": "4.4.3.4", "page_start": 756, "page_end": 756,
     "text": "İç politika oluşturulmasının zorunlu tutulması önerilmektedir."},
]


def fake_search(_question):
    return HITS


class AnswerTests(unittest.TestCase):
    def test_cited_answer_is_renumbered_and_carries_source_facts(self):
        result = answer("Yol haritası ne kadar sürede hazırlanmalı?", fake_search,
                        lambda prompt: "Kurumlar 12 hafta içinde hazırlar [1]. Komisyon bunu önerir [3].")
        self.assertEqual(result["status"], "answer")
        self.assertEqual(result["answer"], "Kurumlar 12 hafta içinde hazırlar [1]. Komisyon bunu önerir [2].")
        first, second = result["sources"]
        self.assertEqual((first["n"], first["doc_id"], first["legal_status"]), (1, "Doc01", "Politika / plan"))
        self.assertEqual(first["location"], "Eylem 7 · EKSEN 2 · PDF s. 28")
        self.assertEqual(first["date"], "13.06.2026 (açıklanma)")
        self.assertTrue(first["url"].startswith("https://sanayi.gov.tr/"))
        self.assertEqual((second["doc_id"], second["legal_category"]), ("Doc05", "report"))

    def test_prompt_contains_sources_with_legal_status(self):
        seen = {}

        def capture(prompt):
            seen["prompt"] = prompt
            return "Cevap [1]."
        answer("Soru?", fake_search, capture)
        self.assertIn("[3] Belge: TBMM Yapay Zekâ Araştırma Komisyonu Raporu", seen["prompt"])
        self.assertIn("Hukuki statü: Rapor (öneri)", seen["prompt"])
        self.assertIn("SORU: Soru?", seen["prompt"])

    def test_model_says_no_answer(self):
        result = answer("Yarın hava nasıl?", fake_search, lambda prompt: "CEVAP_YOK")
        self.assertEqual((result["status"], result["reason"]), ("decline", "no_answer"))
        self.assertIn("Millî Teknoloji ve Yapay Zekâ Genel Müdürlüğüne", result["notice"])
        self.assertEqual(result["sources"], [])

    def test_answer_without_valid_citation_is_declined(self):
        result = answer("Soru?", fake_search, lambda prompt: "Bir cevap ama kaynak yok [9].")
        self.assertEqual(result["reason"], "no_answer")

    def test_no_search_results(self):
        result = answer("Soru?", lambda q: [], lambda prompt: self.fail("model must not be called"))
        self.assertEqual(result["reason"], "no_answer")

    def test_compliance_question_is_declined_before_search(self):
        result = answer("Bizim bakanlığın hazırladığı yol haritası bu kurallara uygun mu?",
                        lambda q: self.fail("search must not be called"), lambda p: self.fail("no model"))
        self.assertEqual((result["status"], result["reason"]), ("decline", "compliance"))


class RuleTests(unittest.TestCase):
    def test_compliance_detection(self):
        self.assertTrue(asks_for_compliance("Hastane randevu sistemimizde kullandığımız yapay zekâ yüksek etkili sayılır mı?"))
        self.assertTrue(asks_for_compliance("Kurumumuzun veri politikası KVKK'ya uygun mu?"))
        self.assertFalse(asks_for_compliance("Kamu kurumları yol haritasını ne kadar sürede hazırlamalı?"))
        self.assertFalse(asks_for_compliance("Ülkemizde yapay zekâ eylem planının hedefleri nelerdir?"))

    def test_renumber(self):
        self.assertEqual(renumber("A [2]. B [1, 2]. C [2][2].", 3), ("A [1]. B [2][1]. C [1].", [2, 1]))
        self.assertEqual(renumber("A [7].", 3), ("A .", []))

    def test_dates_and_catalog(self):
        self.assertEqual(turkish_date("2026-03"), "Mart 2026")
        self.assertEqual(turkish_date("2023-11-01 (Official Gazette)"), "01.11.2023 (Resmî Gazete)")
        self.assertEqual(turkish_date("2026-05 (PDF creation date; no date printed in the document)"), "Mayıs 2026")
        self.assertEqual(collection_date(), "14 Ekim 2026")
        self.assertEqual(document_facts("Bilinmeyen belge")["legal_status"], "Belirtilmemiş")


if __name__ == "__main__":
    unittest.main()
