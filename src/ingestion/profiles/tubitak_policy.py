"""Select reviewed TÜBİTAK policy content, then reuse generic HybridChunker.

Run: python -m src.ingestion.profiles.tubitak_policy --input data/markdown/doc07_tubitak_yapay_zeka_politikasi.md
"""
import argparse
import json
import re
from pathlib import Path

import yaml

from src.shared.common import OUTPUT, ROOT, sha256, valid_document_id, write_jsonl
from src.ingestion.markdown_source import PAGE_MARKER, read_markdown

DOCUMENT_ID='doc07-tubitak-yapay-zeka-politikasi'


def retrieval_input(source: Path, directory: Path):
    body,metadata=read_markdown(source.read_text(encoding='utf-8'))
    if metadata.get('source_pdf_pages')!=8 or metadata.get('doc_id')!='Doc07':
        raise ValueError('Bu profil PDF ile karşılaştırılmış sekiz sayfalık Doc07 girdisini bekliyor.')
    markers=list(PAGE_MARKER.finditer(body))
    if [int(m.group(1)) for m in markers]!=list(range(1,9)):
        raise ValueError('Sekiz kaynak sayfa işareti sıralı olarak bulunmalı.')
    reference_text=body[markers[-1].end():]
    if re.findall(r'^\[([1-4])\]',reference_text,re.M)!=list('1234'):
        raise ValueError('Dört kaynak kaydı bulunamadı.')
    exclusions=[];parts=[body[:markers[0].start()]]
    for i,m in enumerate(markers):
        end=markers[i+1].start() if i+1<len(markers) else len(body)
        content=body[m.end():end]
        page=int(m.group(1))
        parts.append(m.group())
        if page in (1,8):
            exclusions.append({'page':page,'reason':'cover' if page==1 else 'bibliography','text':content})
        else:
            parts.append(content)
    body='\n\n'.join(parts)
    # These are bibliography callouts, not numbered policy clauses. The original
    # callouts and all four reference records remain in the reviewed source.
    body,removed=re.subn(r'[ \t]*\[[1-4]\]','',body)
    report={
        'policy_version':1,'reviewed_markdown_file':source.name,
        'reviewed_markdown_sha256':sha256(source),'excluded_pdf_pages':[1,8],
        'retained_pdf_pages':list(range(2,8)),
        'citation_callouts_removed':removed,'bibliography_records_archived':4,
        'numbered_policy_sections_retained_in_section_metadata':True,
    }
    metadata['retrieval_preprocessing']=report
    directory.mkdir(parents=True,exist_ok=True)
    target=directory/'retrieval_input.md'
    target.write_text('---\n'+yaml.safe_dump(metadata,allow_unicode=True,sort_keys=False,width=120).strip()+'\n---\n\n'+body,encoding='utf-8')
    write_jsonl(directory/'source_exclusions.jsonl',exclusions)
    (directory/'guide_preprocessing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return target,report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    parser.add_argument('--document-id',default=DOCUMENT_ID)
    args=parser.parse_args()
    id_=valid_document_id(args.document_id);directory=args.output/id_
    source,_=retrieval_input(args.input,directory)
    from src.ingestion.prepare import prepare_document
    manifest=prepare_document(source,output_root=args.output,document_id=id_,merge_peers=True,compact_payload=True)
    manifest['files'].update({name:sha256(directory/name) for name in
                             ('retrieval_input.md','guide_preprocessing.json','source_exclusions.jsonl')})
    (directory/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
