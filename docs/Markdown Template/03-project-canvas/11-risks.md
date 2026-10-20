# Risks

This page records the strategic risks identified at the start of the project. Each assumption in [Assumptions & Constraints](03-assumptions-and-constraints.md) has its flip-side risk here with the same number (A-01 ↔ R-01 … A-07 ↔ R-07). Risks R-08 to R-10 come from constraints, R-11 from a dependency on the publishers' websites, and R-12 to R-15 are technical risks in the data and model pipeline. Probability is the residual value after mitigation. Owners and their roles are listed in [Project Organization](08-project-organization.md); objectives and success criteria are in the [Project Executive Summary](01-project-executive-summary.md), and deliverables D1–D11 in [Deliverables](05-deliverables.md).

## Risk register

| # | Layer | Risk (event) | When / where | Probability | Impact | Score | Owner | Linked to |
|---|---|---|---|---|---|---|---|---|
| R-01 | People / process | Fewer than 6 people from outside the team confirm as pilot participants by 04/11/2026, or fewer than 6 take part in the default-state test (by 18/11/2026), the beta (09/12/2026) or the pilot test (23/12/2026). | Sprints 2–4; development and after deployment | 3 (outside participants are unpaid and must attend three sessions over about six weeks; public institution staff have limited time) | 4 (the success criteria of Objectives 1 and 3 count 10 participants; D3, D8 and D9 require them) | 12 (High) | Muhammed Batuhan Tezcan (Product Owner) | A-01; [Dependencies](06-dependencies.md) 6; mitigated by preparing the user sessions ([Major Activities](04-major-activities.md) row 5) |
| R-02 | People / process | Fewer than 10 proxy questions pass the second-member check on 28/10/2026, because they repeat the documents' wording instead of the users' tasks. | Sprint 1; development | 2 (members write the questions from their persona's tasks before re-reading the documents; copied questions are rewritten during the check) | 4 (an evaluation set phrased like the documents overstates the Objective 2 results reported in D7) | 8 (Medium) | Elif Yeşim Koçoğlu (Data Scientist) | A-02; [Dependencies](06-dependencies.md) 5; mitigated by the second-member check of the evaluation set ([Major Activities](04-major-activities.md) row 4) |
| R-03 | Data | A corpus document is amended, replaced or repealed before 30/12/2026, so some answers describe outdated rules. | Sprints 1–4; development and after deployment (model decay) | 2 (the Action Plan runs to 2030 [1, 2]; guidance and circulars can still be issued at any time) | 3 (answers to the affected questions become partly wrong; the collection date shown to users (Feature 6) limits the effect) | 6 (Medium) | Deniz Şenkutlu (Data Engineer) | A-03; C-01, C-03; mitigated by the sprint-start check of the sources ([Major Activities](04-major-activities.md) row 20) and by showing the collection date |
| R-04 | Data | In the passage check, fewer than 9 of 10 randomly chosen passages match the source PDF in wording and numbers (broken Turkish characters, merged columns or lost table structure). | Sprints 1–2; development | 3 (one corpus document, D04 in the document inventory, already could not be extracted automatically) | 4 (D4 acceptance criterion 5; wrong text leads to wrong citations under Objective 2) | 12 (High) | Utku Uçar (Data Engineer) | A-04; C-02; [Dependencies](06-dependencies.md) 3; mitigated by the 10-passage spot check ([Major Activities](04-major-activities.md) row 8) |
| R-05 | People / process | The terms of use of a publisher's website forbid storing or quoting one of the corpus documents. | Sprint 1; development | 1 (all documents are official publications offered free of charge; FSEK Art. 31 covers laws and circulars) | 4 (removing a document breaks D2 acceptance criterion 3 and D4 acceptance criterion 2) | 4 (Low) | Utku Uçar (Data Engineer) | A-05; [Dependencies](06-dependencies.md) 2; mitigated by checking the terms of use before indexing ([Major Activities](04-major-activities.md) row 7) |
| R-06 | Infrastructure | Google Cloud spending reaches $70 before 09/12/2026, so the $100 credit would run out before 30/12/2026. | Sprints 2–4; development and after deployment | 2 (one-off indexing of the corpus, a 40-question evaluation set and about 3 weeks of hosting; the cost estimate is made in Sprint 1) | 5 (an overrun is above 20% of the budget; the credit is fixed, so the assistant would stop running, and D8 acceptance criterion 5 requires spending below $100) | 10 (High) | Elif Yeşim Koçoğlu (Data Scientist) | A-06; C-07, C-09; [Dependencies](06-dependencies.md) 4, 9; mitigated by the billing budget alert and spending tracking ([Major Activities](04-major-activities.md) rows 17, 19) |
| R-07 | People / process | A team member leaves the course, is unavailable for more than 2 weeks, or spends fewer than 10 hours per week on the project in two sprints in a row. | Sprints 1–4; development | 2 (all four members are enrolled, hold an assigned role in Sprint 1 and agreed on 10 to 15 hours per week) | 3 (a quarter of the team's capacity and one of the four proxy participants are lost; if the only Data Scientist leaves, the evaluation work for D7 and D9 slips) | 6 (Medium) | Muhammed Batuhan Tezcan (Product Owner) | A-07; C-12; mitigated by pull request reviews, which give every piece of work a second member who knows it ([Major Activities](04-major-activities.md) row 24) |
| R-08 | Model | At the MVP evaluation on 09/12/2026, fewer than 24 of 30 in-scope answers are correct, or fewer than 24 of 30 cite a document and section that support them. | Sprints 2–3; development | 3 (the baseline is run only in Sprint 2; reported Turkish RAG results depend strongly on chunking and retrieval choices [10]) | 4 (Objective 2 success criterion; D7 acceptance criterion 2) | 12 (High) | Elif Yeşim Koçoğlu (Data Scientist) | C-04, C-05; mitigated by the baseline run and experiments ([Major Activities](04-major-activities.md) row 14) |
| R-09 | Model | The assistant answers out-of-scope or compliance-judgement questions instead of giving the fixed notice that refers the user to the Millî Teknoloji ve Yapay Zekâ Genel Müdürlüğü: fewer than 8 of 10 such test questions receive the notice. | Sprints 2–4; development and after deployment | 2 (language models tend to answer rather than decline; the fixed-notice rule and the 10 out-of-scope test questions in D2 reduce this) | 4 (Objective 5 success criterion) | 8 (Medium) | Elif Yeşim Koçoğlu (Data Scientist) | C-06; mitigated by the decline rule and the out-of-scope tests ([Major Activities](04-major-activities.md) row 11) |
| R-10 | People / process | Users type personal data (names, ID numbers, institution details) into questions, and it ends up in logs, evaluation files or the index. | Sprints 3–4; after deployment | 2 (the page has no personal-data field, but questions are free text) | 4 (breaks C-11 and Law No. 6698; D9 acceptance criterion 3) | 8 (Medium) | Deniz Şenkutlu (Data Engineer) | C-08, C-11; mitigated by masking personal data before logging ([Major Activities](04-major-activities.md) row 13) |
| R-11 | Integration | The official URL of a corpus document changes or goes offline, so a citation link in the answers is broken. | Sprints 2–4; development and after deployment | 1 (every official URL is checked before each release, and the download date is recorded for each document) | 4 (D5 acceptance criterion 2; users cannot open the original under Feature 2) | 4 (Low) | Utku Uçar (Data Engineer) | [Dependencies](06-dependencies.md) 2 (the public bodies that publish the corpus documents); the official URL of each document is recorded in the inventory ([Major Activities](04-major-activities.md) row 7) |
| R-12 | Data | Splitting the documents into passages cuts articles, tables or Tedbir entries apart: in a check of 20 randomly chosen passages, more than 2 have no article or section number or end in the middle of a provision. | Sprints 1–2; development | 2 (article and section numbers are stored with each passage, and the splitting is tested on a sample before the full corpus is indexed) | 4 (wrong or missing citations threaten the Objective 2 citation criterion, 24 of 30) | 8 (Medium) | Utku Uçar (Data Engineer) | C-02, C-05; mitigated by storing the article or section with each chunk ([Major Activities](04-major-activities.md) row 9) |
| R-13 | Model | The legal status shown for a cited source differs from the document inventory in more than 3 of 30 test answers at the pilot evaluation (23/12/2026). | Sprints 2–4; development and after deployment | 2 (labels are taken from the document inventory, not generated by the model; answers that cite several documents are the main source of error) | 4 (Objective 4 success criterion, 27 of 30; Feature 3) | 8 (Medium) | Deniz Şenkutlu (Data Engineer) | Objective 4; mitigated by taking labels from the inventory and by the legal-status review ([Major Activities](04-major-activities.md) rows 10, 16) |
| R-14 | Infrastructure | In the beta (09/12/2026), the median time from question to answer is above 20 seconds, so the timed task test cannot show that the answer time is halved. | Sprints 3–4; after deployment | 2 (the corpus is small, and the time per answer is measured in the alpha, D5) | 4 (Objective 1 success criterion) | 8 (Medium) | Elif Yeşim Koçoğlu (Data Scientist) | C-07; mitigated by recording the answer time in the evaluation runs ([Major Activities](04-major-activities.md) row 14) |
| R-15 | Integration | The provider of the language model changes its version, price or usage limits during the project, so answers or costs change between evaluation runs. | Sprints 2–4; development and after deployment | 2 (the model version is fixed in `config/rag.yaml`, and the provider's notices are checked at each sprint start) | 3 (evaluation runs must be repeated, about 1 week; spending may rise, see R-06) | 6 (Medium) | Elif Yeşim Koçoğlu (Data Scientist) | C-05; the model version is fixed in `config/rag.yaml` ([Major Activities](04-major-activities.md) row 9) |

**Model decay after deployment.** The corpus is a fixed snapshot (C-03), so the assistant decays when the rules change (R-03). Maintenance is triggered when the sprint-start check finds that a corpus document has been amended, replaced or repealed. The affected document is then downloaded again, re-indexed, and the collection date shown to users is updated.

## Risk details

Detail blocks are given for every risk with a score of 10 or more.

### Risk R-01: Outside pilot participants not available

| Field | Content |
|---|---|
| **Risk (event)** | Fewer than 6 people from outside the team confirm as pilot participants by 04/11/2026, or fewer than 6 take part in the default-state test (by 18/11/2026), the beta (09/12/2026) or the pilot test (23/12/2026). |
| **Linked to** | A-01 in [Assumptions & Constraints](03-assumptions-and-constraints.md) |
| **Cause** | The outside participants are unpaid; public institution staff have limited time; three sessions are spread over about six weeks. |
| **When / where** | Sprints 2–4; development and after deployment |
| **Mitigation** | Recruit 8 outside candidates (2 in reserve); cap the number of pop-up questions asked in each session (cap: **[TBC]**); allow online sessions; fix all three session dates at recruitment. Results of the four team members, who act as proxies and already know the documents, are reported separately from those of the outside participants in D3 and D9. |
| **Probability (basis)** | 3: the outside participants are beyond the team's control, and the default-state test is due in Sprint 2. |
| **Impact (basis)** | 4: the success criteria of Objectives 1 and 3 count 10 participants, and D3, D8 and D9 require them. |
| **Score** | 12 (High) |
| **Trigger** | Fewer than 6 written confirmations from outside participants on 04/11/2026, or fewer than 5 outside participants at the beta on 09/12/2026. |
| **Contingency plan (B plan)** | Fill the gap with AI-policy graduate students (the secondary user group, stakeholder 2). If there are still fewer than 5 outside participants, run the sessions with those available and the four team members, report Objectives 1 and 3 on the actual number, and inform the Project Review Committee in writing at the next sprint review (renegotiate the target). |
| **Owner** | Muhammed Batuhan Tezcan, Product Owner |
| **Schedule effect** | About 1 week |

### Risk R-04: Text extraction errors

| Field | Content |
|---|---|
| **Risk (event)** | In the passage check, fewer than 9 of 10 randomly chosen passages match the source PDF in wording and numbers. |
| **Linked to** | A-04 and C-02 in [Assumptions & Constraints](03-assumptions-and-constraints.md) |
| **Cause** | The corpus PDFs are produced by different institutions; Turkish characters (ı, ğ, ş, İ), multi-column pages and tables are often extracted incorrectly. |
| **When / where** | Sprints 1–2; development |
| **Mitigation** | Spot check of 10 passages in a Sprint 1 learning spike; compare two extraction tools; check Turkish characters automatically after extraction. |
| **Probability (basis)** | 3: one corpus document (D04 in the document inventory) already could not be extracted automatically. |
| **Impact (basis)** | 4: D4 acceptance criterion 5; wrong text leads to wrong citations under Objective 2. |
| **Score** | 12 (High) |
| **Trigger** | Fewer than 9 of 10 passages match in the spot check on 28/10/2026 or in the Dataset Report (D4) check on 18/11/2026. |
| **Contingency plan (B plan)** | Narrow the scope: for each failing document, keep only the sections that pass the check or are typed in by hand, drop the rest from the corpus, and record this in the Dataset Report (D4). Evaluation questions whose gold source is dropped are replaced with the Product Owner's approval before the baseline run. |
| **Owner** | Utku Uçar, Data Engineer |
| **Schedule effect** | About 1–2 weeks |

### Risk R-06: Cloud credit runs out

| Field | Content |
|---|---|
| **Risk (event)** | Google Cloud spending reaches $70 before 09/12/2026, so the $100 credit would run out before 30/12/2026. |
| **Linked to** | A-06, C-07 and C-09 in [Assumptions & Constraints](03-assumptions-and-constraints.md) |
| **Cause** | The cost of model calls and hosting is not known until the model and hosting choice is made in Sprint 1; repeated evaluation runs add up. |
| **When / where** | Sprints 2–4; development and after deployment |
| **Mitigation** | Billing budget alerts at $25, $50 and $70; the cost of each evaluation run is logged in Weights & Biases; the hosted page is stopped when not in use. |
| **Probability (basis)** | 2: the corpus is indexed once, the evaluation set has 40 questions, and hosting lasts about 3 weeks. |
| **Impact (basis)** | 5: an overrun is above 20% of the budget; the credit is fixed, so the assistant would stop running, and D8 acceptance criterion 5 requires spending below $100. |
| **Score** | 10 (High) |
| **Trigger** | The billing report shows $70 or more spent on any date before 09/12/2026. |
| **Contingency plan (B plan)** | Degrade gracefully: switch to a smaller, cheaper language model, run only the evaluation runs needed for D7 and D9, and keep the hosted page online only during the beta and pilot sessions. The Product Owner informs the Project Review Committee if an objective is affected. |
| **Owner** | Elif Yeşim Koçoğlu, Data Scientist |
| **Schedule effect** | About 1 week |

### Risk R-08: MVP correctness targets not met

| Field | Content |
|---|---|
| **Risk (event)** | At the MVP evaluation on 09/12/2026, fewer than 24 of 30 in-scope answers are correct, or fewer than 24 of 30 cite a document and section that support them. |
| **Linked to** | C-04 and C-05 in [Assumptions & Constraints](03-assumptions-and-constraints.md) |
| **Cause** | Turkish word forms make retrieval harder; the corpus contains long documents, and some questions combine several documents or are follow-ups. |
| **When / where** | Sprints 2–3; development |
| **Mitigation** | Baseline run with the Alpha prototype (D5) by 18/11/2026, leaving three weeks to improve; chunking and retrieval experiments tracked in Weights & Biases; article and section numbers stored with each passage. |
| **Probability (basis)** | 3: no baseline exists before Sprint 2, and reported Turkish RAG results depend strongly on chunking and retrieval choices [10]. |
| **Impact (basis)** | 4: Objective 2 success criterion and D7 acceptance criterion 2. |
| **Score** | 12 (High) |
| **Trigger** | Fewer than 20 of 30 in-scope answers correct in the baseline run (D5) on 18/11/2026, or results below 24 of 30 correct or 24 of 30 cited on 09/12/2026. |
| **Contingency plan (B plan)** | After the baseline: degrade gracefully by showing the retrieved passages with their citations instead of a generated answer when retrieval confidence is low. After the MVP evaluation: renegotiate the target with the Product Owner and the Project Review Committee, and report the measured values in the Final report (D11). |
| **Owner** | Elif Yeşim Koçoğlu, Data Scientist |
| **Schedule effect** | About 2 weeks |

## References

References [1]–[10] are listed in [Project Executive Summary](01-project-executive-summary.md).
