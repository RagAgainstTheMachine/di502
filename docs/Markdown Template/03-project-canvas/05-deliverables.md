# Deliverables

Identify and define the high-level deliverables required to achieve the project's objectives. A **deliverable** is a tangible artifact, product or result produced as a direct output of work. It fulfils a requirement.

Because this project follows Scrum, the charter itself is updated iteratively. Treat each version as a separate deliverable (e.g., "Project Charter v1" as Deliverable 1, "Project Charter v2" as Deliverable 2, and so on).

A weak deliverable cannot be checked. A strong one can. Write "Acceptance criteria: Recall@5 ≥ 0.70 on the 200-question test set", not "The model works well" (examples illustrative only).

## Two kinds of deliverable

Include both kinds.

| Kind | What it is | Examples |
|---|---|---|
| **Solution deliverable** | Part of the product or its technical documentation | Features, data dictionary, solution architecture report, Q&A Generation-Dataset, and the alpha, beta and release candidate builds (see [Release Plan](03-project-canvas_v2/10-release-plan.md)) |
| **Project-management deliverable** | Needed for review and approval | Charter document (each version), lessons learned register, data quality report, status dashboard, final report, exit report |

### Deliverables the course expects

- **Each charter version** as its own deliverable.
- **A Q&A Generation-Dataset** for evaluating the system. Say how you will make the generated questions diverse and representative. You can use an existing Q&A dataset from your domain if one exists.
- **Datasheets and model cards**, if you plan to deliver them, follow Mitchell et al. [1] and Gebru et al. [2], not Hugging Face or other formats.
  - Write a model card yourself only when you train or fine-tune a model. For a model used as-is, import the model card from its source or document the model in the AI SBOM.
  - If a dataset already has a datasheet at its source and you do no further preprocessing, a separate datasheet is not needed. A data quality report or a preprocessing report can be useful instead.

## How to fill in each deliverable

| Field | What it means | When it applies | Question it answers |
|---|---|---|---|
| **Project Deliverable #** | Number and name, e.g., "D3: Q&A Generation-Dataset v1" | Every block | Which deliverable is this? |
| **Description** | What the artifact is and what it contains | Every block | What do we hand over? |
| **Acceptance Criteria** | How quality and completion will be assessed. Each criterion must be measurable. | Every block | How do we know it is done and good enough? |
| **Due Date** | A calendar date (dd/mm/yyyy) inside a sprint (see [Release Plan](03-project-canvas_v2/10-release-plan.md)), aligned with the milestone it supports (see [Milestones](03-project-canvas_v2/02-milestones.md)) | Every block | When? |
| **Stakeholders** | Who the deliverable is **for**: the people or roles who will use or receive it | Every block | For whom? |
| **Approving Stakeholder(s)** | Who **signs off** on it. Use a named person or a role from [Project Organization](03-project-canvas_v2/08-project-organization.md), e.g., Product Owner or Project Review Committee. | Every block | Who says it is accepted? |

**Stakeholders and approvers are different fields.** Assign them carefully. For example, the MVP is developed for the customer, not for the project team. The customer may also be the approver: ISO/IEC 5339 describes the AI customer as consulted during verification and validation and during deployment [3], and ISO/IEC 5338 states that validation is ratified by stakeholders [4].

## Rules

Each rule is a condition you can check with yes or no.

1. The page includes both solution deliverables and project-management deliverables.
2. Each iteration of a document is a separate deliverable. (e.g. Project Charter, Question & Answer Dataset, Model Cards and so on)
3. Every block has all six fields filled.
4. Every acceptance criterion is measurable. It names what is checked and the pass condition: a number with a threshold, or a check with a single yes/no outcome.
5. No acceptance criterion uses an adjective without a number ("fast", "good", "clear", "complete").
6. The Stakeholders field names who the deliverable is for. A customer-facing deliverable, such as the MVP, does not list only the project team.
7. The Approving Stakeholder(s) field names a person or role who signs off.
8. Every due date is aligned with the milestone it supports in [Milestones](03-project-canvas_v2/02-milestones.md).
9. There is a Q&A Generation-Dataset deliverable whose acceptance criteria cover the diversity and representation of the questions.
10. Any model card written by the team is for a model the team trained or fine-tuned.
11. If an objective in [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) sets a target that is measured later (e.g., user satisfaction), a deliverable holds the result (e.g., the survey result).
12. Deliverables do not force a waterfall approach. For example, the product is delivered in several versions across sprints, not once at the end.

