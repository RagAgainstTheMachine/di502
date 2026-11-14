# Alpha application: what was added and why

| Jira | Author | Date | Related |
|---|---|---|---|
| DI502-72 | Utku Uçar | 14/11/2026 | D5 alpha, D8 beta, C-07; [deploy guide](../deploy/app-deploy-guide.md); [pipeline guide](../pipeline/README.md); ADR 0001 |

This page explains the answer layer, the web page and the deploy files added on top of the hybrid search (PRs #39 and #40). Commands are in the [deploy guide](../deploy/app-deploy-guide.md).

## 1. Starting point

On 14/11/2026 the repository had document preparation (`src/ingestion/`) and hybrid search (`src/retrieval/`). The README and ADR 0001 listed three missing parts:

1. Answer generation: `config/rag.yaml` had `llm: null`.
2. An API the page can call.
3. A working web page: UI mockup v1 existed only as a picture.

D5 needs a local web page and D8 needs Google Cloud. The new code calls `search()` from `src/retrieval/search.py` and changes no ingestion or retrieval code.

## 2. Path of one question

```
Page sends the question to /api/ask                            src/app/server.py
→ asks whether an institution complies?                        src/app/answer.py
     yes → fixed decline; no search, no model call
→ hybrid search returns the top 5 passages                     src/retrieval/search.py
     none → "not in the documents" decline
→ passages go into the prompt with document,
  location and legal status                                    prompts/answer_v1.txt
→ qwen3:8b writes the answer                                   src/app/llm.py
     CEVAP_YOK or no valid citation → "not in the documents" decline
→ citations renumbered 1..m; one card per cited source:
  document, location, legal status, date, official link, quote src/app/answer.py, catalog.py
→ page shows the answer and the cards                          src/app/static/index.html
```

## 3. Files

### Application (`src/app/`)

| File | What it does | Why |
|---|---|---|
| `server.py` | Serves the page and `/api/ask`, `/api/config`, `/healthz`. | Standard library only, so `requirements.txt` is unchanged. Question text is not logged and no chat is stored (C-08, C-11). |
| `answer.py` | The whole path in section 2. | Search and the model are passed in as functions, so tests run without Qdrant or a GPU. |
| `llm.py` | Calls the Ollama API. On Cloud Run it adds a Google identity token. | The model service is private; only the web service may call it. The same code runs on a laptop and on Cloud Run; only `LLM_URL` changes. |
| `catalog.py` | Source-card facts: legal status from `config/documents.yaml`; official URL, version date and collection date from `data/manifest.csv`. | The Qdrant payloads have no legal status, date or URL. URL and dates already live in the manifest, so they are not written a second time. |
| `static/index.html` | UI mockup v1, working. | Same look as the mockup. Changes: fluid width with one column on phones; mockup markers and legend removed; 5 questions per chat and "Yeni sohbet" work; the chat lives in the browser tab only. Answers are inserted as text, never as HTML. |

### Configuration and prompt

| File | Change | Why |
|---|---|---|
| `config/rag.yaml` | `models.llm`: `qwen3:8b`, thinking off, temperature 0, 8,192-token context, 500-token answers, 280 s timeout. `prompt_variant: answer_v1`. `app`: 5 questions per chat, 450-character quotes. | All parameters in one file (README rule). With thinking on, answers take several times longer and the reasoning text can break citation parsing. |
| `config/documents.yaml` | New. Document name in the payload → Doc number, short title, legal status. | Legal-status labels on source cards, using the labels of `docs/eval/eval-set-v1.csv`. |
| `prompts/answer_v1.txt` | New. Six rules: sources only; at most 5 sentences; a source number after each sentence; say that a report states a recommendation, not a rule in force (O4); no yes/no on an institution's compliance; CEVAP_YOK when the sources do not answer. | One template per file (`prompts/` rule). |

### Tests (`tests/app/test_answer.py`)

9 tests with a fake search and a fake model: citation renumbering and source cards; legal status in the prompt; the three "not in the documents" paths (CEVAP_YOK, invalid citation, no results); compliance decline before search; date formats and the collection date (14 Ekim 2026).

### Deploy files

| File | Purpose |
|---|---|
| `Dockerfile` (root) | Web service image: Python 3.12, `requirements.txt`, `src/`, `config/`, `prompts/`, `data/manifest.csv`. No GPU. |
| `.gcloudignore` (root) | Not uploaded: `.env` (the Qdrant key), docs, tests, document copies. |
| `deploy/llm/Dockerfile` | Model service image: Ollama with `qwen3:8b` pulled at build time. |
| `docs/deploy/app-deploy-guide.md` | Local run, Cloud Run deploy, API fields. |

## 4. Cloud Run layout

| Service | Contents | Hardware | Access | Cost |
|---|---|---|---|---|
| `di502-web` | Page, API, answer code | 1 vCPU, 1 GiB | Private for now (proxy); public for the beta by 02/12/2026 | $0 while idle |
| `di502-llm` | Ollama + `qwen3:8b` | 1 NVIDIA L4, 4 vCPU, 16 GiB | Always private; only `di502-web` may call it | about $1.05 per hour while running; deleted after each session |

The Qdrant key is the Secret Manager secret `qdrant-api-key`. Two services keep the GPU off while people only open the page, and keep the model private when the page becomes public.

## 5. Known limits (14/11/2026)

| Limit | Effect |
|---|---|
| Doc04 is not in `ai_plan_text_only` (team decision) | No answer can cite the binding law |
| The compliance decline is a keyword rule: a first-person owner ("bizim", "kurumumuz", "-imiz") plus a judgement ("uygun mu", "sayılır mı") | Other out-of-scope questions rely on the model writing CEVAP_YOK |
| No highlight in the quote | The card shows the first 450 characters of the passage |
| PDF page only | The payloads have no printed page number |
| No personal-data masking | Not needed while question text is never logged; review before the beta (Dependencies 13) |
| Accuracy not measured | Needs the baseline run on evaluation set v1 (D5 Definition of Done) |
