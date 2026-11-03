# Evaluation Metrics

This page lists what we measure and how. The targets come from the objectives in the [Project Executive Summary](../Markdown%20Template/03-project-canvas/01-project-executive-summary.md), and the way we judge answers follows spike [S2](../spikes/s2-rag-evaluation-methods.md). Results are written in [results.md](results.md), and every experiment run is logged in Weights & Biases.

We test with evaluation set v1 (D2): 30 in-scope and 10 out-of-scope questions, each with a reference answer and a gold source. Ten of the in-scope questions are also used for the timed test in the pilot. Since the sets are small, we report counts ("24 of 30") rather than percentages.

## Metrics we report

Two of us judge each answer using the correctness rule in D2. If we disagree, we talk it through and note the disagreement.

| Metric | How we count it | Target | Objective |
|---|---|---|---|
| Answer correctness | Answers that contain the key points of the reference answer and say nothing beyond the documents | 24 of 30 | O2 |
| Citation support | Answers where every citation supports the sentence it is attached to | 24 of 30 | O2 |
| Legal-status accuracy | Answers where the legal status shown for each source matches the document inventory | 27 of 30 | O4 |
| Declines | Out-of-scope and compliance questions that get a clear decline instead of a guess | 8 of 10 | O5 |
| Time per task | Median time on the 10 timed questions, compared with the default state (D3) | Half of D3 or less | O1 |
| Would use again | Pilot participants who say yes in the survey | 7 of 10 | O3 |

Correctness and citation support are measured at the baseline (D5) and the MVP evaluation (D7). The others are measured in the pilot (D9), together with the business outcomes in the Executive Summary.

## Metrics we use to debug

These have no target. We log them in each run so we can see what went wrong:

- **Retrieval hit at 5:** was the gold source in the top 5 passages? If not, the problem is the search, not the answer.
- **Wrong declines:** how many in-scope questions were declined. This keeps us from hitting the decline target just by refusing more.
- **Follow-up accuracy:** did a follow-up question get answered about the right item?
- **Response time:** median and slowest answers.
- **Cost per run:** cloud spending for one run of the 40 questions, so we stay inside the $100 credit.

We may use a language model for a quick score during experiments, but never for the results we report. If we do, it gets the reference answer and is a different model from the one being tested.

We also check, before the beta, that no personal data ends up in logs, evaluation files or the index.

## What the literature uses

Most RAG papers split evaluation into retrieval, the answer, and citations.

**Retrieval.** Recall at k, precision at k and nDCG are standard measures [5], and mean reciprocal rank (MRR) comes from question-answering evaluation [7]. We use hit at 5 because it is simple and each question has one gold source. MRR could help when comparing retrieval settings. nDCG needs graded relevance labels, which we don't have.

**The answer.** RAGAS [1] and ARES [2] score faithfulness (are the answer's statements supported by the passages?), answer relevance and context relevance. Our correctness rule covers the first two by hand. Word-overlap scores such as exact match, F1, ROUGE and BLEU are common in older QA work, but they work poorly for free-form Turkish answers, where the same word can take many endings. BERTScore [6] compares meaning instead of words and could be a useful extra check with a multilingual model.

**Citations.** ALCE [3] separates citation recall (is each statement supported by its citations?) from citation precision (is each citation needed?). Our citation support metric is citation recall.

**Declines.** The RGB benchmark [4] calls this "negative rejection": declining when the retrieved passages hold no answer. It also tests noise robustness and combining information from several documents, which our multi-document questions cover.

## References

[1] S. Es, J. James, L. Espinosa Anke and S. Schockaert, "RAGAs: Automated Evaluation of Retrieval Augmented Generation," in *Proc. EACL 2024: System Demonstrations*, St. Julians, Malta, 2024, pp. 150–158.

[2] J. Saad-Falcon, O. Khattab, C. Potts and M. Zaharia, "ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems," in *Proc. NAACL 2024 (Volume 1: Long Papers)*, Mexico City, Mexico, 2024, pp. 338–354.

[3] T. Gao, H. Yen, J. Yu and D. Chen, "Enabling Large Language Models to Generate Text with Citations," in *Proc. EMNLP 2023*, Singapore, 2023, pp. 6465–6488.

[4] J. Chen, H. Lin, X. Han and L. Sun, "Benchmarking Large Language Models in Retrieval-Augmented Generation," in *Proc. AAAI 2024*, vol. 38, no. 16, 2024, pp. 17754–17762.

[5] C. D. Manning, P. Raghavan and H. Schütze, *Introduction to Information Retrieval*, Cambridge University Press, 2008, ch. 8.

[6] T. Zhang, V. Kishore, F. Wu, K. Q. Weinberger and Y. Artzi, "BERTScore: Evaluating Text Generation with BERT," in *Proc. ICLR 2020*, 2020.

[7] E. M. Voorhees, "The TREC-8 Question Answering Track Report," in *Proc. Eighth Text REtrieval Conference (TREC-8)*, NIST, 1999, pp. 77–82.