## Test: three questions for every acceptance criterion

1. **Could two people check it and agree?** If they could disagree, it is not measurable.
2. **Is there a number or a yes/no check instead of an adjective?** "Responses are fast" fails; "p95 latency ≤ 3 s on the test set" passes (illustrative).
3. **Has the approving stakeholder agreed to it?** ISO/IEC 5338 asks for explicit agreement on stakeholder requirements, including critical performance measures [4]. If the approver has not seen the criterion, it is not agreed.

## Not this / this

Each corrected entry fixes only the named defect. All examples are illustrative.

| Not this | This | Defect |
|---|---|---|
| MVP deliverable, Stakeholders: "Project team" | Stakeholders: "AI customer: the office that would use the assistant; AI users: its staff" | The MVP is developed for the customer, not the team |
| Final demo deliverable: "Quality meets goals (e.g., good accuracy and fast responses)" | "Accuracy and p95 latency meet the thresholds of objective 1 in [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) (e.g., accuracy ≥ 70%, p95 ≤ 10 s on the test set)" | Adjectives instead of measurable criteria |
| Documentation-card deliverables: "Each card must provide complete, clear, and reproducible documentation" | "Every section of the Mitchell et al. [1] template is filled; every reported metric links to an experiment card" | Not measurable |
| No Q&A dataset deliverable | Add "Q&A Generation-Dataset v1", with criteria on topic coverage and question types | A separate Q&A dataset deliverable is required |
| "Datasheet and Data Quality Report" for an external dataset used as-is that already has a datasheet at its source | "Data Quality Report v1" only, linking to the source's datasheet | A separate datasheet is not needed |
| One "Project Charter" deliverable and no later versions | "Project Charter v1" (Sprint 1) and "Project Charter v2" (Sprint 2) as separate deliverables | Each charter version is a separate deliverable |
| Version 1 and version 2 of the same deliverable with identical description and acceptance criteria | Version 2's criteria state what is new, e.g., "covers 20 indexed items instead of 10" | Deliverables not clearly defined |

## Patterns to use if stuck

- **Version it.** Plan v1, v2, … of a deliverable across sprints, as with the charter. Each version's criteria say what is new.
- **One deliverable per milestone condition.** Ask what artifact proves the milestone in [Milestones](03-project-canvas_v2/02-milestones.md).
- **Release builds as deliverables.** Make each alpha, beta and release candidate in [Release Plan](03-project-canvas_v2/10-release-plan.md) a deliverable.
- **Borrow thresholds from [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md).** Reuse the success-criteria numbers of the objective the deliverable serves. This also means referring to metrics by name. (e.g. Recall@k, MRR, Faithfullness)
- **Documentation set.** Typical documentation deliverables are the Dataset Report, Q&A Data Report or Third-party Dataset Register, the AI SBOM, model cards (training or fine-tuning only) and experiment cards.

## What doesn't belong on this page

| Item | Where it belongs |
|---|---|
| Events and checkpoints, and the alignment rule | [Milestones](03-project-canvas_v2/02-milestones.md) |
| Sprint dates and releases | [Release Plan](03-project-canvas_v2/10-release-plan.md) |
| Objective success criteria | [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) |
| Deliverables needed from, or required by, other projects | [Dependencies](03-project-canvas_v2/06-dependencies.md) |
| Costs | [Cost & Funding](03-project-canvas_v2/07-cost-and-funding.md) |
| Roles and who holds them | [Project Organization](03-project-canvas_v2/08-project-organization.md) |
| The content of datasheets, model cards and experiment cards | Their own pages |

## Deliverable block

Copy and paste the block below as needed for each deliverable.

| Project Deliverable #: | [Deliverable Name] |
|---|---|
| Description: |   |
| Acceptance Criteria: |   |
| Due Date: |   |
| Stakeholders: |   |
| Approving Stakeholder(s): |   |

