# Software Bill of Materials

| Last updated | By | Covers |
|---|---|---|
| 12/11/2026 | Utku Uçar | Everything used in Sprint 2 up to spikes S4 and S5. The baseline (D5) adds its rows when it is built. |

This page lists every library, tool, service and model that the project has used, with its exact version. Pinned Python packages are in `src/spikes/s4/requirements.txt` (spike S4) and, from the baseline on, in the root `requirements.txt`.

## Software Bill of Materials

### Python packages

| Package Name | Version | Description | License | Supplier | Package Checksum | Used in |
|---|---|---|---|---|---|---|
| numpy | 2.5.4 | Arrays; BM25 scores and embedding similarity | BSD-3-Clause | NumPy developers | not recorded | S4 |
| torch | 2.15.0 | Runs the embedding model on CPU | BSD-3-Clause | PyTorch Foundation | not recorded | S4 |
| transformers | 5.22.2 | Loads the embedding model | Apache-2.0 | Hugging Face | not recorded | S4 |
| sentence-transformers | 6.3.0 | Encodes passages and questions | Apache-2.0 | UKP Lab / Hugging Face | not recorded | S4 |
| huggingface_hub | 2.4.0 | Downloads model files from Hugging Face | Apache-2.0 | Hugging Face | not recorded | S4 |
| pdfplumber | 0.11.10 | Extracts the text of Law No. 6698 (Doc04) from its PDF | MIT | Jeremy Singer-Vine | not recorded | `src/extraction/doc04_law_6698.py` |

Checksums are generated with syft from the baseline's `requirements.txt` when the baseline is built.

### Tools and services not in requirements.txt

| Tool or service | Version | What for | License or terms | Supplier | Used by, when | Used in |
|---|---|---|---|---|---|---|
| Python | 3.12.0 | Runs all project code | PSF License | Python Software Foundation | Utku Uçar, 03/11–12/11/2026 | S4, S5 |
| Ollama (container image `ollama/ollama`) | `latest` on 07/11/2026, not pinned | Serves the language models over HTTP | MIT | Ollama | Utku Uçar, 07/11/2026 | S5 (`deploy/trial/Dockerfile`) |
| Google Cloud Run | managed service | Runs the trial answer service; run B with one NVIDIA L4 GPU | Google Cloud terms | Google | Utku Uçar, 07/11/2026 | S5 |
| Google Cloud Build | managed service | Builds the trial container image from source | Google Cloud terms | Google | Utku Uçar, 07/11/2026 | S5 |
| Google Artifact Registry | managed service | Stores the built container images | Google Cloud terms | Google | Utku Uçar, 07/11/2026 | S5 |
| Google Cloud CLI (`gcloud`) | Google Cloud SDK 592.0.0 | Deploys and deletes the services | Apache-2.0 | Google | Utku Uçar, 07/11–10/11/2026 | S5, [Google Cloud setup](../deploy/gcp-setup.md) |

## AI Software Bill of Materials

| Model Name | Purpose | License | Accesser | Date of Access | Method of Interaction | Experiment and Results | Used? Why |
|---|---|---|---|---|---|---|---|
| [intfloat/multilingual-e5-base](https://huggingface.co/intfloat/multilingual-e5-base), revision `d128750597153bb5987e10b1c3493a34e5a4502a`, 278M parameters, full precision, 768-dimension embeddings | Embed passages and questions for search | MIT | Utku Uçar | 12/11/2026 | Run locally on a laptop CPU with sentence-transformers 6.3.0; "query: " and "passage: " prefixes | [S4](../spikes/s4-retrieval-experiment.md): right source in the top 5 for 29 of 32 development questions, first for 20 of 32; found the two questions keyword search missed | **Used**: embedding model of the baseline (D5), as recommended by S4 |
| [qwen2.5:1.5b](https://ollama.com/library/qwen2.5:1.5b) (Ollama library), model ID `65ec06548149`, weights layer `183715c43589` (986 MB, Cloud Build log of 07/11/2026), 1.54B parameters, Q4_K_M | Write the answer from the retrieved passages | Apache-2.0 | Utku Uçar | 07/11/2026 | Pulled into the container at build time; called over the Ollama HTTP API by `deploy/trial/app.py`; Cloud Run, 4 vCPU, 8 GiB, no GPU | [S5](../spikes/s5-cloud-run-trial-results.md), run A: correct behaviour on 0 of 3 questions; 18.8–51.2 s per answer; declined two answerable questions and gave a false citation | **Rejected**: does not follow the prompt and is too slow on CPU |
| [qwen2.5:7b](https://ollama.com/library/qwen2.5:7b) (Ollama library), model ID `845dbda0ea48`, weights layer `2bada8a74506` (4.7 GB, Cloud Build log of 07/11/2026), 7.62B parameters, Q4_K_M | Write the answer from the retrieved passages | Apache-2.0 | Utku Uçar | 07/11/2026 | As above; Cloud Run, 1 NVIDIA L4 GPU, 4 vCPU, 16 GiB | [S5](../spikes/s5-cloud-run-trial-results.md), run B: correct behaviour on 3 of 3 questions; 0.5–2.4 s per answer | **Candidate** for the alpha and beta; to be measured on the 32 development questions before M6 (S5 recommendation 2) |

Notes:
- **No experiment cards yet.** S4 and S5 are spikes with their own notes, linked above. The baseline run gets the first experiment card.
- **Licence of the fallback model.** R-06's fallback, a 3B model on CPU, would not be under Apache-2.0: in Qwen2.5, the 3B and 72B models have their own Qwen licence. Check the licence before using it.
- **Unpinned versions.** The `ollama/ollama` image is not pinned. S5 recommendation 4 pins the image and the model tags and records them in `ai-bom.yaml` before 18/11/2026.
