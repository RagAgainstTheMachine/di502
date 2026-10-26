# Spike S3: How to split legal and policy documents into passages

| Jira | Participants | Facilitator | Timebox | Time spent | Dates | Status | Informs |
|---|---|---|---|---|---|---|---|
| DI502-45 | Muhammed Batuhan Tezcan, Elif Yeşim Koçoğlu, Utku Uçar, Deniz Şenkutlu | Utku Uçar | 6 person-hours | 4 person-hours | 26/10 – 28/10/2026 | in progress | DEC-03 in the [System Architecture Design Document](../Markdown%20Template/11-system-architecture-design-document.md) and the `chunking` values in `config/rag.yaml` |

**Type:** research spike (reading only; no code or experiments).

## Question

What does research say about the size and boundaries of the passages a RAG system retrieves, especially for legal texts, and which approach should we start with for our corpus of laws, plans, reports and guidance?

## Sources

| Source | What it is |
|---|---|
| Akarajaradwong et al., *NitiBench* (2025) [1] | Legal question answering over Thai legislation; compares ways of splitting laws |
| Köse et al., *RAGTurk* (SIGTURK 2026) [2] | Turkish RAG benchmark; reference [10] of our charter |
| Chen et al., *Dense X Retrieval* (EMNLP 2024) [3] | Compares passages, sentences and single-fact "propositions" as retrieval units |
| Anthropic, *Contextual Retrieval* (2024) [4] | Adds a short description of where each passage sits in its document before indexing |

## Findings

1. **One legal section per passage works best for laws (NitiBench).** Splitting legislation so that each passage holds exactly one complete section improved both retrieval and final answers compared with splitting by characters, by lines or by generic separators (tested at 212–553 characters with overlaps of 50–200). Following cross-references to other sections automatically did not help. Retrieval, not the language model, was the main bottleneck.
2. **Headings travel with the passage (RAGTurk).** Each Turkish passage carried its document title and section path. Sections over 1,000 characters were split further; the average passage was about 560 characters. Adding the previous and next passage to each hit was part of the recommended default.
3. **Smaller units help when the prompt is short (Dense X).** Indexing single facts instead of whole passages raised recall@5 by 9–12 points for retrievers that were not trained for the task, but much less for trained ones. The advantage was largest when only 100–200 words of context fit into the prompt and shrank as the prompt grew. Producing single facts needs a language model pass over the whole corpus.
4. **Context in the passage reduces failed searches (Contextual Retrieval).** Adding a short, generated description of each passage's place in its document, together with keyword search on the same text, cut failed retrievals by 49%; adding a reranker cut them by 67% (from 5.7% to 1.9% of searches). The description costs one language-model call per passage.

## What this means for our corpus

| Document type (our corpus) | Natural unit | Source of the advice |
|---|---|---|
| Law No. 6698 | One article (madde) | NitiBench [1] |
| Action Plan, Development Plan, Annual Programme | One action, numbered paragraph or Tedbir entry | NitiBench [1], RAGTurk [2] |
| TBMM report, KVKK guide, TÜBİTAK policy | One recommendation or titled section; split above about 1,000 characters | RAGTurk [2] |
| Public-sector AI glossary | One term with its definition | Dense X [3]: one self-contained fact per unit |

## Limits of the evidence

- NitiBench is about Thai law and Dense X and Contextual Retrieval about English; none tests Turkish policy documents.
- The reported gains come from different datasets and metrics and cannot be added up.

## Recommendation (proposed, for sprint planning)

1. Split at the document's own structure: one article, action, paragraph, Tedbir entry, recommendation or glossary term per passage.
2. Put the document title and section path at the start of every passage. This is a free version of Contextual Retrieval, because our documents already have headings; generated descriptions are an option only if retrieval fails in the baseline.
3. Split sections longer than about 1,000 characters, repeating the heading in each piece; instead of large overlaps, add the previous and next passage to each hit.
4. Do not start with single-fact propositions or automatic cross-reference following; both add cost and showed no clear gain for legal text.
5. The final size and overlap are chosen in the chunk-size experiments against the baseline (D5), as DEC-03 already plans.

## Time spent

| Activity | Who | Planned | Actual |
|---|---|---|---|
| Reading the sources and writing 3–5 findings each | All four, 1 h each | 4 h | |
| Discussion and recommendation (30 min) | All four | 2 h | |
| **Total** | | **6 person-hours** | |

## References

[1] P. Akarajaradwong et al., "NitiBench: A Comprehensive Study of LLM Framework Capabilities for Thai Legal Question Answering," arXiv:2502.10868, 2025. https://arxiv.org/abs/2502.10868

[2] S. K. Köse et al., "RAGTurk: Best Practices for Retrieval Augmented Generation in Turkish," in *Proc. SIGTURK 2026*, ACL, 2026, pp. 179–196. https://aclanthology.org/2026.sigturk-1.15

[3] T. Chen et al., "Dense X Retrieval: What Retrieval Granularity Should We Use?," in *Proc. EMNLP 2024*, ACL, 2024. https://arxiv.org/abs/2312.06648

[4] Anthropic, "Introducing Contextual Retrieval," Sep. 2024. https://www.anthropic.com/news/contextual-retrieval
