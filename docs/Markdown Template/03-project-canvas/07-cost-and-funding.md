# Cost & Funding

This page shows what the project consumes and where it comes from. Human effort is counted in person-hours; cloud use is counted in US dollars of the Google Cloud credit. Rows 1–16 cost every in-scope row of [Major Activities](04-major-activities.md) and every deliverable D1–D11 in [Deliverables](05-deliverables.md); rows 17–24 cost every resource in [Facilities & Resources](09-facilities-and-resources.md). Story points from poker planning are used to size the work of each sprint in Jira; they are not converted to person-hours here.

**Budget:** $100 of Google Cloud credits (fixed, per project). This is the same statement as in the [Project Executive Summary](01-project-executive-summary.md) and constraint C-09 in [Assumptions & Constraints](03-assumptions-and-constraints.md).

## 1. Initial Cost Estimate

### Human effort

| # | Item | Type (One-time/Ongoing) | Estimated Cost | Notes |
|---|---|---|---|---|
| 1 | Charter v1, user stories and User Story Map ([Major Activities](04-major-activities.md) rows 1, 3; D1) | One-time | 64 person-hours | 4 members × 8 h × 2 weeks. Sprint 1. Owner: Muhammed Batuhan Tezcan. |
| 2 | Evaluation set v1 ([Major Activities](04-major-activities.md) row 4; D2) | One-time | 30 person-hours | 40 questions × 30 min = 20 h; second-member check, 40 × 15 min = 10 h. Sprints 1–2. Owner: Elif Yeşim Koçoğlu. |
| 3 | User sessions and default-state measurement ([Major Activities](04-major-activities.md) row 5; D3) | One-time | 20 person-hours | Preparation 10 h; 10 participants × 1 h = 10 h. Sprint 2. Owner: Muhammed Batuhan Tezcan. |
| 4 | Learning spikes and System Architecture Design Document ([Major Activities](04-major-activities.md) row 6) | One-time | 30 person-hours | 6 spikes × 4 h = 24 h; design document 6 h. Sprints 1–2. Owner: Deniz Şenkutlu. |
| 5 | Document collection, inventory, extraction and Dataset Report ([Major Activities](04-major-activities.md) rows 7, 8; D4) | One-time | 32 person-hours | 8 documents × 2 h = 16 h; manual extraction of D04 and D05 because of C-02, 8 h; Dataset Report, 8 h. Sprints 1–2. Owner: Utku Uçar. |
| 6 | Chunking, embedding and indexing with metadata ([Major Activities](04-major-activities.md) row 9) | One-time | 16 person-hours | 4 document types × 3 h = 12 h; index build and check, 4 h. Sprint 2. Owner: Elif Yeşim Koçoğlu. |
| 7 | Retrieval, answer generation, decline rule and personal-data masking ([Major Activities](04-major-activities.md) rows 10, 11, 13) | One-time | 40 person-hours | Retrieval and answers, 24 h; decline rule because of C-06, 8 h; personal-data masking because of C-11, 8 h. Sprints 2–3. Owners: Deniz Şenkutlu and Elif Yeşim Koçoğlu. |
| 8 | Web chat page ([Major Activities](04-major-activities.md) row 12; D5) | One-time | 20 person-hours | Page, 16 h; personal-data notice and check because of C-08 and C-11, 4 h. Sprint 2. Owner: Utku Uçar. |
| 9 | Baseline run, experiments and MVP evaluation ([Major Activities](04-major-activities.md) rows 14, 15; D5, D7) | One-time | 36 person-hours | Baseline run, 6 h; 3 experiments × 4 h = 12 h; 30 answers × 2 judges × 10 min = 10 h; report, 8 h. Sprints 2–3. Owner: Elif Yeşim Koçoğlu. |
| 10 | Google Cloud deployment and beta release ([Major Activities](04-major-activities.md) row 17; D8) | One-time | 16 person-hours | Set-up and deployment because of C-07, 10 h; access test, 6 h. Sprint 3. Owner: Elif Yeşim Koçoğlu. |
| 11 | Pilot evaluation ([Major Activities](04-major-activities.md) row 16; D9) | One-time | 24 person-hours | 10 participants × 1 h = 10 h; review of the results, 8 h; report, 6 h. Sprint 4. Owner: Muhammed Batuhan Tezcan. |
| 12 | Release candidate, pilot defect fixes and final demo ([Major Activities](04-major-activities.md) rows 18, 19; D10) | One-time | 24 person-hours | Defect fixes, 16 h; demo preparation, 8 h. Sprint 4. Owner: Muhammed Batuhan Tezcan. |
| 13 | Charter v2 and final report ([Major Activities](04-major-activities.md) row 22; D6, D11) | One-time | 20 person-hours | Charter v2, 8 h (Sprint 2); final report, 12 h (Sprint 4). Owner: Muhammed Batuhan Tezcan. |
| 14 | Project management and Scrum events ([Major Activities](04-major-activities.md) row 24) | Ongoing | 56 person-hours | Scrum events, 2.5 h × 4 members × 4 sprints = 40 h; pull request reviews because of C-13, 1 h × 4 members × 4 sprints = 16 h. Sprints 1–4. Owner: Deniz Şenkutlu. |
| 15 | Source check and spending tracking ([Major Activities](04-major-activities.md) rows 19, 20) | Ongoing | 8 person-hours | 2 h × 4 sprint starts; continues after deployment [1]. Sprints 1–4. Owners: Deniz Şenkutlu (sources) and Elif Yeşim Koçoğlu (spending). |
| 16 | Shut down cloud resources and delete logs ([Major Activities](04-major-activities.md) row 23) | One-time | 2 person-hours | Once, after the final demo on 30/12/2026. Owner: Elif Yeşim Koçoğlu. |
| | **Total effort** | | **438 person-hours** | Within the team capacity of 440 to 660 person-hours: 4 members × 10 to 15 h per week × 11 weeks (A-07, C-12). |

