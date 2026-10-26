# Spike S2: How to judge RAG answers

| Jira | Participants | Facilitator | Timebox | Time spent | Dates | Status | Informs |
|---|---|---|---|---|---|---|---|
| DI502-44 | Muhammed Batuhan Tezcan, Elif Yeşim Koçoğlu, Utku Uçar, Deniz Şenkutlu | Utku Uçar | 6 person-hours | 4 person-hours | 26/10 – 28/10/2026 | in progress | The correctness rule in D2 (acceptance criterion 6), the evaluation section of the [System Architecture Design Document](../Markdown%20Template/11-system-architecture-design-document.md), D7 and D9 |

**Type:** research spike (reading only; no code or experiments).

## Question

How should we judge whether an answer is correct, whether its citations support it, and whether an out-of-scope question was declined, so that the Objective 2, 4 and 5 results in the [Project Executive Summary](../Markdown%20Template/03-project-canvas/01-project-executive-summary.md) can be trusted? Can a language model do part of the judging?

## Sources

| Source | What it is |
|---|---|
| Es et al., *RAGAS* (2023) [1] | Automatic scores for RAG answers without reference answers |
| Saad-Falcon et al., *ARES* (NAACL 2024) [2] | Trained judge models corrected with a small human-labelled set |
| Gao et al., *ALCE* (EMNLP 2023) [3] | Benchmark for answers with citations |
| Zheng et al., *Judging LLM-as-a-Judge* (NeurIPS 2023) [4] | How far a language model can replace human judges |

## Findings

1. **Judge statement by statement (RAGAS).** Faithfulness splits an answer into statements and counts how many are supported by the retrieved passages (supported ÷ all). It is scored separately from whether the answer addresses the question and whether the retrieved passages were relevant. On a small English test set it agreed with human pairwise judgements 95% of the time for faithfulness, but only 78% for answer relevance and 70% for passage relevance.
2. **Correctness and citation support are different things (ALCE).** ALCE scores citations separately: does the cited text support each statement, and is each citation needed? Even the best models of 2023 lacked complete citation support in about half of the answers on one dataset. This matches Objective 2, which counts correct answers and supported citations separately.
3. **Automatic judges still need human labels (ARES).** ARES trains small judge models and corrects their errors with a few hundred human-labelled examples. Our evaluation set has 40 questions, so this method costs more than it saves.
4. **LLM judges are useful but biased (Zheng et al.).** A strong model agreed with humans 85% of the time, against 81% between two humans. Judges prefer the first answer shown, prefer longer answers, and may favour their own answers. Giving the judge a reference answer cut its errors on maths questions from 14 of 20 to 3 of 20.
5. **Separate retrieval from generation (RAGTurk, see [S1](s1-turkish-rag-literature.md)).** Retrieval was scored against the gold passages (for example recall@5) separately from the answer, which shows whether an error came from search or from writing.

## Recommendation (proposed, for sprint planning)

| Question | Recommendation |
|---|---|
| Who judges the reported results (D7, D9)? | Two team members, using the written rule in D2. With 40 questions, human judging is affordable and is the reference. Disagreements are discussed and the number of disagreements is recorded. |
| What does the correctness rule say? | Write it statement by statement: an answer is correct when it contains the key points of the reference answer and none of its statements contradicts or goes beyond the official documents. |
| How are citations judged? | Separately from correctness: for each answer, does every cited document and section support the statement it is attached to? This gives the "24 of 30 cited" count. |
| How is a decline judged? | Count the fixed notice on the 10 out-of-scope questions (Objective 5). Also count in-scope questions that were wrongly declined, so the rule does not reach its target by refusing too much. |
| Can a language model judge? | Only to speed up experiments between sprints, not for reported results. If used: give it the reference answer, use a different model from the one that writes the answers, and check it against the human judgements on 10 questions first. |
| What else is logged? | Whether the gold source appears in the top 5 retrieved passages, as a diagnostic in each Weights & Biases run. |

## Time spent

| Activity | Who | Planned | Actual |
|---|---|---|---|
| Reading the sources and writing 3–5 findings each | All four, 1 h each | 4 h | |
| Discussion and recommendation (30 min) | All four | 2 h | |
| **Total** | | **6 person-hours** | |

## References

[1] S. Es, J. James, L. Espinosa-Anke and S. Schockaert, "Ragas: Automated Evaluation of Retrieval Augmented Generation," arXiv:2309.15217, 2023. https://arxiv.org/abs/2309.15217

[2] J. Saad-Falcon, O. Khattab, C. Potts and M. Zaharia, "ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems," in *Proc. NAACL 2024*, ACL, 2024, pp. 338–354. https://aclanthology.org/2024.naacl-long.20

[3] T. Gao, H. Yen, J. Yu and D. Chen, "Enabling Large Language Models to Generate Text with Citations," in *Proc. EMNLP 2023*, ACL, 2023, pp. 6465–6488. https://aclanthology.org/2023.emnlp-main.398

[4] L. Zheng et al., "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena," in *Proc. NeurIPS 2023 Datasets and Benchmarks Track*, 2023. https://arxiv.org/abs/2306.05685
