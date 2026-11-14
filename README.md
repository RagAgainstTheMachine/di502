# Türkiye AI Policy Assistant

A Turkish question-answering assistant for Türkiye's official AI policy documents. It answers from the documents only, cites the document and article or section, and shows each source's legal status, so users can tell binding rules apart from plans and recommendations.

**Team:** RagAgainstTheMachine · **Course:** DI 502 · **Timeline:** 14/10/2026 – 30/12/2026 (4 sprints)

## How it works

Retrieval-augmented generation (RAG): the official documents are split and indexed. For each question, the most relevant passages are retrieved and a language model writes the answer from them only. Questions outside the documents, or asking whether a specific institution complies, are declined. No personal data is stored.

Details: [Project Executive Summary](docs/Markdown%20Template/03-project-canvas/01-project-executive-summary.md) · [System Architecture Design Document](docs/Markdown%20Template/11-system-architecture-design-document.md)

## Status

Document ingestion and hybrid retrieval are available. Grounded answer generation and the web interface are not implemented yet. The alpha prototype (local web page) is due 14/11/2026.

## Install

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# For document preparation and the full test suite:
pip install -r requirements-ingestion.txt
```

## Run

Copy `.env.example` to `.env` in the repository root and fill in the existing Qdrant connection values. Then:

```bash
python -m src.retrieval.search "Data Sovereignty nedir?" --limit 3
python -m src.ingestion.index --output data/processed --all --dry-run
```

Search defaults to hybrid (E5 + BM25 + RRF), with BM25 on `text` only and parent expansion off. Seven documents and 1183 points are already indexed in `ai_plan_text_only`; no reparse or upload is needed to search them. The web interface is not available yet.

See [pipeline instructions](docs/pipeline/README.md) and the [branch delivery plan](docs/pipeline/branch-plan.md).

## Repository structure

| Path | Contents |
| --- | --- |
| `src/ingestion/` | PDF/MD preparation, chunking, validation and Qdrant upload |
| `src/retrieval/` | Importable hybrid search for the future LLM layer |
| `src/shared/` | Configuration, payload and Qdrant helpers |
| `config/rag.yaml` | All parameters: chunking, models, top-k, prompt variant |
| `prompts/` | Prompt templates, one file per template |
| `data/markdown/`, `data/processed/` | Reviewed sources and ready chunk bundles |
| `data/manifest.csv` | Source URL, licence, download date and hash of each document |
| `requirements.txt` | Pinned dependencies (exact versions) |
| `ai-bom.yaml` | AI Bill of Materials (from Sprint 2) |
| `docs/Markdown Template/` | Project charter and course documents (synced to Confluence) |
| `docs/design.md` | One-page design overview |
| `docs/adr/` | Architecture Decision Records |
| `docs/spikes/` | Learning spike notes |
| `docs/eval/` | Evaluation set and results |
| `docs/sprints/` | One-page report per sprint |
| `excess_folders/` | Course material from the template repo (reference only) |


## Team

| Member | Role |
| --- | --- |
| Muhammed Batuhan Tezcan | Product Owner |
| Deniz Şenkutlu | Scrum Master, Data Engineer |
| Utku Uçar | Data Engineer |
| Elif Yeşim Koçoğlu | Data Scientist |
