# Dependencies

A dependency says that **A must happen before B can start**, and **whom to contact if there is a problem with A**.

"Pretrained models are needed for the chatbot" is a weak entry. It names neither the item nor the work that waits for it, and gives nobody to call. A strong entry names both sides, a date and a person: "Retrieval evaluation (Sprint 3) cannot start until the evaluation Q&A set exists. Check by: end of Sprint 2. Contact: the Data Scientist who builds the Q&A set." (illustrative only)

## Kinds of dependency

List dependencies such as these:

| Kind | Example (illustrative only) |
|---|---|
| Predecessor/successor relationships among tasks within this project | The chunked and embedded index must exist before retrieval evaluation starts. |
| Predecessor/successor relationships with another project (e.g., partnerships) | A partner group's labelled data must be delivered before fine-tuning. |
| Related projects that require a deliverable from this project | Another team's dashboard needs this project's API. |
| Deliverables this project requires from a related project | This project needs another project's evaluation set. |
| Products, services or results that must be released together with this project's output | The user guide must be released with the MVP. |

Dependencies on outside organizations also count. A project can depend on other organizations to provide infrastructure or a capability, such as a cloud setup [1]. Acquiring data from outside the project brings its own dependency and continuity issues [1]. In ISO/IEC 5339 terms, such a supplier is often an AI partner or a data provider [2]. You do not need to write ISO process names or numbers in the charter.

The life cycle itself creates dependencies: a piece of functionality is implemented before it can be verified, and verified before it is deployed [1].

## Fields

| Field | What it means | Question it answers |
|---|---|---|
| **Dependency Description** | What A and B are | What waits for what? |
| **Critical Date** | The latest date by which you check that A exists | By when must we confirm A is in place? |
| **Contact** | The person to reach if there is a problem with A | Whom do we call if A is late or broken? |

## Rules

1. Every row names both A (what must happen first) and B (what waits for it).
2. Every row has a Critical Date.
3. The Critical Date is no later than the planned start of B.
4. Every row has a Contact who is a named team member.
5. A row describes a relationship, not a task. "Prepare the final presentation" is a task; it goes in [Major Activities](03-project-canvas_v2/04-major-activities.md).
6. A row for an outside supplier names the supplier [1].
7. The chance that A fails or changes is a risk. Register it in [Risks](03-project-canvas_v2/11-risks.md) and write this row's number in its **Linked to** field.

## Test to apply to your draft

Fill in this sentence for each row:

> **B** cannot start until **A** has happened. We check that A exists by **date**. If there is a problem with A, we contact **person**.

If you cannot fill all four slots, the row is not ready.

## Not this / this

The left column shows weak rows, each tagged with the rule it breaks. The corrected version fixes only that defect.

| Not this | Rule broken | This (illustrative only) |
|---|---|---|
| "Necessary documentation updates and preparation of the final presentation must be done." | A task, not a relationship (rule 5) | Move it to [Major Activities](03-project-canvas_v2/04-major-activities.md). If something waits for it, write that link: "The final demo cannot start until the slides are reviewed. Check by: one week before the demo." |
| "Pretrained embedding models and an open-source LLM are needed to implement the chatbot." | A is not named precisely, and no supplier is named (rules 1, 6) | "Pipeline implementation cannot start until the chosen embedding model and LLM are downloaded from the model hub and run in the team environment. Check by: end of Sprint 2. Contact: the Data Scientist responsible for the environment." |

Two good examples:

- "Approval of the project charter before starting Sprint 2." The successor (Sprint 2 work) and the approver are clear. The contact is the course instructor, who sits on the Project Review Committee.
- "The RAG pipeline must be implemented before the chatbot is connected to the user interface." A clear predecessor and successor.

Why the dates matter: dependencies cause wait times. A Critical Date gives you a point at which to check, and a Contact gives you someone to chase.

## Patterns to use if you are stuck

- **Task chain inside the team:** "Evaluation of X cannot start until the index for X is built."
- **Data handoff:** "Fine-tuning cannot start until the labelled set is delivered by the data provider." [2]
- **External service:** "Integration tests cannot start until the API key for the external service is issued." [1]
- **Approval gate:** "Sprint 2 work cannot start until the charter is approved by the Project Review Committee."
- **Release together:** "The MVP cannot be released without the user guide."

## What doesn't belong here

- **Tasks** themselves go in [Major Activities](03-project-canvas_v2/04-major-activities.md).
- **Milestone dates** go in [Milestones](03-project-canvas_v2/02-milestones.md).
- **What happens if A fails** (mitigation, contingency) goes in [Risks](03-project-canvas_v2/11-risks.md).
- **The resource itself** (tool, account, compute, its owner and status) goes in [Facilities & Resources](03-project-canvas_v2/09-facilities-and-resources.md). Add a row here only when B is waiting for someone to deliver that resource.
- **Fixed limits**, such as a quota, go in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) as constraints.

## Dependencies

| # | Dependency Description | Critical Date | Contact |
|---|---|---|---|
| 1 | | | |

## Example (illustrative only)

Scenario: a legal research assistant. Names and dates are illustrative.

| # | Dependency Description | Critical Date | Contact |
|---|---|---|---|
| 1 | Sprint 2 work cannot start until the Project Charter v1 is approved by the Project Review Committee. | 28/10/2026 | Named team member who submits the charter |
| 2 | Indexing cannot start until the document set is delivered by the external data provider under the agreed licence. | 28/10/2026 | Business Analyst who holds the contact with the data provider (named member) |
| 3 | Retrieval evaluation cannot start until the evaluation Q&A set is generated and spot-checked. | 18/11/2026 | Data Scientist who builds the Q&A set (named member) |
| 4 | Staging deployment cannot start until the cloud project is created under the university credit. | 02/12/2026 | Data Scientist responsible for infrastructure (named member) |

Row 2 has a matching risk in [Risks](03-project-canvas_v2/11-risks.md): "The data provider delivers the document set more than one week late" (Linked to: [Dependencies](03-project-canvas_v2/06-dependencies.md) row 2).

## Checklist before submitting

- [ ] Every row names both A and B (rule 1)
- [ ] Every row has a Critical Date (rule 2)
- [ ] No Critical Date is later than the planned start of B (rule 3)
- [ ] Every row has one named Contact (rule 4)
- [ ] No row is a bare task (rule 5)
- [ ] Every row for an outside supplier names the supplier (rule 6)
- [ ] Every dependency that might fail has a risk in [Risks](03-project-canvas_v2/11-risks.md) that links back to it (rule 7)

---

## References

[1] ISO/IEC JTC 1/SC 42, *ISO/IEC 5338:2023 Information technology — Artificial intelligence — AI system life cycle processes*, 1st ed. Geneva, Switzerland: International Organization for Standardization and International Electrotechnical Commission, Dec. 2023. UK implementation: BS ISO/IEC 5338:2023, London, UK: BSI Standards Limited, 2024.

[2] ISO/IEC JTC 1/SC 42, *ISO/IEC 5339:2024 Information technology — Artificial intelligence — Guidance for AI applications*, 1st ed. Geneva, Switzerland: International Organization for Standardization and International Electrotechnical Commission, Jan. 2024. UK implementation: BS ISO/IEC 5339:2024, London, UK: BSI Standards Limited, 2024.
