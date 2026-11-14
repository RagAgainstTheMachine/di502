"""Prepare the reviewed KVKK guide using explicit, source-specific policies.

Run: python -m src.ingestion.profiles.kvkk_guide --input data/markdown/doc06_kvkk_rehberi_yapay_zeka.md
The reviewed Markdown remains unchanged. Generic chunking code is reused.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import yaml

from src.shared.common import OUTPUT, ROOT, sha256, valid_document_id, write_jsonl
from src.ingestion.markdown_source import PAGE_MARKER, prepare_markdown, read_markdown

DOCUMENT_ID = 'doc06-kvkk-yapay-zeka-rehberi'
INLINE_NOTES = ('2', '6', '17')
GLOSSARY = 'Yapay Zekâya İlişkin Bazı Kavramlar ve Tanımlar'
EXCLUDED_SECTIONS = ('İçindekiler', 'Rehberin Hazırlanmasında Faydalanılan Kaynaklar')


def retrieval_input(source: Path, directory: Path) -> tuple[Path, dict]:
    body, metadata = read_markdown(source.read_text(encoding='utf-8'))
    definitions = {m.group(1): m.group(2) for m in re.finditer(r'^\[\^(\d+)\]: (.+)$',body,re.M)}
    if set(definitions) != {str(n) for n in range(1,34)}:
        raise ValueError('Bu profil PDF ile incelenmiş, 33 dipnotlu Doc06 girdisini bekliyor.')
    # These three notes qualify the substantive content, rather than citing a
    # publication: deep-fake terminology, scope, and lifecycle variability.
    for id_ in INLINE_NOTES:
        marker = f'[^{id_}]'
        refs = list(re.finditer(re.escape(marker)+r'(?!:)',body))
        if len(refs) != 1:
            raise ValueError(f'{id_}. açıklama dipnotu tam bir kez kullanılmalı.')
        end = body.find('\n\n',refs[0].end())
        if end < 0:
            raise ValueError('Açıklama dipnotunun paragraf sonu bulunamadı.')
        body = body[:end]+' '+definitions[id_]+body[end:]
    body, exclusions, footnote_report = prepare_markdown(body,exclude_footnotes=True)
    for item in exclusions:
        item['reason'] = 'definition_stored_separately'
        item['explanatory_text_retained_inline'] = item['footnote_id'] in INLINE_NOTES
    # Explicitly remove cover/contact text by reviewed page provenance. Keep the
    # page comments so that the next heading retains its actual source page.
    markers = list(PAGE_MARKER.finditer(body))
    edits = []
    for i,m in enumerate(markers):
        if int(m.group(1)) in (1,64):
            end = markers[i+1].start() if i+1<len(markers) else len(body)
            removed = body[m.end():end]
            exclusions.append({'page':int(m.group(1)),'reason':'cover_or_contact_page','text':removed})
            edits.append((m.end(),end,'\n\n'))
    for start,end,replacement in reversed(edits):
        body=body[:start]+replacement+body[end:]
    for title in EXCLUDED_SECTIONS:
        headings=list(re.finditer(r'^(#{1,6}) (.+)$',body,re.M))
        matches=[(i,h) for i,h in enumerate(headings) if h.group(2).strip()==title]
        if len(matches)!=1:
            raise ValueError(f'Beklenen bölüm tam bir kez bulunmalı: {title}')
        i,h=matches[0];level=len(h.group(1));end=len(body)
        for following in headings[i+1:]:
            if len(following.group(1))<=level:
                end=following.start();break
        removed=body[h.start():end]
        exclusions.append({'section':title,'reason':'toc_or_bibliography','text':removed})
        comments='\n\n'.join(m.group() for m in PAGE_MARKER.finditer(removed))
        body=body[:h.start()]+comments+'\n\n'+body[end:]
    # Turn each source term/definition pair into its own structural unit.
    start=re.search(r'^## '+re.escape(GLOSSARY)+r'\s*$',body,re.M)
    if start is None:
        raise ValueError('Tanımlar bölümü bulunamadı.')
    following=re.search(r'^## ',body[start.end():],re.M)
    end=start.end()+following.start() if following else len(body)
    section=body[start.end():end]
    terms=[]
    def term_heading(match):
        term=match.group(1)
        terms.append(term)
        return f'### {term}\n\n'+match.group()
    section=re.sub(r'^\*\*(.+?):\*\*[^\n]*$',term_heading,section,flags=re.M)
    if len(terms)!=35:
        raise ValueError(f'35 kaynak tanımı bekleniyordu; bulunan: {len(terms)}')
    body=body[:start.end()]+section+body[end:]
    # Keep the risk infographic's introduction, four labels and conclusion
    # together as one paragraph, instead of leaving a final label-only chunk.
    risk_list='\n\n- Yanlış\n- Tutarsız\n- Ön Yargılı\n- Yanıltıcı/Manipülatif\n\nolabileceği unutulmamalıdır.'
    if body.count(risk_list)!=1:
        raise ValueError('Dört risk etiketinden oluşan kaynak listesi bulunamadı.')
    body=body.replace(risk_list,' Yanlış; Tutarsız; Ön Yargılı; Yanıltıcı/Manipülatif olabileceği unutulmamalıdır.',1)
    # Docling's list item text omits its marker. Preserve source step numbers as
    # ordinary bold text so extraction retains them with the following text.
    body,numbered_steps=re.subn(r'^(\d+)\. (.+)$',r'**\1.** \2',body,flags=re.M)
    report={
        'policy_version':1,'reviewed_markdown_sha256':sha256(source),
        'reviewed_markdown_file':source.name,'inline_explanatory_footnotes':list(INLINE_NOTES),
        'footnote_definitions_archived':33,'citation_only_footnotes_excluded':30,
        'excluded_sections':list(EXCLUDED_SECTIONS),'excluded_pages':[1,64],
        'glossary_terms':terms,'footnote_processing':footnote_report,
        'numbered_questions_in_section_metadata':15,
        'source_ordered_step_markers_preserved':numbered_steps,
        'risk_infographic_retained_as_one_paragraph':True,
    }
    metadata['retrieval_preprocessing']=report
    directory.mkdir(parents=True,exist_ok=True)
    dest=directory/'retrieval_input.md'
    dest.write_text('---\n'+yaml.safe_dump(metadata,allow_unicode=True,sort_keys=False,width=120).strip()+'\n---\n\n'+body,encoding='utf-8')
    write_jsonl(directory/'source_exclusions.jsonl',exclusions)
    (directory/'guide_preprocessing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return dest,report


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True,type=Path)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    parser.add_argument('--document-id',default=DOCUMENT_ID)
    args=parser.parse_args()
    id_=valid_document_id(args.document_id)
    directory=args.output/id_
    source,_=retrieval_input(args.input,directory)
    from src.ingestion.prepare import prepare_document
    manifest=prepare_document(source,output_root=args.output,document_id=id_,merge_peers=True,compact_payload=True)
    manifest['files'].update({name:sha256(directory/name) for name in
                              ('retrieval_input.md','guide_preprocessing.json','source_exclusions.jsonl')})
    (directory/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    main()
