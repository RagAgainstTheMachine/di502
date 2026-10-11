# DI 502 Team Project

<!-- One-line description of the system. -->

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

<!-- How to start the system, e.g. `python -m src.app`. -->

## Repository structure

| Path | Contents |
| --- | --- |
| `ai-bom.yaml` | AI Bill of Materials (from Sprint 2) |
| `requirements.txt` | Pinned dependencies (exact versions) |
| `config/rag.yaml` | All parameters: chunking, models, top-k, prompt variant |
| `prompts/` | Prompt templates, one file per template |
| `data/manifest.csv` | Source URL, licence, version date and hash of each document |
| `src/` | Code |
| `docs/Markdown Template/` | Project documentation template (synced to Confluence) |
| `docs/design.md` | One-page design overview |
| `docs/adr/` | Architecture Decision Records, one file per decision |
| `docs/spikes/` | Learning and hypothesis notes |
| `docs/eval/` | Evaluation set and results |
| `docs/sprints/` | One-page report per sprint |
| `excess_folders/` | Course material from the template repo (reference only) |
