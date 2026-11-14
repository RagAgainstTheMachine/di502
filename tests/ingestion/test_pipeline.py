from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import uuid
import warnings

from qdrant_client import QdrantClient, models

from src.shared.common import ROOT, DIMENSIONS, MODEL, load_validated_chunks
from src.shared.payload import build_payload
from src.ingestion.retrieval_filter import filter_chunks
from src.ingestion.index import ensure_collection, index_document, embedding_document, document_filter


BUNDLE=ROOT/'data/processed/turkiye_ai_eylem_plani_2026_2030'


class SelectedPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chunks,cls.manifest=load_validated_chunks(BUNDLE)
        cls.parents=[json.loads(x) for x in (BUNDLE/'parents.jsonl').read_text().splitlines()]
        cls.blocks=[json.loads(x) for x in (BUNDLE/'blocks.jsonl').read_text().splitlines()]

    def test_selected_output_and_text_only_contract(self):
        self.assertEqual(len(self.chunks),196)
        self.assertEqual(len(self.parents),95)
        self.assertEqual({c['action_id'] for c in self.chunks if c['kind']=='action'},set(range(1,17)))
        terms=[c for c in self.chunks if c['kind']=='glossary']
        self.assertEqual(len(terms),38)
        self.assertTrue(all(c['text'].startswith(c['title']+':') for c in terms))
        for c in self.chunks:
            self.assertEqual(c['embedding_text'],c['text'])
            request=embedding_document(c)
            self.assertEqual(request.text,c['text'])
            self.assertEqual(request.model,MODEL)
            self.assertNotIn('embedding_model',build_payload(c))

    def test_exclusion_replay_and_filter_idempotency(self):
        excluded=[json.loads(x) for x in (BUNDLE/'excluded_chunks.jsonl').read_text().splitlines()]
        removed_parents=[json.loads(x) for x in (BUNDLE/'excluded_parents.jsonl').read_text().splitlines()]
        self.assertEqual(len(excluded),7)
        self.assertEqual(sum(x['reason']=='table_of_contents' for x in excluded),1)
        kept,parents,removed,_=filter_chunks(self.chunks+[e['chunk'] for e in excluded],self.parents+removed_parents,self.blocks)
        self.assertEqual(kept,self.chunks)
        self.assertEqual(parents,self.parents)
        self.assertEqual({e['chunk']['id'] for e in removed},{e['chunk']['id'] for e in excluded})
        kept2,_,removed2,_=filter_chunks(kept,parents,self.blocks)
        self.assertEqual(kept2,kept)
        self.assertFalse(removed2)

    def test_short_facts_are_preserved(self):
        record={'id':'short','kind':'section','section':'Hedef','text':'42','source_refs':['b'],
                'parent_id':'p','chunk_index':0,'pages':[1]}
        parent={'parent_id':'p','text':'42','chunk_count':1}
        kept,_,excluded,_=filter_chunks([record],[parent],[{'source_ref':'b','text':'42','label':'text'}])
        self.assertEqual(kept,[record])
        self.assertFalse(excluded)

    def test_scoped_reindex_preserves_other_document_and_avoids_duplicates(self):
        a=deepcopy([c for c in self.chunks if c.get('action_id')==1])
        b=deepcopy([c for c in self.chunks if c['kind']=='glossary'][:1])
        b[0].update(id=str(uuid.uuid5(uuid.NAMESPACE_URL,'other-document')),
                    document_id='other-document',document_name='Diğer Belge',parent_id='other-document:term_01')
        vector=[1.0]+[0.0]*(DIMENSIONS-1)
        client=QdrantClient(':memory:')
        try:
            with tempfile.TemporaryDirectory() as directory, patch('src.ingestion.index.embedding_document',return_value=vector):
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore',UserWarning)
                    ensure_collection(client,'test')
                root=Path(directory)
                ma={'document_id':a[0]['document_id'],'source_sha256':'fixture'}
                mb={'document_id':'other-document','source_sha256':'fixture'}
                index_document(client,'test',a,ma,root/'a')
                index_document(client,'test',b,mb,root/'b')
                before=client.retrieve('test',[b[0]['id']],with_vectors=True)[0].model_dump()
                index_document(client,'test',a,ma,root/'a')
                self.assertEqual(client.count('test',exact=True).count,len(a)+len(b))
                updated=index_document(client,'test',a[:-1],ma,root/'a')
                self.assertEqual(updated['stale_points_removed'],1)
                after=client.retrieve('test',[b[0]['id']],with_vectors=True)[0].model_dump()
                self.assertEqual(before,after)
                self.assertEqual(client.count('test',count_filter=document_filter('Diğer Belge'),exact=True).count,1)
        finally:
            client.close()


if __name__=='__main__':
    unittest.main()
