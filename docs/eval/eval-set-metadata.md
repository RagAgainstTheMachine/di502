# Evaluation set metadata

**Version:** v1 (describes `docs/eval/eval-set-v1.csv`)

This page explains every column of `docs/eval/eval-set-v1.csv`. 


## Columns

| Column | What it holds | Allowed values and rules | Serves |
|---|---|---|---|
| `id` | A stable identifier for the question | Unique. Never changed, never reused | Tracing a question through reviews and runs |
| `question` | The question, as a user would ask it | Natural-language Turkish, not a keyword search. Covers only documents in the retrieval set | The input to every run |
| `type` | The kind of question | One of `factual`, `procedural`, `conditional/multi-hop`, `follow-up`, `out-of-scope` | D2 criteria 1 and 2 |
| `gold_answer` | The reference answer | In-scope: the correct answer, supported by the gold source. Out-of-scope: the decline and its reason. Never empty | Judging correctness with the written rule (D2 criterion 6) |
| `gold_source` | Where the answer is found | Document ID, article or section, and page. Never empty for in-scope questions; may be empty for out-of-scope ones. The exact form per document is fixed in phase 1 of the build guide and added here | D2 criteria 3 and 4; citation checks |
| `story_tag` | The user story whose criterion this question tests | Exactly one tag per in-scope question, taken from the user stories. The allowed list is the one in the user-story requirements | Trace chain: story, requirement, question, run |
| `follows` | The `id` of the first question, when this row is a follow-up | Empty unless `type` is `follow-up`. The first question and its answer are scripted when the follow-up is run | Multi-turn runs |
| `timed` | Whether the question is in the timed set | `yes` for the 10 of the 30 in-scope questions drawn at random, otherwise empty. The draw method and result are recorded in `docs/eval/timed-set.md` | D2 criterion 7 |
| `checked_by` | The second team member who checked the answer | A name, filled only when the checker agrees. Never the writer. Empty means not yet checked | D2 criterion 5 |

An empty `checked_by` on a row that has been reviewed means the checker did not agree. The reason goes in the review log.
