# Evaluation Metrics

This page lists what we measure, how we measure it, and which objective each measure checks. The targets come from the objectives in the [Project Executive Summary](../Markdown%20Template/03-project-canvas/01-project-executive-summary.md). The metric choices follow the course literature review on building test datasets for RAG [1], and spike [S2](../spikes/s2-rag-evaluation-methods.md) covers the earlier research on judging answers.

We test on the current version of the evaluation set (D2) in `docs/eval/`, described in [eval-set-metadata.md](eval-set-metadata.md). Each row has a question, a gold answer and the gold source that contains it, which is the minimum a test example needs [1]. The set has in-scope questions, which the documents answer, and out-of-scope questions, which the assistant should decline.

The questions and their number can change between versions, so the targets below are rates. A target is met when the share of passing questions reaches it, rounded up to a whole question. We report both the count and the rate, for example "33 of 40 (83%)".

## 1. Metrics we report

These decide whether objectives O2, O4 and O5 are met. They are computed with DeepEval [3] and RAGAS [2]. Where no built-in metric fits, we use DeepEval's G-Eval [8], which scores an answer against a rule we write, or a small custom metric. A question passes when its score reaches the threshold, and we report the number of questions that pass.

| Metric | Objective | Tool and metric | Scored on | Target |
|---|---|---|---|---|
| Answer correctness | O2 | RAGAS `FactualCorrectness` and DeepEval `FaithfulnessMetric` (both must pass) | In-scope questions | 80% |
| Citation support | O2 | G-Eval: every cited sentence is supported by the passage it cites [7] | In-scope questions | 80% |
| Legal-status accuracy | O4 | Custom metric: each cited document's label matches the `legal_status` column | In-scope questions | 90% |
| Decline accuracy | O5 | G-Eval: the response declines and gives no answer, guess or yes/no verdict | Out-of-scope questions | 80% |

With the current set of 40 in-scope and 10 out-of-scope questions, these targets are 32, 32, 36 and 8 passing questions.

The decline rule is also run on the in-scope questions to count false declines, so declining everything cannot pass.

**Judge setup.** The judge is a self-hosted model, different from the one that answers. The G-Eval rules, thresholds, tool versions and judge model are fixed before the baseline run. Before the baseline, two of us label 10 questions by hand to check that the judge agrees with us.

## 2. Retrieval metrics

Retrieval is scored separately, so a wrong answer can be traced to the search or to the writing.

- **Recall at 5 and MRR**, computed from the gold source in each row. These need no judge [1].
- **Context precision and context recall** (RAGAS, DeepEval): are the right passages retrieved and ranked at the top?
- **Context entities recall** (RAGAS): are the article and measure numbers from the gold answer in the passages? This matters for our documents.

## 3. Other answer metrics

- **Answer relevancy** (RAGAS, DeepEval): does the answer address the question?
- **Turn relevancy and knowledge retention** (DeepEval): are follow-up questions in a chat answered correctly (US-9)?

These have no target; we use them to compare runs.

## 4. Results by slice

An overall score can hide a weak group of questions, so every run is also reported per slice [1]:

- **Question type:** factual, procedural, conditional/multi-hop, follow-up and out-of-scope (the `type` column).
- **User story:** the `story_tag` column, so a weak result points to the story it affects.
- **Single vs. multi-document:** questions whose gold source names one document vs. several.

## 5. Hard cases

A test set needs questions the assistant should not simply answer [1]. Ours are the out-of-scope questions in D2. The literature names a few kinds, and we check how many of each the set contains:

| Kind | Example for our corpus | Expected behaviour |
|---|---|---|
| Unanswerable | A question about a topic none of the eight documents covers | Say it cannot answer from the documents (US-10) |
| False premise | "When did Türkiye's AI law come into force?" (there is no AI-specific law yet) | Correct the assumption instead of inventing a date [6] |
| Not yet prepared | Details that a plan says will be prepared later | Quote the passage and say the details are not in the documents (US-11) |
| Compliance judgement | "Does my institution's plan comply with the Action Plan?" | Give no verdict; state what the documents say (US-12) |
| Time-sensitive | A question about the current legal state | Answer from the collection and show the collection date (US-8) [6] |

It is hard to prove that no document answers an "unanswerable" question [4], so each one is checked by hand against the eight documents.

## 6. Checking the test set itself

The scores are only as good as the test set. Before the baseline run we check three things [1]:

1. **Is it correct?** Every gold answer is stated in its gold source, and every question is clear without seeing the document. A second member checks each row (the `checked_by` column).
2. **Is it really multi-document?** We ask each multi-document question with only one of its gold documents, then with none. If it is still answered correctly, it has a shortcut and is not a real multi-document question [5].
3. **Is it balanced?** We count questions per type, question word (who, what, when, which, why) and user persona, and compare them with what the users in the Story Map would ask.

## 7. Running the evaluation

- **Each run** goes through the normal application flow on the full set and is logged in Weights & Biases with its Git commit, settings, per-question scores and totals. Full questions, answers and prompts stay in the project files.
- **Regression tests:** DeepEval tests can fail when a metric drops below a threshold and can run in GitHub Actions [3]. We set the thresholds from the baseline run.
- **Data stays with us:** we do not use the DeepEval cloud platform or any other hosted service that would receive our questions and answers.
- **Versions are pinned:** both tools change their interfaces between versions [1].

## References

[1] T. Taskaya Temizel, "Building Test Datasets for RAG: Methods, Tools and Quality Control," literature review (slides), 2026.

[2] RAGAS, "Documentation: Available Metrics, Testset Generation, Experimentation, Multi-turn Evaluation." docs.ragas.io.

[3] DeepEval, "Documentation: Metrics, Golden Synthesizer, Conversation Simulator, Evaluation." deepeval.com/docs.

[4] S. Filice, G. Horowitz, D. Carmel, Z. Karnin, L. Lewin-Eytan and Y. Maarek, "Generating Diverse Q&A Benchmarks for RAG Evaluation with DataMorgana," arXiv:2501.12789, 2025.

[5] S. Min, E. Wallace, S. Singh, M. Gardner, H. Hajishirzi and L. Zettlemoyer, "Compositional Questions Do Not Necessitate Multi-hop Reasoning," in *Proc. ACL 2019*, 2019.

[6] X. Yang et al., "CRAG – Comprehensive RAG Benchmark," in *Proc. NeurIPS 2024 Datasets and Benchmarks Track*, 2024.

[7] T. Gao, H. Yen, J. Yu and D. Chen, "Enabling Large Language Models to Generate Text with Citations," in *Proc. EMNLP 2023*, 2023, pp. 6465–6488.

[8] Y. Liu, D. Iter, Y. Xu, S. Wang, R. Xu and C. Zhu, "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment," in *Proc. EMNLP 2023*, 2023.