### Material and financial resources

The cloud figures are planned on the GPU option in [Facilities & Resources](09-facilities-and-resources.md) row 3, the more expensive of the model options still open. Prices are on-demand rates for us-central1 [2, 3].

| # | Item | Type (One-time/Ongoing) | Estimated Cost | Notes |
|---|---|---|---|---|
| 17 | GPU virtual machine for spikes, development and evaluation runs ([Facilities & Resources](09-facilities-and-resources.md) row 3; rows 4, 6, 7, 9 above) | Ongoing | $38 of the credit | 70 GPU-hours × $0.54 per hour (T4 GPU $0.35 [2] + machine $0.19 [3]); no model is trained (C-05), so there is no training compute. Sprints 2–3. Owner: Elif Yeşim Koçoğlu. |
| 18 | GPU virtual machine for the beta, the pilot and the final demo ([Facilities & Resources](09-facilities-and-resources.md) rows 3, 11; D8, D9, D10) | Ongoing | $27 of the credit | 50 GPU-hours × $0.54 per hour: 10 pilot days × 4 h = 40 h, plus 10 h for the release candidate and the demo. Sprints 3–4. Owner: Elif Yeşim Koçoğlu. |
| 19 | Disks and the Cloud Storage bucket ([Facilities & Resources](09-facilities-and-resources.md) rows 3, 8) | Ongoing | $5 of the credit | Under 1 GB of documents and index snapshots at $0.022 per GB-month [4], plus the machine's disk for about 8 weeks. Sprints 2–4. Owners: Utku Uçar and Elif Yeşim Koçoğlu. |
| 20 | Web page hosting ([Facilities & Resources](09-facilities-and-resources.md) row 11) | Ongoing | $0 | Use by 10 pilot participants and the team stays within the Cloud Run free tier [5]. Sprints 3–4. Owner: Elif Yeşim Koçoğlu. |
| 21 | Credit reserve ([Facilities & Resources](09-facilities-and-resources.md) row 2) | One-time | $30 of the credit | Not planned for use (A-06); spending is watched against the trigger of R-06 in [Risks](11-risks.md). Sprints 1–4. Owner: Elif Yeşim Koçoğlu. |
| | **Total Google Cloud credit** | | **$70 planned + $30 reserve = $100** | Matches the budget statement above. |
| 22 | Managed vector database, free plan ([Facilities & Resources](09-facilities-and-resources.md) row 6) | Ongoing | $0 | Free cluster: 1 GB RAM, 4 GB disk; suspended after 1 week unused [6], so a snapshot is kept in the bucket (row 19). Sprints 2–4. Owner: Elif Yeşim Koçoğlu. |
| 23 | Weights & Biases, free plan ([Facilities & Resources](09-facilities-and-resources.md) row 10) | Ongoing | $0 | Free plan: up to 5 seats and 5 GB per month [7]; the team has 4 members; used because of C-13. Sprints 2–4. Owner: Elif Yeşim Koçoğlu. |
| 24 | Resources at no charge ([Facilities & Resources](09-facilities-and-resources.md) rows 1, 4, 5, 7, 9) | One-time | $0 | Laptops owned by the members; open-weight models with no licence fee; documents published free of charge (A-05); GitHub, Jira and Confluence under the team's existing plans. Sprints 1–4. Owners: Utku Uçar (documents) and Muhammed Batuhan Tezcan (tools). |

