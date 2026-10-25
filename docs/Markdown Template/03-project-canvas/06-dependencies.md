# Dependencies

Each row says what must happen first, what waits for it, the date by which we check that the first step is done, and whom to contact if it is late. The chance that a dependency fails is recorded as a risk in [Risks](11-risks.md) and linked here.

| # | Dependency Description | Critical Date | Contact |
|---|---|---|---|
| 1 | Sprint 2 work cannot start until Project Charter v1 (D1) is approved by the Project Review Committee (course instructors). | 28/10/2026 | Muhammed Batuhan Tezcan (Product Owner) |
| 2 | Indexing cannot start until the terms of use of each source website are checked and recorded in the Third-Party Dataset Register (A-05). Supplier: the public bodies that publish the documents. Linked risk: R-05. | 28/10/2026 | Utku Uçar (Data Scientist) |
| 3 | Splitting and indexing the documents cannot start until every document is downloaded, converted to text and listed in the document inventory with its legal status and download date. Linked risk: R-08. | 04/11/2026 | Utku Uçar (Data Scientist) |
| 4 | Building the answer pipeline cannot start until the Google Cloud project is set up under the $100 credit with a budget alert, and the embedding model and language model chosen in the spikes run from it. Supplier: Google Cloud. Linked risk: R-06. | 04/11/2026 | Elif Yeşim Koçoğlu (Data Scientist) |
| 5 | The baseline run (part of D5) cannot start until evaluation set v1 (D2) is final and committed, and the Weights & Biases workspace is ready (C-13). Linked risk: R-02. | 11/11/2026 | Elif Yeşim Koçoğlu (Data Scientist) |
| 6 | The default-state test (D3) cannot start until the 6 outside participants have confirmed in writing and each team member's persona is checked (A-01). Linked risk: R-01. | 04/11/2026 | Deniz Şenkutlu (Data Scientist) |
| 7 | Charter v2 (D6) cannot be finished until the Quality Team sends its Sprint 2 review of the charter. | 11/11/2026 | Muhammed Batuhan Tezcan (Product Owner) |
| 8 | Beta work (Sprint 3) cannot start until the Product Owner records a "go" at checkpoint M6, based on the alpha (D5) and its baseline results. | 20/11/2026 | Muhammed Batuhan Tezcan (Product Owner) |
| 9 | The beta (D8) cannot be given to the pilot participants until the assistant runs on Google Cloud and opens in a browser outside the team's computers (C-07). Supplier: Google Cloud. Linked risk: R-06. | 02/12/2026 | Elif Yeşim Koçoğlu (Data Scientist) |
| 10 | Release-candidate work (Sprint 4) cannot start until the Product Owner records a "go" at checkpoint M9, based on the MVP evaluation (D7) and first beta use (D8). | 11/12/2026 | Muhammed Batuhan Tezcan (Product Owner) |
| 11 | The Objective 1 result in the pilot evaluation (D9) cannot be calculated until the default-state median time (D3) is recorded for the same 10 timed questions. | 18/11/2026 | Deniz Şenkutlu (Data Scientist) |
| 12 | The release candidate (D10) cannot be released without an up-to-date `README.md` and `ai-bom.yaml` that list the models, documents, prompts, settings and evaluation set it uses. | 23/12/2026 | Deniz Şenkutlu (Scrum Master) |
| 13 | The beta (D8) cannot be given to the pilot participants until personal data in questions is masked before anything is logged (C-11). Linked risk: R-10. | 02/12/2026 | Deniz Şenkutlu (Data Scientist) |
| 14 | Indexing cannot start until a free-plan account is set up with the vector database provider and its storage and request limits are recorded. Supplier: Qdrant Cloud or Pinecone, chosen in the spikes. | 04/11/2026 | Elif Yeşim Koçoğlu (Data Scientist) |
| 15 | The baseline run (part of D5) cannot start until the whole document collection is split and indexed. | 11/11/2026 | Elif Yeşim Koçoğlu (Data Scientist) |
| 16 | The final report (D11) cannot be completed until the pilot evaluation results (D9) are recorded. | 23/12/2026 | Muhammed Batuhan Tezcan (Product Owner) |
| 17 | The default-state test (D3) cannot start until the 10 timed questions are picked at random from evaluation set v1 (D2). | 11/11/2026 | Deniz Şenkutlu (Data Scientist) |
