# Web application: run locally and deploy to Cloud Run

| Owner | Written | Related |
|---|---|---|
| Utku Uçar | 14/11/2026 | D5 alpha (local web page), D8 beta (Google Cloud), C-07; [Google Cloud setup](gcp-setup.md); [pipeline guide](../pipeline/README.md) |

The application adds answer generation and a web page on top of the hybrid search in `src/retrieval/`. The page follows UI mockup v1.

## How it works

| Part | Code | Runs where |
|---|---|---|
| Page and JSON API | `src/app/server.py`, `src/app/static/index.html` | Laptop or Cloud Run service `di502-web` (no GPU) |
| Answer: compliance check → search → prompt → model → citations or decline | `src/app/answer.py`, `prompts/answer_v1.txt` | Same as above |
| Source cards: legal status, date, official link | `src/app/catalog.py`, `config/documents.yaml`, `data/manifest.csv` | Same as above |
| Search (E5 + BM25 + RRF) and embeddings | `src/retrieval/search.py` | Qdrant Cloud |
| Language model `qwen3:8b` (thinking off) | `deploy/llm/Dockerfile`, settings in `config/rag.yaml` | Laptop (Ollama) or private Cloud Run service `di502-llm` (L4 GPU) |

The server does not log question text and stores no chats; a chat lives in the browser tab only.

### API

`POST /api/ask` with `{"question": "..."}` returns:

| Field | Value |
|---|---|
| `status` | `answer` or `decline` |
| `reason` | `null`, `compliance` (asks whether an institution complies) or `no_answer` (not in the documents) |
| `title`, `notice` | Decline heading and the fixed notice (US-10, US-12, C-06) |
| `answer` | Answer text with `[n]` citations, numbered 1..m in order of use |
| `sources[]` | `n`, `document`, `doc_id`, `location` (action, paragraph, section, PDF page), `legal_status`, `legal_category`, `date`, `url`, `domain`, `quote` |
| `timing` | `search_ms`, `llm_ms`, `total_ms` |

`GET /api/config` returns the collection date (from `data/manifest.csv`), questions per chat and the model name.

## Run locally (alpha)

1. `.env` in the repository root with `QDRANT_URL` and `QDRANT_API_KEY` (see `.env.example`).
2. A language model, either:
   - Ollama on the laptop: `ollama pull qwen3:8b` (slow without a GPU), or
   - the Cloud Run model service: `gcloud run services proxy di502-llm --region europe-west1 --port 9090` in a separate window, then `set LLM_URL=http://localhost:9090`.
3. Start the server and open http://localhost:8080:
   ```cmd
   pip install -r requirements.txt
   python -m src.app.server
   ```

Checks without Qdrant or a model: `python -m unittest discover -s tests/app -t . -v`.

## Deploy to Cloud Run

All commands run in Windows CMD from the repository root unless marked Cloud Shell. Replace `<PROJECT_ID>` with `rag-against-the-machine` (team) or `utku-llm-deneme` (trial).

### 1. Qdrant key in Secret Manager (once per project, Cloud Shell)

```bash
gcloud config set project <PROJECT_ID>
gcloud services enable secretmanager.googleapis.com
printf '%s' "$QDRANT_API_KEY" | gcloud secrets create qdrant-api-key --data-file=-
PROJECT_NUMBER=$(gcloud projects describe <PROJECT_ID> --format='value(projectNumber)')
gcloud secrets add-iam-policy-binding qdrant-api-key \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

### 2. Language model service (private, GPU)

```cmd
cd deploy\llm
gcloud run deploy di502-llm --source . --region europe-west1 --gpu 1 --gpu-type nvidia-l4 --no-gpu-zonal-redundancy --cpu 4 --memory 16Gi --no-cpu-throttling --max-instances 1 --concurrency 4 --timeout 600 --no-allow-unauthenticated
gcloud run services describe di502-llm --region europe-west1 --format="value(status.url)"
cd ..\..
```

Note the URL printed by the last command (`https://di502-llm-...run.app`).

### 3. Let the web service call the model service

```cmd
gcloud projects describe <PROJECT_ID> --format="value(projectNumber)"
gcloud run services add-iam-policy-binding di502-llm --region europe-west1 --member=serviceAccount:<PROJECT_NUMBER>-compute@developer.gserviceaccount.com --role=roles/run.invoker
```

### 4. Web service (no GPU)

From the repository root (the root `Dockerfile` and `.gcloudignore` are used; `.env` is not uploaded):

```cmd
gcloud run deploy di502-web --source . --region europe-west1 --cpu 1 --memory 1Gi --max-instances 2 --concurrency 10 --timeout 300 --no-allow-unauthenticated --set-env-vars LLM_URL=<LLM_URL>,QDRANT_URL=<QDRANT_URL> --set-secrets QDRANT_API_KEY=qdrant-api-key:latest
```

### 5. Open the page

```cmd
gcloud run services proxy di502-web --region europe-west1 --port 8080
```

Open http://localhost:8080. The first answer after a pause takes 1–2 minutes while the model service starts.

### 6. After each session

The model service costs about $1.05 per hour while an instance runs. Delete it after each session; the web service scales to zero and can stay.

```cmd
gcloud run services delete di502-llm --region europe-west1
```

To redeploy it later without rebuilding, use the image listed by `gcloud artifacts docker images list europe-west1-docker.pkg.dev/<PROJECT_ID>/cloud-run-source-deploy` with `--image` instead of `--source .`, then repeat step 3.

## Before the public beta (02/12/2026)

- Web service public with `--allow-unauthenticated`; the model service stays private.
- Personal-data masking before any logging (Dependencies 13).
- A read-only Qdrant key with an expiry date for the web service.

## Known limits (14/11/2026)

- Doc04 (Law No. 6698) is not in the `ai_plan_text_only` collection, so binding-law answers (O4) cannot cite it yet.
- The compliance check is a keyword rule (`src/app/answer.py`); other out-of-scope questions rely on the model writing CEVAP_YOK.
- No highlight inside the quoted passage.