## 2. Source of Funding

| Resource type | Source | Amount |
|---|---|---|
| Human | The four team members: Muhammed Batuhan Tezcan, Elif Yeşim Koçoğlu, Utku Uçar and Deniz Şenkutlu | 438 person-hours planned, within 440 to 660 available |
| Material (cloud) | Google Cloud education credit for DI 502 | $100 fixed; $70 planned, $30 reserve |
| Material (other services) | Free plans of Qdrant Cloud and Weights & Biases; GitHub, Jira and Confluence under the plans already available to the team | $0 |
| Data | Official documents published free of charge by the public bodies listed in the [Project Executive Summary](01-project-executive-summary.md) | $0 |

All human-resource effort will be contributed in-kind by the student project team, with no paid labour or external contractors. Each member has committed to 10 to 15 hours per week until 30/12/2026 (A-07), and hours worked are reported at each sprint review. There is no sponsor and no other source of money.

## References

[1] ISO/IEC JTC 1/SC 42, *ISO/IEC 5338:2023 Information technology — Artificial intelligence — AI system life cycle processes*, 1st ed. Geneva, Switzerland: ISO and IEC, Dec. 2023.

[2] Google Cloud, "GPU pricing." [Online]. Available: https://cloud.google.com/products/compute/gpus-pricing. Accessed: 24 Oct. 2026.

[3] Economize, "n1-standard-4 pricing, Google Cloud Compute Engine." [Online]. Available: https://www.economize.cloud/resources/gcp/pricing/compute-engine/n1-standard-4/. Accessed: 24 Oct. 2026.

[4] CloudZero, "GCP storage pricing." [Online]. Available: https://www.cloudzero.com/blog/gcp-storage-pricing. Accessed: 24 Oct. 2026.

[5] Google Cloud, "Cloud Run pricing." [Online]. Available: https://cloud.google.com/run/pricing. Accessed: 24 Oct. 2026.

[6] Qdrant, "Create a cluster." Qdrant Cloud documentation. [Online]. Available: https://qdrant.tech/documentation/cloud/create-cluster/. Accessed: 24 Oct. 2026.

[7] CoreWeave, "Weights & Biases pricing." [Online]. Available: https://coreweave.com/forge-pricing. Accessed: 24 Oct. 2026.
