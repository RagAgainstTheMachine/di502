import re
import tempfile
import unittest
from pathlib import Path

from src.shared.common import load_validated_chunks
from src.ingestion.markdown_source import prepare_markdown
from src.shared.payload import build_payload
from src.ingestion.prepare import prepare_document


class MarkdownUnits(unittest.TestCase):
    def test_scope_and_footnote_provenance_are_preserved(self):
        source = (
            '# Rapor\n\n## Açıklama\n\n1. Bu sıradan bir listedir.\n\n'
            '<!-- page: pdf 10 -->\nBir değerlendirme[^7].\n\n'
            '## Sonuç Tablosu\n\n### Hukuk\n\n'
            '1. Şeffaflık sağlanması. — Vade: Kısa\n\n'
            '<!-- page: pdf 11 -->\n2. Denetim yapılması. — Vade: —\n\n'
            '## Ek\n\n3. Sonuç dışı liste.\n\n## Dipnotlar\n\n'
            '<!-- page: pdf 10 -->\n[^7]: Kaynak makale.\n    İkinci satır.\n')
        text, excluded, report = prepare_markdown(source, exclude_footnotes=True,
            numbered_unit_section='Sonuç Tablosu', numbered_unit_label='Öneri')
        self.assertEqual(report['numbered_units'], ['1','2'])
        self.assertEqual(report['removed_footnote_references'], 1)
        self.assertEqual(excluded[0]['page'], 10)
        self.assertIn('İkinci satır.', excluded[0]['text'])
        self.assertNotIn('Kaynak makale', text)
        self.assertNotIn('Dipnotlar', text)
        self.assertIn('1. Bu sıradan bir listedir.', text)
        self.assertIn('3. Sonuç dışı liste.', text)
        self.assertIn('#### Öneri 2', text)
        self.assertIn('**2.** Denetim yapılması. — Vade: —', text)
        with self.assertRaisesRegex(ValueError, 'Tanımı olmayan'):
            prepare_markdown('Metin[^8].', exclude_footnotes=True)

    def test_recommendations_do_not_mix_and_parent_expansion_keeps_unit_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root/'report.md'
            source.write_text('# Rapor\n\n## Sonuç\n\n### Hukuk\n\n'
                '<!-- page: pdf 20 -->\n'
                '1. '+ 'Açıklanabilir yapay zekâ sistemleri düzenli olarak değerlendirilecektir. '*30 + '— Vade: Orta\n\n'
                '<!-- page: pdf 21 -->\n2. Veri güvenliği sağlanması[^7]. — Vade: —\n\n'
                '## Dipnotlar\n\n<!-- page: pdf 21 -->\n[^7]: Bir kaynak.\n')
            prepare_document(source, root/'output', document_id='report', merge_peers=True,
                compact_payload=True, max_tokens=96, markdown_options={
                    'exclude_footnotes':True, 'numbered_unit_section':'Sonuç',
                    'numbered_unit_label':'Öneri'})
            chunks, manifest = load_validated_chunks(root/'output/report')
            self.assertEqual({c['paragraph_id'] for c in chunks}, {'1','2'})
            self.assertTrue(all(c['section']=='Sonuç / Hukuk' for c in chunks))
            first = [c for c in chunks if c['paragraph_id']=='1']
            second = [c for c in chunks if c['paragraph_id']=='2']
            self.assertGreater(len(first), 1)
            self.assertEqual(len(second), 1)
            self.assertTrue(all(c['pages']==[20] for c in first))
            self.assertEqual(second[0]['pages'],[21])
            self.assertIn('Vade: —',second[0]['text'])
            self.assertNotIn('parent_id',build_payload(second[0]))
            self.assertIn('parent_id',build_payload(first[0]))
            self.assertTrue(all(c['embedding_text']==c['text'] and not re.search(r'\[\^',c['text']) for c in chunks))
            self.assertEqual(manifest['markdown_preprocessing']['excluded_footnotes'],1)


if __name__ == '__main__':
    unittest.main()
