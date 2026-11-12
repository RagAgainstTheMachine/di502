# Spike S4: Which passage splitting and search method finds the right source

| Jira | Participants | Facilitator | Timebox | Time spent | Dates | Status | Informs |
|---|---|---|---|---|---|---|---|
| DI502-68 | Utku Uçar | Utku Uçar | 4.5 person-hours | | 03/11 – 12/11/2026 | done | D2 and D3 in the [System Architecture Design Document](../Markdown%20Template/11-system-architecture-design-document.md); the `chunking` and `retrieval` values in `config/rag.yaml` |

**Type:** experiment spike (code and measurements, no language model).

## Question

On our own corpus, does splitting at the documents' own structure find the right source more often than fixed-size windows, and which search method (keyword, embedding or both) should the baseline use?

## Setup

- **Corpus:** the extracted `.md` files of all 8 documents (`data/text/`). Doc01–Doc03 and Doc05–Doc08 were made by `src/extraction/extract.py` (see `EXTRACTION_REPORT.md`). Doc04 (Law No. 6698) was blocked there because the wrong PDF had been supplied; it was extracted on 03/11/2026 from the correct 21-page PDF by `src/extraction/doc04_law_6698.py` (pdfplumber 0.11.10; 33 articles, 3 provisional articles, 8 footnotes). Check with the report's method: 25 of 25 sampled sentences found on the marked page; mean character coverage 0.9989, no page below 0.98.
- **Splitting** (`src/rag/chunking.py`):
  - *structure*: one passage per heading (action, Tedbir, paragraph, glossary term or section); sections over 1,000 characters are split at paragraph or sentence boundaries; every passage starts with the document title and section path. 1,226 passages.
  - *fixed*: windows of 1,000 characters with 200 characters of overlap, no title or section. 1,126 passages.
- **Search** (`src/rag/retrieval.py`):
  - *bm25*: keyword search on whole words [1].
  - *bm25s5*: the same on the first 5 letters of each word, a simple form of Turkish stemming [2] (S1, finding 6).
  - *+id*: when the question names "Eylem N", "Tedbir N.N", "Paragraf N" or "Madde N", passages under that heading go first (US-4).
  - *dense*: embedding search with `intfloat/multilingual-e5-base` [4] ("query: " and "passage: " prefixes, cosine similarity), run on Utku Uçar's laptop CPU on 12/11/2026 with sentence-transformers 6.3.0, transformers 5.22.2, torch 2.15.0.
  - *hybrid*: reciprocal rank fusion [3] of bm25s5 and dense, equal weights, top 50 of each.
- **Questions:** 32 development questions (`docs/eval/dev-set-v0.csv`), 2–7 per document, each with a gold anchor (a phrase in the source). This set is separate from evaluation set v1 (D2) and is used only to choose settings, so that D2 stays unseen until the baseline run.
- **Measures** (`src/experiments/s4_retrieval_spike.py`): hit@1 (the first passage covers the gold anchor), recall@5 (one of the first 5 does), MRR@10 (the mean of 1 ÷ the rank of the first passage that covers the gold anchor, counted as 0 when it is not in the first 10: rank 1 gives 1, rank 2 gives 0.5, rank 5 gives 0.2), and query time.

## Results

32 questions. Runs on 12/11/2026 on a laptop CPU: BM25 rows from run `20261112-2116` (the same numbers as the first run on 03/11), the bm25s5 +id, dense and hybrid rows from run `20261112-2128`. Both runs are in `docs/spikes/results/`.

| Splitting | Search | Hit@1 | Recall@5 | MRR@10 |
|---|---|---|---|---|
| structure | bm25 | 17/32 | 26/32 | 0.64 |
| structure | bm25s5 | 22/32 | 29/32 | 0.77 |
| structure | bm25s5 +id | 23/32 | 29/32 | 0.79 |
| fixed | bm25 | 18/32 | 25/32 | 0.63 |
| fixed | bm25s5 | 17/32 | 22/32 | 0.61 |
| structure | dense (e5-base) | 20/32 | 29/32 | 0.73 |
| structure | hybrid: bm25s5 + dense +id | 26/32 | 28/32 | 0.83 |

BM25 answers a query in under 2 ms and builds its index in 0.1 s. Dense search answers in 33 ms; embedding the 1,226 passages took 304 s once on a laptop CPU, after which the cached embeddings load in about 4 s.

## Findings

