# Spike S1: What research recommends for Turkish RAG

| Jira | Participants | Facilitator | Timebox | Time spent | Dates | Status | Informs |
|---|---|---|---|---|---|---|---|
| DI502-43 | Muhammed Batuhan Tezcan, Elif Yeşim Koçoğlu, Utku Uçar, Deniz Şenkutlu | Utku Uçar | 6 person-hours | 3 person-hours | 26/10 – 28/10/2026 | in progress | DEC-03, DEC-04 and DEC-05 in the [System Architecture Design Document](../Markdown%20Template/11-system-architecture-design-document.md) |

**Type:** research spike (reading only; no code or experiments).

## Question

What does published research recommend for building a retrieval-augmented generation (RAG) pipeline in Turkish, and which of these recommendations should shape our first design for passage splitting, embedding and retrieval?

## Sources

| Source | What it is |
|---|---|
| Köse et al., *RAGTurk* (SIGTURK 2026) [1] | Benchmark of seven RAG pipeline stages on a Turkish question–answer dataset; reference [10] of our charter |
| Baysan and Güngör, *TR-MTEB* (Findings of EMNLP 2025) [2] | Benchmark of Turkish text embeddings |
| Can et al., *Information retrieval on Turkish texts* (JASIST 2008) [3] | Keyword search and word stemming in Turkish |

## Findings

1. **Splitting (RAGTurk).** Passages were split by headings, and each passage carried its document title and section path. Sections longer than 1,000 characters were split further; the authors tried other limits and found 1,000 the best balance. The average passage was about 560 characters.
2. **Retrieval and context (RAGTurk).** The baseline scored 78.7%. The authors' recommended default (a cross-encoder reranker, adding the previous and next passage to each hit, and placing the most relevant passages at the ends of the prompt) scored 84.6% with about 2,000 prompt tokens. The most accurate pipeline (HyDE query rewriting plus reranking and summarising) scored 85.0% but needed about 3,700 tokens.
3. **More LLM steps are not always better (RAGTurk).** Chaining many generative steps lowered accuracy, which the authors attribute to lost Turkish word endings. Simple question clarification with good reranking worked well.
4. **Embedding model (RAGTurk).** RAGTurk used EmbeddingGemma, which is also our candidate in [Facilities & Resources](../Markdown%20Template/03-project-canvas/09-facilities-and-resources.md) row 5. It did not compare embedding models.
5. **Embedding comparison (TR-MTEB).** TR-MTEB covers 26 Turkish datasets in six task types, including retrieval, and publishes results and two Turkish-specific embedding models. It is the place to shortlist embedding models for Turkish retrieval.
6. **Keyword search (Can et al.).** Cutting each word to a fixed prefix gave retrieval quality similar to a full lemmatizer. A simple prefix rule is enough for the keyword part of hybrid search.

## Limits of the evidence

- RAGTurk uses Wikipedia and web text, not legal or policy documents; our article-numbered texts may behave differently.
- RAGTurk did not test hybrid keyword and vector search (it lists it as future work), and its reranker (ms-marco-MiniLM-L-12-v2) was trained on English data.
- RAGTurk's accuracy combines an LLM judge with similarity to a reference answer; see [S2](s2-rag-evaluation-methods.md) for the weaknesses of LLM judges.

## Recommendation (proposed, for sprint planning)

| Design area | Recommendation | Affects |
|---|---|---|
| Passage splitting | Split at headings and article numbers; every passage carries the document title and section path; start with at most 1,000 characters | DEC-03, [S3](s3-chunking-research.md) |
| Embedding model | Keep EmbeddingGemma as the first candidate; shortlist one or two Turkish models from the TR-MTEB retrieval results | DEC-04 |
| Retrieval | Add a cross-encoder reranker and previous/next passage to the candidate design; treat hybrid keyword search as our own experiment, with simple prefix stemming for the keyword part | DEC-05 |
| Query rewriting | Do not start with HyDE or several chained LLM steps; in RAGTurk they nearly doubled the prompt (about 3,700 against 2,000 tokens) for 0.4 percentage points of accuracy | DEC-06 |

## Time spent

| Activity | Who | Planned | Actual |
|---|---|---|---|
| Reading the sources and writing 3–5 findings each | All four, 1 h each | 4 h | |
| Discussion and recommendation (30 min) | All four | 2 h | |
| **Total** | | **6 person-hours** | |

## References

[1] S. K. Köse et al., "RAGTurk: Best Practices for Retrieval Augmented Generation in Turkish," in *Proc. SIGTURK 2026*, ACL, 2026, pp. 179–196. https://aclanthology.org/2026.sigturk-1.15

[2] M. S. Baysan and T. Güngör, "TR-MTEB: A Comprehensive Benchmark and Embedding Model Suite for Turkish Sentence Representations," in *Findings of EMNLP 2025*, ACL, 2025, pp. 8867–8887. https://aclanthology.org/2025.findings-emnlp.471

[3] F. Can et al., "Information retrieval on Turkish texts," *JASIST*, vol. 59, no. 3, pp. 407–421, 2008. https://repository.bilkent.edu.tr/items/5be10741-6b40-44ba-b324-9e7951d54c03
