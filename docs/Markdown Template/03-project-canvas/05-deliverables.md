# Deliverables

| Project Deliverable #: | D1: Project Charter v1 |
|---|---|
| Description: | First version of the Project Canvas pages. |
| Acceptance Criteria: | 1. All cells marked as required are filled. 2. Every objective has at least one numeric success criterion. 3. Every milestone in [Milestones](02-milestones.md) has an associated deliverable on this page. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Project Review Committee; Quality Team; project team |
| Approving Stakeholder(s): | Project Review Committee |

| Project Deliverable #: | D2: Q&A Generation-Dataset v1 |
|---|---|
| Description: | Test questions with reference answers and gold sources, used to evaluate the assistant (`docs/eval/eval-set-v1.csv`). Fixed before any experiment. |
| Acceptance Criteria: | 1. 30 in-scope and 10 out-of-scope questions; the out-of-scope set includes questions asking whether an institution's own plan or practice complies with the rules. 2. The in-scope set has at least 3 factual, 3 procedural, 3 conditional/multi-hop and 3 follow-up questions. 3. Every document in the collection (document inventory) is the gold source of at least 2 questions. 4. Every in-scope question has a reference answer and a gold source (document and article or section). 5. A second team member has checked every reference answer against its source. 6. A written rule for judging an answer correct is included. 7. 10 of the 30 in-scope questions are selected at random as the timed question set for Objective 1; the selection method and result are recorded. |
| Due Date: | 11/11/2026 |
| Stakeholders: | Project Review Committee (AI customer); Quality Team; project team |
| Approving Stakeholder(s): | Project Review Committee |

| Project Deliverable #: | D3: Default-state measurement report |
|---|---|
| Description: | Record of how long pilot participants take today to answer AI-policy questions, using only the official documents and websites (Objective 1). |
| Acceptance Criteria: | 1. 10 pilot participants each answer the 10 timed questions of D2. 2. The time for each question and participant is recorded. 3. The median time is reported. 4. Participants are recorded only by a pseudonymous ID. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project Review Committee (AI customer); AI users: pilot participants |
| Approving Stakeholder(s): | Project Review Committee |

| Project Deliverable #: | D4: Dataset Report v1 |
|---|---|
| Description: | Dataset Report (course template, after Gebru et al.) for the document collection. |
| Acceptance Criteria: | 1. Every section of the Dataset Report template is answered. 2. Every document in the collection is extracted to text. 3. Every page cut, entry selection or manual step is documented so it can be repeated. 4. Each document's legal status, official URL and download date are recorded. 5. In a check of 10 randomly chosen passages, at least 9 match the source PDF in wording and numbers. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project team; Quality Team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D5: Alpha prototype |
|---|---|
| Description: | First working version of the assistant on a local web page, used by the team, with the user stories planned for Sprint 2 in Jira, and its baseline RAG run on the full evaluation set. |
| Acceptance Criteria: | 1. A team member submits a question in Turkish and receives an answer in Turkish. 2. Every answer that cites a source names the document and the article or section, with a link to its official URL. 3. The interface has no field for personal data. 4. All 40 questions of D2 are run with the configuration committed in `config/rag.yaml` and logged in Weights & Biases. 5. The number of correct answers (by the D2 rule) and of answers citing a supporting source is recorded and linked to its Weights & Biases run. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project team (alpha users); Quality Team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D6: Project Charter v2 |
|---|---|
| Description: | Charter updated after the Sprint 2 review. |
| Acceptance Criteria: | 1. Every point in the Quality Team's Sprint 2 review has either a change in the charter or a written rebuttal. 2. Every change lists its reason and the affected requirements and test questions. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project Review Committee; Quality Team; project team |
| Approving Stakeholder(s): | Project Review Committee |

| Project Deliverable #: | D7: MVP evaluation report |
|---|---|
| Description: | Evaluation of the assistant on the evaluation set for Objective 2. |
| Acceptance Criteria: | 1. All 30 in-scope questions are judged against the reference answers using the D2 rule. 2. The results meet the Objective 2 success-criterion levels in the [Project Executive Summary](01-project-executive-summary.md). 3. Each result links to its Weights & Biases run. |
| Due Date: | 09/12/2026 |
| Stakeholders: | Project Review Committee (AI customer); Quality Team; project team |
| Approving Stakeholder(s): | Project Review Committee |

| Project Deliverable #: | D8: Beta release |
|---|---|
| Description: | The deployed assistant with the user stories planned for the beta in Jira, given to the 10 pilot participants. |
| Acceptance Criteria: | 1. Each of the 10 pilot participants opens the assistant in a browser over the internet and receives an answer. 2. Every follow-up question in D2 is answered about the item of the previous exchange it refers to. 3. Every cited source shows its legal status and date. 4. The collection date is visible before a question is asked. 5. The assistant runs on Google Cloud; spending to date is recorded on the [Cost & Funding](07-cost-and-funding.md) page and is below $100. |
| Due Date: | 09/12/2026 |
| Stakeholders: | AI users: 10 pilot participants (the 4 team members and 6 people outside the team); AI customer |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D9: Pilot evaluation report |
|---|---|
| Description: | Results of the pilot for Objectives 1, 3, 4 and 5. |
| Acceptance Criteria: | 1. Objectives 1, 3, 4 and 5 are each reported against their success-criterion levels in the [Project Executive Summary](01-project-executive-summary.md); Objective 1 is compared with D3. 2. The business outcomes of Objectives 1–5 are reported. 3. No personal data of participants is stored. |
| Due Date: | 23/12/2026 |
| Stakeholders: | Project Review Committee (AI customer); AI users: pilot participants; project team |
| Approving Stakeholder(s): | Project Review Committee |

| Project Deliverable #: | D10: Release candidate |
|---|---|
| Description: | Final version of the assistant shown at the final presentation. |
| Acceptance Criteria: | 1. Every user story in the User Story Map is accepted against its acceptance criteria, or listed as not delivered with a reason. 2. Every defect found in the pilot is fixed or listed with a reason. 3. The live demo runs from question to cited answer without errors. |
| Due Date: | 30/12/2026 |
| Stakeholders: | AI users: public institution staff and AI-policy researchers; AI customer |
| Approving Stakeholder(s): | Project Review Committee |

| Project Deliverable #: | D11: Final report |
|---|---|
| Description: | Summary of the project's results against its objectives. |
| Acceptance Criteria: | 1. Each objective (1–5) is reported with its target, measured result and business outcome. 2. Each reported number links to its source (D7, D9 or a Weights & Biases run). 3. Lessons learned are listed. |
| Due Date: | 30/12/2026 |
| Stakeholders: | Project Review Committee; AI customer |
| Approving Stakeholder(s): | Project Review Committee |
