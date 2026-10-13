# Deliverables

| Project Deliverable #: | D1: Default-state measurement report |
|---|---|
| Description: | Record of how long pilot participants take to answer AI-policy questions today, using only the official documents and websites. Baseline for Objective 1. |
| Acceptance Criteria: | 1. 10 pilot participants each answer the same 10 timed policy questions. 2. The time for each question and participant is recorded. 3. The median time is reported. 4. Participants are recorded only by a pseudonymous ID. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Product Owner; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D2: Project Charter v1 |
|---|---|
| Description: | First version of the Project Canvas pages. |
| Acceptance Criteria: | 1. All cells marked as required are filled. 2. Every objective has at least one numeric success criterion. 3. Every milestone in [Milestones](02-milestones.md) has an associated deliverable on this page. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Project Review Committee; Quality Team; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D3: Q&A Generation-Dataset v1 |
|---|---|
| Description: | Test questions with reference answers and gold sources, used to evaluate the assistant (`docs/eval/eval-set-v1.csv`). Fixed before any experiment. |
| Acceptance Criteria: | 1. 30 in-scope and 10 out-of-scope questions. 2. Each in-scope question type (factual, procedural, conditional/multi-hop, follow-up) has at least 3 questions. 3. Each corpus document (D01–D05, D08, D10) is the gold source of at least 2 questions. 4. Every in-scope question has a reference answer and a gold source (document and article or section). 5. Questions are tagged as multi-document and time-sensitive where they apply. 6. At least 10 questions come from people outside the team (public institution staff or AI-policy researchers). 7. A second team member has checked every reference answer against the source. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Project team (AI developer role); Quality Team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D4: User Story Map v1 |
|---|---|
| Description: | Feature–epic–story–task hierarchy of the assistant, with the user stories in Jira. |
| Acceptance Criteria: | 1. Every charter feature (F1–F6) has at least one user story. 2. Every story has acceptance criteria, a priority, a story point estimate and an assignee in Jira. 3. The map in the repository lists every epic and story with its Jira key. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Project team; Quality Team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D5: System Architecture Diagram v1 |
|---|---|
| Description: | Diagram of the assistant's components and how they connect, with a one-page design overview (`docs/design.md`). |
| Acceptance Criteria: | 1. The diagram shows the document store, the retriever, the language model, the chat interface and the evaluation logging, and the data flow between them. 2. Each component names its technology or a learning spike that will choose it. 3. The design overview is at most two pages. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Project team; Quality Team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D6: Dataset Report v1 |
|---|---|
| Description: | Report on the prepared document collection: what was extracted, how, and with what result. |
| Acceptance Criteria: | 1. All 7 corpus documents are extracted to text. 2. D04 is typed in by hand; D05 is limited to PDF pages 642–806; D08 contains only the AI-related Tedbir entries, each with its number and responsible institution. 3. Each document has its legal status, official URL and download date recorded. 4. In a check of 10 randomly chosen passages, at least 9 match the PDF word for word. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project team (AI developer role) |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D7: Baseline experiment card |
|---|---|
| Description: | First end-to-end run of the assistant on the evaluation set. |
| Acceptance Criteria: | 1. All 40 questions of D3 are run. 2. The configuration (`config/rag.yaml`) is committed and linked. 3. The run is logged in Weights & Biases. 4. The number of correct answers and of answers citing a supporting source are reported. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project team; Quality Team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D8: Alpha prototype |
|---|---|
| Description: | First working version of the assistant on a local web page, used by the team (user stories US-1, US-4, US-7). |
| Acceptance Criteria: | 1. A team member can submit a question in Turkish and receive an answer in Turkish. 2. For each of the 30 in-scope test questions, the answer names the document and the article or section. 3. Every cited document has a link to its official URL. 4. The interface has no field for personal data. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project team (alpha users) |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D9: Project Charter v2 |
|---|---|
| Description: | Charter updated after the Sprint 2 review. |
| Acceptance Criteria: | 1. Every Quality Team review point has either a change in the charter or a written rebuttal. 2. Every change lists its reason and the affected requirements and test questions. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project Review Committee; Quality Team; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D10: Cloud deployment v1 |
|---|---|
| Description: | The assistant running on Google Cloud, with a record of its cost. |
| Acceptance Criteria: | 1. The assistant opens in a browser on a computer outside the team. 2. Cumulative Google Cloud spending is recorded on the [Cost & Funding](07-cost-and-funding.md) page and is below $100. 3. A billing budget alert is set up. |
| Due Date: | 02/12/2026 |
| Stakeholders: | AI users: pilot participants; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D11: MVP evaluation report |
|---|---|
| Description: | Evaluation of the assistant on the evaluation set for Objective 2. |
| Acceptance Criteria: | 1. All 30 in-scope questions are evaluated against the reference answers by two team members. 2. At least 25 of 30 answers are correct. 3. At least 27 of 30 answers cite a document and section that support them. 4. Each result links to its Weights & Biases run. |
| Due Date: | 09/12/2026 |
| Stakeholders: | Product Owner; Quality Team; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D12: Beta release |
|---|---|
| Description: | The deployed assistant with all user stories (US-1 to US-7), given to the pilot participants. |
| Acceptance Criteria: | 1. Each of the 10 pilot participants can open the assistant and receive an answer. 2. A follow-up question that refers to the previous exchange is answered about the referred item. 3. Every cited source shows its legal status and date. 4. The collection date is visible before a question is asked. |
| Due Date: | 09/12/2026 |
| Stakeholders: | AI users: 10 pilot participants (public institution staff and AI-policy researchers); AI customer |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D13: Project Charter v3 |
|---|---|
| Description: | Charter updated after the Sprint 3 review. |
| Acceptance Criteria: | 1. Every Quality Team review point has either a change in the charter or a written rebuttal. 2. Every change lists its reason and the affected requirements and test questions. |
| Due Date: | 09/12/2026 |
| Stakeholders: | Project Review Committee; Quality Team; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D14: Pilot evaluation report |
|---|---|
| Description: | Results of the pilot for Objectives 1, 3, 4 and 5. |
| Acceptance Criteria: | 1. Median time of the 10 pilot participants on the 10 timed questions, compared with D1 (Objective 1 target: at most half). 2. Number of participants who would use the assistant again (target: at least 7 of 10). 3. Number of test answers whose legal status matches the document inventory (target: at least 29 of 30). 4. Number of out-of-scope and case-assessment questions declined with a referral (target: at least 9 of 10). 5. No personal data of participants is stored. |
| Due Date: | 23/12/2026 |
| Stakeholders: | Product Owner; AI customer; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D15: Release candidate |
|---|---|
| Description: | Final version of the assistant shown at the final presentation. |
| Acceptance Criteria: | 1. Every acceptance criterion of user stories US-1 to US-7 passes on the evaluation set. 2. Every defect found in the pilot is fixed or listed with a reason. 3. The live demo runs from question to cited answer without errors. |
| Due Date: | 30/12/2026 |
| Stakeholders: | AI users: public institution staff and AI-policy researchers; AI customer |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D16: Final report |
|---|---|
| Description: | Summary of the project's results against its objectives. |
| Acceptance Criteria: | 1. Each objective (1–5) is reported with its target and measured result. 2. Each reported number links to its source (D14, D11 or a Weights & Biases run). 3. Lessons learned are listed. |
| Due Date: | 30/12/2026 |
| Stakeholders: | Project Review Committee; AI customer |
| Approving Stakeholder(s): | Product Owner |
