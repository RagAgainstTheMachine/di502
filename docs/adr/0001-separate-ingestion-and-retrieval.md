# Separate document ingestion from request-time retrieval

Status: ingestion implemented; retrieval follows in a separate branch · Date: 2026-11-14

The production code previously ran from a standalone homework folder. This repo
needs reproducible document preparation and an importable retriever for the
future question-answering application.

Document conversion, source cleaning, chunking, validation, upload and index
setup live in `src/ingestion/`. Request-time search will be added in `src/retrieval/` by the dependent retrieval branch.
Common configuration, payload projection and connection/schema helpers live
in `src/shared/`. Retrieval has no dependency on ingestion or Docling. Separate
requirement files keep parsing dependencies out of the retrieval runtime.

The selected baseline is preserved: multilingual-e5-small, 384-dimensional
cosine vectors; text-only embeddings; 300-token chunks; BM25 on `text`; Qdrant
RRF hybrid retrieval by default; parent expansion off. Settings are read from
`config/rag.yaml`, with credentials supplied outside Git. Native BM25 uses the
existing collection; no vector regeneration or Cloud mutation is part of this
repository migration.

Earlier spike documents describe alternatives and proposed experiments. They
are retained as research history; the committed config and pipeline guide state
the current baseline. LLM generation, reranking and the web/API remain separate
future work.