1. **Structure splitting finds the source more often.** With the same search (bm25s5), structure passages put the gold source in the top 5 for 29 of 32 questions, fixed windows for 22 of 32. Fixed windows break Kalkınma Planı paragraphs and Tedbir records in the middle: none of the fixed configurations found Paragraf 591.1 or 591.2 in the top 10.
2. **5-letter stemming helps only with structure passages.** It raised recall@5 from 26 to 29 of 32 with structure passages but lowered it from 25 to 22 with fixed windows.
3. **Questions that name an item need an exact lookup.** "Eylem 16 neyi kapsıyor?" was ranked 5th by bm25s5 alone and 1st with +id; the number "16" alone is too common for keyword search.
4. **Keyword search misses questions in everyday words.** "Sohbet botlarına hangi kişisel bilgilerimi yazmamalıyım?" was not found in the top 10 by any BM25 configuration, because the KVKK guide says "ÜYZ uygulamaları", not "sohbet botu". Dense search ranked the right passage 1st (finding 7).
5. **Front matter competes with content.** Tables of contents ("İçindekiler") and the foreword ("SUNUŞ") were the first hit for 2 questions.
6. **A report can outrank the law it explains.** For "Kişisel veriler hangi hâllerde açık rıza olmadan işlenebilir?" the first hits were the TBMM report's sections on processing conditions, and Article 5 of Law No. 6698 was not in the top 10. An answer citing the report would show "report" as the legal status of a rule that is binding law (Objective 4, R-11). Dense search found Article 5 at rank 3, still below the report.
7. **Keyword and dense search miss different questions.** bm25s5 +id misses dev20, dev21 and dev32 in the top 5; dense misses dev03 ("hesaplama gücü" for the GPU programme), dev09 and dev10. No question is missed by both, so each method finds what the other misses.
8. **Equal-weight rank fusion keeps the misses of both.** Hybrid put the right passage first most often (26 of 32), but in the top 5 it missed dev03 and dev09 like dense and dev21 and dev32 like BM25 (28 of 32). Passages that only one method ranks high fall below passages both methods rank in the middle.

## Limits of the evidence

- 32 questions: one question changes a rate by 3.1 percentage points.
- The questions and anchors were written by one author who had read the documents, which favours keyword search; evaluation set v1 is written from user personas.
- A hit is counted only when the passage covers the anchor line; for 2 questions (dev19, dev23) BM25's first hit was another passage of the right section, counted as a miss.
- One embedding model (multilingual-e5-base) was tested; larger or Turkish-specific models were not.
- Doc04 has 4 questions, fewer than the larger documents.

## Recommendation (proposed, for sprint planning)

| Design area | Recommendation | Affects |
|---|---|---|
| Passage splitting | Use structure splitting with at most 1,000 characters and the title and section path in every passage | D2 in the design document; `chunking` in `config/rag.yaml` |
| Baseline search (D5) | Use dense search with `intfloat/multilingual-e5-base`, top 5, over structure passages. It keeps the 29 of 32 of bm25s5 +id and finds dev21 and dev32. The rule set before the run ("hybrid must find dev21 or dev32 and keep 29 of 32") was not met by hybrid (28 of 32, neither found); dense alone meets the same thresholds | D3; `retrieval` and `models.embedding` in `config/rag.yaml` |
| First retrieval experiment (Sprint 3) | Combine keyword and dense search so that each keeps its own top hits (for example the top 3 of each, or a weighted fusion), with the exact-ID lookup, and measure on this development set before evaluation set v1. Expected from finding 7, not yet measured | D3 |
| Binding sources | When the law and a report both match, test giving the passage from binding law a higher rank, and re-check dev32 | D3; Objective 4 |
| Index content | Leave tables of contents, forewords and abbreviation lists out of the index, then re-run | D2 |

## How to reproduce

```cmd
python src\experiments\s4_retrieval_spike.py --methods bm25,bm25s5,bm25s5+id
python src\experiments\s4_retrieval_spike.py --strategies structure --methods bm25s5+id,dense:intfloat/multilingual-e5-base,hybrid:intfloat/multilingual-e5-base+id
```

Packages: `requirements.txt`. The first dense run downloads the model (about 1 GB) and writes the passage embeddings to `data/emb_cache/`.

Each run writes a summary and a per-question file to `docs/spikes/results/`.

## Time spent

| Activity | Who | Planned | Actual |
|---|---|---|---|
| Splitting and search code, development questions | Utku Uçar | 2 h | |
| Doc04 extraction and check | Utku Uçar | 0.5 h | |
| BM25 runs and write-up | Utku Uçar | 1 h | |
| Embedding runs on a laptop and write-up | Utku Uçar | 1 h | |
| **Total** | | **4.5 person-hours** | |

## References

[1] S. Robertson and H. Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond," *Foundations and Trends in Information Retrieval*, vol. 3, no. 4, pp. 333–389, 2009.

[2] F. Can et al., "Information retrieval on Turkish texts," *JASIST*, vol. 59, no. 3, pp. 407–421, 2008.

[3] G. V. Cormack, C. L. A. Clarke and S. Büttcher, "Reciprocal rank fusion outperforms Condorcet and individual rank learning methods," in *Proc. SIGIR 2009*, ACM, 2009, pp. 758–759.

[4] L. Wang et al., "Multilingual E5 Text Embeddings: A Technical Report," arXiv:2402.05672, 2024.
