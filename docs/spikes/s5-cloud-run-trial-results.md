# Spike S5 (trial): small CPU model against 7b GPU model on Cloud Run

| Jira | Participant | Date | Status | Informs |
|---|---|---|---|---|
| **[TBC]** | Utku Uçar | 07/11/2026 | trial done; full measurement open | Language model choice in `config/rag.yaml`; C-07; Cost & Funding row 18; R-06; R-11 |

**Type:** trial deployment, not a measurement. Only 3 questions were asked, so the results show the direction of the difference, not its size.

## Question

Can the answer path (search, language model, citation check) run on Cloud Run, and does a 1.5b model on CPU answer acceptably, or is a 7b model on a GPU needed?

## Setup

- **Project:** personal project `utku-llm-deneme`, region `europe-west1`, paid from the education credit. Steps: [Cloud Run trial deployment guide](../deploy/cloud-run-trial-guide.md).
- **Search (the same in both runs):** BM25 on 5-letter prefixes over 977 passages (paragraphs joined up to 900 characters), top 4 passages sent to the model. Offline check on the 32 development questions: the gold passage is in the top 4 for 23/32. S4's structure splitting with ID lookup reached 29/32 in the top 5.
- **Prompt and decline rule:** taken from `src/experiments/ask.py`. The fixed decline notice is shown when the model writes CEVAP_YOK or cites no valid source number.

| Run | Service | Model | Hardware |
|---|---|---|---|
| A | `di502-trial` | qwen2.5:1.5b | 4 vCPU, 8 GiB, no GPU |
| B | `di502-trial-gpu` | qwen2.5:7b | 1 NVIDIA L4, 4 vCPU, 16 GiB |

## Results

| Question | Expected | A: 1.5b, CPU | B: 7b, L4 GPU |
|---|---|---|---|
| Açık rıza nedir? | Definition; Law No. 6698, Art. 3 | Declined · 51.2 s | Correct definition, cited · 2.4 s |
| Kamu kurumları yapay zekâ yol haritasını ne kadar sürede hazırlamalı? | 12 weeks; Doc01, Eylem 7 | Declined · 22.1 s | Correct ("12 hafta"), cites Eylem 7 · 1.2 s |
| Yarın İstanbul'da hava nasıl olacak? | Decline (out of scope) | Repeated the question with a false citation [2] · 18.8 s | Declined · 0.5 s |
| **Behaviour correct** | | **0/3** | **3/3** |

| Item | A | B |
|---|---|---|
| Build and deploy time | about 10 min | under 13 min |
| GPU quota | not needed | granted on the first deployment, no request |
| Cost | about $0.01 (Cloud Run spend cap page, 07/11) | about $0.35 estimated (20 min × $1.05/h); check in Billing after 24 h |

## Findings

1. **The 1.5b model is not usable for this task.** In question 2 the correct passage was at rank 3 and the model still declined. In question 3 it did not follow the prompt and produced a false citation.
2. **The 7b model answered all 3 correctly and in under 3 s each on the L4.** The first question was fast because the app loads the model at start-up, so this trial did not measure the true cold start (a new instance starting up and loading the model).
3. **Legal status risk (R-11, O4).** The "açık rıza" answer cites the KVKK guide (Doc06) and the TBMM report (Doc05). Both passages contain the definition, so the citations support the answer. But the binding source, Law No. 6698, Art. 3, was not retrieved. This is the same pattern as dev32 in S4.
4. **The decline check can be fooled.** Any answer that carries a valid source number counts as an answer (run A, question 3). A floor on the search score would catch out-of-scope questions before they reach the model.

## Recommendations

| # | Recommendation | For | By |
|---|---|---|---|
| 1 | Do not use models smaller than 7b on CPU. Use a 7b-class model on the L4 GPU for the beta. A 3b model on CPU, the cheaper fallback for R-06, is untested. | Model choice | Before M6, 20/11/2026 |
| 2 | Measure run B on all 32 development questions with a batch script: share correct, declines, median time, cold start of a fresh instance. One session takes about 30 min and costs under $1. | Utku Uçar | 11/11/2026 |
| 3 | Search: use S4's structure splitting with ID lookup, add a score floor for out-of-scope questions, and rank binding sources (laws) first when several documents state the same text. | Search owners | Before the baseline run |
| 4 | Pin the Ollama image version and the model tag, and record them in `ai-bom.yaml` (D5 Definition of Done, "Versions are recorded"). | Utku Uçar | 18/11/2026 |
| 5 | Budget: at $1.05 per hour, Cost row 18 ($27) covers about 25 GPU hours. Keep `--max-instances 1`, delete the GPU service after each session, and keep a Cloud Run spend cap on the team project. | Elif Yeşim Koçoğlu | When the team project is created |
| 6 | Web access (deadline 02/12/2026, Dependencies 9): a public web service without a GPU, calling a private GPU model service, as in the planned architecture. Visitors reach only the cheap web service, and the GPU service scales to zero when no questions come in. | Utku Uçar | After the front-end decision |

## Limits of this trial

3 questions, 1 run each, no repeat; one search setup; personal project, not the team project; the cold start was not measured; the web page label says "CPU" for both runs (fixed text in `app.py`).