## Example (illustrative only)

The project, names, numbers and dates are invented. They match the examples in [Milestones](03-project-canvas_v2/02-milestones.md) and [Release Plan](03-project-canvas_v2/10-release-plan.md). The project is a RAG assistant that answers students' questions about a university's course regulations.

| Project Deliverable #: | D1: Project Charter v1 |
|---|---|
| Description: | First version of the Project Canvas pages |
| Acceptance Criteria: | 1. All cells marked with * are filled. 2. Every objective has at least one numeric success criterion. 3. Every milestone in [Milestones](03-project-canvas_v2/02-milestones.md) has an associated deliverable on this page. |
| Due Date: | 28/10/2026 |
| Stakeholders: | Project Review Committee; project team |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D2: Q&A Generation-Dataset v1 |
|---|---|
| Description: | Question–answer pairs generated from the regulations corpus, used to evaluate retrieval and answers. Stored as a file in the Git repository. |
| Acceptance Criteria: | 1. At least 200 pairs. 2. Every regulation chapter has at least 10 questions. 3. At least 20% of questions need two or more passages to answer. 4. A sample of 40 pairs is checked by hand, with at least 90% judged correct. 5. The generator model and prompt are recorded. |
| Due Date: | 18/11/2026 |
| Stakeholders: | Project team (AI developer role) |
| Approving Stakeholder(s): | Product Owner |

| Project Deliverable #: | D6: Beta release |
|---|---|
| Description: | Assistant deployed for five pilot students, with a feedback button |
| Acceptance Criteria: | 1. All five pilot users can log in and receive an answer. 2. Recall@5 ≥ 0.70 and p95 latency ≤ 3 s on the D2 test questions. 3. Every answer shows at least one source link. |
| Due Date: | 09/12/2026 |
| Stakeholders: | AI customer: student affairs office; AI users: pilot students |
| Approving Stakeholder(s): | Product Owner; student affairs contact |

## Checklist before submitting

- [ ] Both solution and project-management deliverables are listed (Rule 1)
- [ ] Each charter version is a separate deliverable (Rule 2)
- [ ] Every block has all six fields filled (Rule 3)
- [ ] Every acceptance criterion is measurable (Rule 4)
- [ ] No acceptance criterion relies on an adjective without a number (Rule 5)
- [ ] Customer-facing deliverables list the customer or users as Stakeholders, not only the team (Rule 6)
- [ ] Every block names an Approving Stakeholder (Rule 7)
- [ ] Every due date is aligned with its milestone in [Milestones](03-project-canvas_v2/02-milestones.md) (Rule 8)
- [ ] A Q&A Generation-Dataset deliverable exists, with diversity and representation criteria (Rule 9)
- [ ] Any team-written model card is for a trained or fine-tuned model (Rule 10)
- [ ] Every later-measured target in [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) has a deliverable that holds the result (Rule 11)
- [ ] The product is delivered in more than one version across sprints (Rule 12)
- [ ] The page is complete in the first version of the canvas (red cell)

## References

[1] Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. In *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAT\* '19)* (pp. 220–229). Association for Computing Machinery. https://doi.org/10.1145/3287560.3287596

[2] Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM, 64*(12), 86–92. https://doi.org/10.1145/3458723

[3] International Organization for Standardization & International Electrotechnical Commission. (2024). *Information technology — Artificial intelligence — Guidance for AI applications* (ISO/IEC 5339:2024, 1st ed.). Prepared by ISO/IEC JTC 1/SC 42, Artificial intelligence. Edition used: British Standards Institution. (2024). *BS ISO/IEC 5339:2024* (published 31 January 2024). BSI Standards Limited. ISBN 978 0 539 15221 0.

[4] International Organization for Standardization & International Electrotechnical Commission. (2023). *Information technology — Artificial intelligence — AI system life cycle processes* (ISO/IEC 5338:2023, 1st ed.). Prepared by ISO/IEC JTC 1/SC 42, Artificial intelligence. Edition used: British Standards Institution. (2024). *BS ISO/IEC 5338:2023* (published 29 February 2024). BSI Standards Limited. ISBN 978 0 539 15220 3.
