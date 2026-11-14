"""Prepare separate, validated bundles from PDF or Markdown documents."""
from __future__ import annotations

import argparse
import importlib.metadata
import json
import logging
import os
import shutil
from pathlib import Path

from src.shared.common import (CONFIG, DIMENSIONS, MODEL, MODEL_CONTEXT, OUTPUT, ROOT, TOKEN_LIMIT,
                    default_document_id, sha256, valid_document_id, write_jsonl)
from src.shared.payload import write_payload_preview


def load_tokenizer():
    os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "huggingface"))
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer
    options = {"cache_dir": Path(os.environ["HF_HOME"]) / "hub"}
    try:
        path = snapshot_download(MODEL, local_files_only=True, **options)
    except OSError:
        path = snapshot_download(MODEL, allow_patterns=["tokenizer*", "special_tokens_map.json", "sentencepiece.bpe.model", "config.json"], **options)
    return AutoTokenizer.from_pretrained(path, local_files_only=True)


def convert_document(source: Path, output: Path, force=False, ocr=False, markdown_options=None):
    os.environ.setdefault("HF_HOME", str(ROOT / ".cache" / "huggingface"))
    from docling_core.types.doc import DoclingDocument
    from src.ingestion.markdown_source import PREPROCESS_VERSION
    fingerprint = sha256(source)
    preprocessing = PREPROCESS_VERSION if source.suffix.lower() != ".pdf" else 0
    markdown_options = markdown_options or {}
    output.mkdir(parents=True, exist_ok=True)
    for candidate in (output, output.parent):
        cached, info_path = candidate / "docling.json", candidate / "conversion.json"
        if not force and cached.is_file() and info_path.is_file():
            info = json.loads(info_path.read_text(encoding="utf-8"))
            if info.get("source_sha256") == fingerprint and info.get("ocr", False) == ocr and info.get("preprocess_version", 0) == preprocessing and info.get("markdown_options", {}) == markdown_options:
                document = DoclingDocument.load_from_json(cached)
                if candidate != output:
                    for name in ("docling.json", "conversion.json", "document.md", "chunking_source.md", "cleaned.md", "markdown_preprocessing.json", "excluded_footnotes.jsonl"):
                        if (candidate / name).is_file():
                            shutil.copyfile(candidate / name, output / name)
                print(f"Docling önbelleği: {source.name}", flush=True)
                return document, fingerprint
    from docling.datamodel.base_models import ConversionStatus, InputFormat
    from docling.document_converter import DocumentConverter, PdfFormatOption
    if source.suffix.lower() == ".pdf":
        from docling.datamodel.accelerator_options import AcceleratorDevice, AcceleratorOptions
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        options = PdfPipelineOptions(do_ocr=ocr, do_table_structure=True)
        options.accelerator_options = AcceleratorOptions(num_threads=4, device=AcceleratorDevice.CPU)
        converter = DocumentConverter(format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=options)})
    else:
        from src.ingestion.markdown_source import read_markdown, conversion_input, prepare_markdown
        body, _ = read_markdown(source.read_text(encoding="utf-8"))
        body, excluded, preprocessing_report = prepare_markdown(body, **markdown_options)
        (output / "chunking_source.md").write_text(body, encoding="utf-8")
        write_jsonl(output / "excluded_footnotes.jsonl", excluded)
        (output / "markdown_preprocessing.json").write_text(json.dumps(preprocessing_report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        body, joins = conversion_input(body)
        cleaned = output / "cleaned.md"
        cleaned.write_text(body, encoding="utf-8")
        converter = DocumentConverter(allowed_formats=[InputFormat.MD])
    print(f"Docling dönüşümü: {source.name}", flush=True)
    result = converter.convert(source if source.suffix.lower() == ".pdf" else cleaned)
    if result.status != ConversionStatus.SUCCESS:
        raise ValueError(f"Docling dönüşümü tamamlanamadı: {result.status}; {result.errors}")
    result.document.save_as_json(output / "docling.json")
    result.document.save_as_markdown(output / "document.md")
    (output / "conversion.json").write_text(json.dumps({"source_sha256": fingerprint, "source_file": source.name, "ocr": ocr, "preprocess_version": preprocessing, "markdown_options": markdown_options}, indent=2) + "\n", encoding="utf-8")
    return result.document, fingerprint


def prepare_document(source: Path, output_root=OUTPUT, document_id=None, title=None,
                     profile="generic", max_tokens=TOKEN_LIMIT, force_parse=False,
                     ocr=False, merge_peers=None, convert_only=False, compact_payload=False,
                     markdown_options=None):
    from src.ingestion.chunking import chunk_parents, extract_blocks, segment_generic, validate
    source = source.resolve()
    if not source.is_file() or source.suffix.lower() not in {".pdf", ".md", ".markdown"}:
        raise ValueError(f"PDF/Markdown dosyası bulunamadı: {source}")
    if not 96 <= max_tokens <= MODEL_CONTEXT:
        raise ValueError("--max-tokens 96-512 arasında olmalı.")
    explicit_id = document_id is not None
    document_id = valid_document_id(document_id or default_document_id(source))
    output = Path(output_root) / document_id
    if (output / "manifest.json").is_file() and not explicit_id:
        old = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
        if old.get("source_path") not in (None, str(source)) and old.get("source_sha256") != sha256(source):
            raise ValueError("Aynı dosya adında farklı kaynak var; ayrı --document-id verin.")
    if profile == "ai-plan":
        if source.suffix.lower() != ".pdf":
            raise ValueError("ai-plan profili PDF yerleşimine bağlıdır; Markdown için generic kullanın.")
        from src.ingestion.profiles.ai_plan import TITLE
        title = title or TITLE
    elif profile != "generic":
        raise ValueError("Bilinmeyen profil.")
    markdown_body, source_metadata = None, {}
    if source.suffix.lower() in {".md", ".markdown"}:
        from src.ingestion.markdown_source import read_markdown
        markdown_body, source_metadata = read_markdown(source.read_text(encoding="utf-8"))
    title = title or str(source_metadata.get("title") or source.stem.replace("_", " "))
    if markdown_options and markdown_body is None:
        raise ValueError("Markdown ön işleme seçenekleri yalnızca Markdown kaynağıyla kullanılabilir.")
    document, fingerprint = convert_document(source, output, force_parse, ocr, markdown_options)
    if convert_only:
        return {"document_id": document_id, "output": str(output), "conversion_only": True}
    blocks = extract_blocks(document)
    annotated = 0
    if markdown_body is not None:
        from src.ingestion.markdown_source import annotate_pages
        from src.ingestion.markdown_source import prepare_markdown
        markdown_body, _, preprocessing_report = prepare_markdown(markdown_body, **(markdown_options or {}))
        annotated = annotate_pages(blocks, markdown_body)
    if profile == "ai-plan":
        from src.ingestion.profiles.ai_plan import build_parents
        parents = build_parents(document, blocks, document_id)
    else:
        parents = segment_generic(blocks, document_id, title)
    merge = CONFIG["chunking"]["ai_plan_merge_peers" if profile == "ai-plan" else "generic_merge_peers"] if merge_peers is None else merge_peers
    tokenizer = load_tokenizer()
    chunks, summaries = chunk_parents(parents, tokenizer, max_tokens, title=title,
                                     merge_peers=merge, attach_numbers=profile == "generic",
                                     bound_headings=profile != "ai-plan")
    for record in chunks + summaries:
        record.update(document_name=title, source_file=source.name, source_sha256=fingerprint)
    from src.ingestion.retrieval_filter import filter_chunks, POLICY_VERSION
    chunks, summaries, excluded, excluded_parents = filter_chunks(chunks, summaries, blocks)
    if compact_payload:
        parent_sizes = {p["parent_id"]: p["chunk_count"] for p in summaries}
        for chunk in chunks:
            chunk["compact_payload"] = True
            if parent_sizes[chunk["parent_id"]] > 1:
                chunk["parent_chunk_count"] = parent_sizes[chunk["parent_id"]]
    validation = validate(chunks, summaries, tokenizer, max_tokens)
    validation["retrieval_exclusions"] = len(excluded)
    if profile == "generic":
        validation["headings_used_as_context"] = sum(b["label"] in {"section_header", "title"} for b in blocks)
        # Heading text remains in section paths; every non-heading source block
        # must survive segmentation, including short answers, dates, and numbers.
        body = [b for b in blocks if b["label"] not in {"section_header", "title"}]
        segmented = [b for p in parents for b in p["blocks"]]
        validation["body_blocks_preserved"] = body == [{k: v for k, v in b.items() if k != "section"} for b in segmented]
        if not validation["body_blocks_preserved"]:
            validation["errors"].append("Gövde blokları bölümleme sırasında değişti.")
    validation["pages_without_extracted_blocks"] = sorted(set(document.pages) - {b["page"] for b in blocks if b["page"] is not None})
    if validation["errors"]:
        raise ValueError("Doğrulama başarısız: " + "; ".join(validation["errors"]))
    write_jsonl(output / "blocks.jsonl", blocks)
    write_jsonl(output / "parents.jsonl", summaries)
    write_jsonl(output / "chunks.jsonl", chunks)
    write_jsonl(output / "excluded_chunks.jsonl", excluded)
    write_jsonl(output / "excluded_parents.jsonl", excluded_parents)
    payload_preview = write_payload_preview(output, chunks)
    manifest = {
        "format_version": 2, "document_id": document_id, "title": title, "profile": profile,
        "source_format": source.suffix.lower().lstrip("."), "source_path": str(source),
        "source_metadata": source_metadata, "blocks_with_page_annotations": annotated,
        "source_file": source.name, "source_sha256": fingerprint, "page_count": len(document.pages),
        "model": MODEL, "dimensions": DIMENSIONS, "max_tokens": max_tokens, "merge_peers": merge,
        "embedding_context": "text_only",
        "compact_payload": compact_payload,
        "payload_fields": sorted({field for item in payload_preview for field in item["payload"]}),
        "retrieval_review": {"policy_version": POLICY_VERSION, "excluded_total": len(excluded)},
        "chunk_count": len(chunks), "parent_count": len(summaries), "validation": validation,
        "files": {name: sha256(output / name) for name in ("chunks.jsonl", "parents.jsonl", "excluded_chunks.jsonl", "excluded_parents.jsonl")},
        "packages": {name: importlib.metadata.version(name) for name in ("docling", "docling-core", "transformers", "qdrant-client")},
    }
    if markdown_body is not None:
        manifest["markdown_options"] = markdown_options or {}
        manifest["markdown_preprocessing"] = preprocessing_report
        manifest["files"].update({name: sha256(output / name) for name in ("chunking_source.md", "excluded_footnotes.jsonl", "markdown_preprocessing.json")})
    source_pages = len(document.pages) if source.suffix.lower() == ".pdf" else source_metadata.get("source_pdf_pages")
    if type(source_pages) is int and source_pages > 0:
        manifest["source_pdf_page_count"] = source_pages
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    page_description = f"Kaynak PDF sayfası: {source_pages}" if source_pages else "Kaynak: Markdown"
    lines = [title, f"Belge: {document_id} | Profil: {profile} | Kaynak: {manifest['source_format']}",
             f"Chunk: {len(chunks)} | Parent: {len(summaries)} | {page_description}",
             f"Token sınırı: {max_tokens}; gözlenen: {validation['max_observed_tokens']}",
             "Hatalar: 0; parent metinleri child'lardan eksiksiz yeniden oluşturuldu.",
             f"Kaynak sayfa işaretiyle eşleşen Markdown bloğu: {annotated}; işaretsiz kaynakta bölüm başlığı kullanılır."]
    (output / "validation.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    review = [f"# {title}", f"Belge: `{document_id}` | Profil: `{profile}`", ""]
    for chunk in chunks:
        location = f"PDF {chunk['page_start']}-{chunk['page_end']}" if chunk["pages"] else "Markdown bölümü"
        paragraph = f" | Paragraf {chunk['paragraph_id']}" if chunk.get("paragraph_id") else ""
        review += [f"## {chunk['section']} / {chunk['chunk_index']}",
                   f"{location}{paragraph} | {chunk['token_count']} token | `{chunk['parent_id']}`", "", chunk["text"], ""]
    (output / "chunks_review.md").write_text("\n".join(review), encoding="utf-8")
    print("\n".join(lines[:5]) + f"\nÇıktı: {output}", flush=True)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", "--pdf", dest="inputs", type=Path, nargs="+", required=True)
    parser.add_argument("--document-id", help="Kalıcı belge kimliği; tek dosya ile kullanılabilir.")
    parser.add_argument("--title")
    parser.add_argument("--profile", choices=("generic", "ai-plan"), default="generic")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--max-tokens", type=int, default=TOKEN_LIMIT)
    parser.add_argument("--merge-peers", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--force-parse", action="store_true")
    parser.add_argument("--convert-only", action="store_true")
    parser.add_argument("--compact-payload", action="store_true", help="Tek chunk'lık bölümlerde gereksiz gruplama/tür alanlarını payload'a koyma.")
    parser.add_argument("--ocr", action="store_true")
    parser.add_argument("--exclude-footnotes", action="store_true", help="Dipnot tanımlarını ve referanslarını retrieval dışında ayrı sakla.")
    parser.add_argument("--numbered-unit-section", help="Numaralı liste öğelerinin bağımsız birim yapılacağı Markdown bölümünün tam başlığı.")
    parser.add_argument("--numbered-unit-label", choices=("Paragraf", "Tedbir", "Politika", "Öneri"), default="Paragraf")
    args = parser.parse_args()
    if len(args.inputs) > 1 and (args.document_id or args.title):
        parser.error("--document-id ve --title tek dosya ile kullanılabilir.")
    logging.basicConfig(level=logging.INFO)
    try:
        markdown_options = {}
        if args.exclude_footnotes:
            markdown_options["exclude_footnotes"] = True
        if args.numbered_unit_section:
            markdown_options.update(numbered_unit_section=args.numbered_unit_section, numbered_unit_label=args.numbered_unit_label)
        for source in args.inputs:
            prepare_document(source, args.output, args.document_id, args.title, args.profile,
                             args.max_tokens, args.force_parse, args.ocr, args.merge_peers, args.convert_only, args.compact_payload, markdown_options)
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Hata: {exc}\n")


if __name__ == "__main__":
    main()
