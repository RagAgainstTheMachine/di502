# Assumptions & Constraints

This page records what your plan rests on. It has two parts:

- An **assumption** is something you treat as true for planning, but have not proven yet. It is a documented bet that you commit to checking.
- A **constraint** is a fixed limit you must work within. It is not uncertain. It bounds the project, especially its scope.

"The dataset will be sufficient" is a weak assumption. "Sufficient" is not defined, nobody can test it, and nobody is responsible for checking it. A strong version says what the bet is based on, how it will be checked, by whom and by when: "The supplied dataset of about 12,000 labelled queries covers the 8 intents in scope, with at least 300 examples each. The Data Scientist preparing the data checks this with an exploratory analysis by the end of Sprint 1." (numbers illustrative only)

The project uses RAG as its basic solution; this is a constraint set by the Project Review Committee, so it should be reflected here.

## Assumption, constraint, risk or out of scope?

Each statement belongs in exactly one place. Use this table to decide where.

| Entry | What it is | Question it answers | Where it goes |
|---|---|---|---|
| **Assumption** | An uncertain belief you plan around, not yet proven | What are we betting on, and how will we check it? | Table 1 on this page |
| **Constraint** | A fixed limit, not uncertain; a rule that limits how the in-scope work is done | What can we not change? | Table 2 on this page |
| **Risk** | An uncertain event that would hurt the project if it happens | What could go wrong, and what will we do about it? | [Risks](03-project-canvas_v2/11-risks.md) |
| **Out-of-scope activity** | Work the team will not do at all | What are we not building? | [Major Activities](03-project-canvas_v2/04-major-activities.md), Status = Out of Scope |

## How the entries connect

**Every assumption has a risk on its flip side.** If you assume the dataset covers the in-scope categories, the matching risk is that some categories are under-represented and perform poorly. Log the assumption here and register the matching risk in [Risks](03-project-canvas_v2/11-risks.md). Cross-reference them by ID, for example A-03 ↔ R-07. An assumption that might not hold must always appear in Risks with a response plan.

**A constraint often creates or removes work.** Write such a decision as three statements, one per place, each pointing to the others:

1. The constraint (this page): the rule the system must obey.
2. An in-scope activity ([Major Activities](03-project-canvas_v2/04-major-activities.md)): the work you do because of the rule.
3. An out-of-scope activity ([Major Activities](03-project-canvas_v2/04-major-activities.md)): the features you give up because of it.

The uncertain part of a constraint becomes a risk, and the in-scope activity is its mitigation.

**Scope protects your assumptions.** Define the intended operating domain (users, inputs, languages, categories) and list what is out of scope. Your assumptions then only have to hold inside that boundary. A failure outside the boundary is a documented limitation, not a broken assumption.

**One concern can produce several entries.** For example:

| Entry | Example |
|---|---|
| Constraint | The project will be developed by four students. No additional recruitment is possible. |
| Risk | A member of the team may leave the team or cannot dedicate the required time. |
| Assumption | All defined team members will remain enrolled in the course and continue participation for the full duration of the project. |

To make that assumption checkable, give it an owner and a validation date, for example "checked at each sprint start by the named member" (illustrative only).

## Fields

### Table 1: Assumptions

| Field | What it means | Question it answers |
|---|---|---|
| **#** | ID in the form A-01, A-02, … | Which risk refers to this assumption? |
| **Assumption** | The belief, stated with numbers or a named condition | What exactly are we betting on? |
| **Basis** | The evidence the belief rests on | Based on what? |
| **Validation** | How the belief will be checked, and the date or sprint | How and by when will we know? |
| **Owner** | The named person who does the check | Who is responsible for checking? |
| **Linked risk** | ID of the matching risk in [Risks](03-project-canvas_v2/11-risks.md) | What happens if the bet is wrong? |

### Table 2: Constraints

| Field | What it means | Question it answers |
|---|---|---|
| **#** | ID in the form C-01, C-02, … | Which activities and risks refer to this constraint? |
| **Category** | One of the five layers used in [Risks](03-project-canvas_v2/11-risks.md): Data, Model, Infrastructure, Integration, People / process | What kind of limit is this? |
| **Constraints** | The fixed limit, stated as a fact | What can we not change? |
| **Linked activities / risks** | IDs or row numbers in [Major Activities](03-project-canvas_v2/04-major-activities.md) and [Risks](03-project-canvas_v2/11-risks.md) | What work does it create or remove, and what is uncertain about it? |

Legal, budget and schedule limits all go under People / process. Technical limits go under Data, Model, Infrastructure or Integration, so that you can describe the technical side in more detail.

## Rules

Assumptions:

1. An assumption could turn out false, and being wrong would visibly change the plan. If it couldn't be wrong, or being wrong wouldn't matter, delete it.
2. An assumption is specific. It uses no undefined words such as "sufficient", "enough" or "stable" without a number.
3. An assumption states its basis.
4. An assumption has a validation method, a date or sprint, and a named owner.
5. An assumption has a linked risk in [Risks](03-project-canvas_v2/11-risks.md).
6. An assumption concerns a matter outside the project's control. A commitment the team makes about its own work is a plan, not an assumption.
7. These are not assumptions:
   - The performance of the selected LLM, embedding model or API ("the API will work seamlessly"). Handle these as risks.
   - Expected user behaviour ("users will ask contextually related questions"). Define the input boundary as a constraint instead.
   - Having enough resources, such as cloud credits. This is a constraint.
   - "Milestones will be achieved on time". This is a goal.
   - "The system will not have downtimes". This is a desired outcome; restate it as a risk.

Constraints:

8. A constraint is stated as a fact, not as a hope. Write "Compute is limited to the allocated credit", not "The credit will be enough".
9. A constraint gives the number or names the rule; it uses no adjectives such as "limited" or "relatively short".
10. Every constraint has a category, and constraints are grouped by category.
11. A limit the system operates within is a constraint, for example a user-input boundary or English-only text. Work you will not do goes to [Major Activities](03-project-canvas_v2/04-major-activities.md) as Out of Scope.
12. A constraint that creates or removes work has its matching in-scope and out-of-scope rows in [Major Activities](03-project-canvas_v2/04-major-activities.md), and each statement points to the others.
13. "Limited computational resources" is a constraint. The assigned resources fluctuating or failing is a risk.

Both:

14. The same statement does not appear as both an assumption and a constraint. Duplicates are an internal inconsistency in the review error types.

## Tests to apply to your draft

**For each assumption, answer four questions.** If you cannot answer one, fix the row.

1. **Based on what?** Name the evidence.
2. **Could it be wrong, and would that change the plan?** If not, delete it.
3. **Who checks it, how, and by when?**
4. **Is it outside our control?** If not, it is a task or a plan, not an assumption.

**For each constraint, answer three questions.**

1. **Is it fixed?** If it is uncertain, it is an assumption or a risk.
2. **Is there a number or a named rule?**
3. **Does it create or remove work?** If yes, the matching rows exist in [Major Activities](03-project-canvas_v2/04-major-activities.md).

## Not this / this

The left column shows weak entries. Each row names the rule it breaks. The corrected version fixes only that defect. Numbers on the right are illustrative only.

| Not this | Rule broken | This |
|---|---|---|
| "The dataset has enough entries to sufficiently answer questions." | Vague and untestable, with no owner or date (rules 2–4) | "The supplied dataset has at least 200 entries for each of the 6 in-scope topics. Basis: row counts on the dataset's public page. The Data Scientist preparing the data checks this with a per-topic count by the end of Sprint 1. Linked risk: R-02." |
| "Users will ask contextually related questions about the indexed content." | Expected user behaviour is not an assumption (rule 7) | Constraint (Model): "The system handles single-turn, fact-seeking questions about the indexed content only." Plus risk: "Users ask out-of-scope questions and receive confident wrong answers." |
| "The system will not perform complex actions, and will focus on simple questions and answers." | A scope limit written as an assumption (rule 11) | Constraint (Model): "The system answers questions only; it performs no actions on the user's behalf." Plus an out-of-scope row in [Major Activities](03-project-canvas_v2/04-major-activities.md): "Transactions or account actions for the user." |
| "The project team will have consistent access to the necessary computational resources." | Available resources are a constraint, not an assumption (rule 7) | Constraint (Infrastructure): "Compute is limited to one shared GPU allocation from the university." Plus risk: "The assigned GPU allocation fluctuates or becomes unavailable." |
| "The external data APIs will remain accessible and stable during the project period." | API behaviour is not an assumption (rule 7) | A row in [Dependencies](03-project-canvas_v2/06-dependencies.md) for the API, and a risk in [Risks](03-project-canvas_v2/11-risks.md): "The external data API changes its endpoints or is unavailable for more than 1 day." |
| "The free-tier access limits of these APIs will be sufficient for development and testing." | "Sufficient" is vague, and the limit itself is a constraint (rules 2, 7) | Constraint (Integration): "The API free tier allows 500 calls per day." Assumption: "The test plan needs at most 300 calls per day. Basis: planned test-set size × runs per day. Checked by the owner of the evaluation scripts by the end of Sprint 2. Linked risk: R-05." |
| "The project team will maintain continuous internal coordination and follow sprint planning practices." | Within the team's control, so not an assumption (rule 6) | Remove it. Coordination is planned work; put it in [Major Activities](03-project-canvas_v2/04-major-activities.md) (project management). |
| "The cloud credit provided will be enough to complete the project." | A constraint stated as a hope (rule 8) | Constraint (People / process): "Compute spending is limited to the cloud credit allocated by the university." Assumption: "Planned experiments use at most 70% of that credit. Basis: cost of the Sprint 1 pilot run. Checked by the Data Scientist running experiments by the end of Sprint 2. Linked risk: R-04." |
| "Team members have relatively limited time to work on the project." | Adjective instead of a number (rule 9) | Constraint (People / process): "Each team member works on the project at most 5 hours per week." |
| "The system relies on third-party APIs, so any downtime or API change may affect performance." | Describes an uncertain event, so not a fixed limit (rule 8) | A row in [Dependencies](03-project-canvas_v2/06-dependencies.md) for the reliance, and a risk in [Risks](03-project-canvas_v2/11-risks.md) for the downtime. |
| "English" listed both as Assumption 1 and as a constraint. | Duplicate entry (rule 14) | Keep only the constraint (Data): "The system is developed and evaluated on English-language text only." |

A good entry to copy: "The dataset is not a data stream, so some information may not be up to date." It is a fixed, specific limit. It could be sharpened with the date range of the data.

## Patterns to use if you are stuck

Assumption patterns. Each one is concrete, could be false, and would change the plan if it were:

- **Representativeness:** the historical data is representative of the data the system will see after deployment.
- **Label quality:** labels have an error rate below about 5%, checked by manually reviewing a random sample of 200 records.
- **Expert time:** domain experts are available at least 2 hours per week for labelling questions and result review.
- **Environment access:** access to the production or staging environment is provided by week 4.
- **Permission to use data:** using the data for training is permitted under the data agreement and privacy rules, confirmed with the data owner before training begins.
- **Agreed target:** stakeholders agree that a stated metric value on the held-out test set is acceptable for the first release.

Constraint patterns:

- **User-input boundary:** "The system's functional scope is limited to single-turn, contextually related, fact-seeking queries about the indexed content."
- **Language:** "Working with English text only."
- **Team size:** "Four students; no additional recruitment is possible."
- **Compute limit:** a fixed allocation or quota.
- **Privacy rule**, written with its activities:
  - Constraint: "The system shall not persist personally identifiable information (e.g., names, email addresses, national ID numbers) in any database, log or vector index."
  - In scope ([Major Activities](03-project-canvas_v2/04-major-activities.md)): "Implement PII detection and masking on user inputs before logging." "Configure logs to keep only anonymized interaction data."
  - Out of scope ([Major Activities](03-project-canvas_v2/04-major-activities.md)): "User accounts, personal profiles, and saved conversation history linked to an identity."
  - Risk ([Risks](03-project-canvas_v2/11-risks.md)): "Users submit PII in free-text queries, and it ends up in logs or the retrieval index." The masking activity is the mitigation; a review of the logs is the check.

## What doesn't belong here

- **Risk plans** (mitigation, trigger, contingency, owner) go in [Risks](03-project-canvas_v2/11-risks.md). This page keeps only the ID of the linked risk.
- **Features you will not build** go in [Major Activities](03-project-canvas_v2/04-major-activities.md) as Out of Scope.
- **Who must deliver what, by when** goes in [Dependencies](03-project-canvas_v2/06-dependencies.md).
- **The list of tools, compute and data access** goes in [Facilities & Resources](03-project-canvas_v2/09-facilities-and-resources.md). A fixed limit on one of them stays here as a constraint.
- **Effort and cost figures** go in [Cost & Funding](03-project-canvas_v2/07-cost-and-funding.md).
- **Goals and targets** go in the objectives of [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md).
- **Milestone dates** go in [Milestones](03-project-canvas_v2/02-milestones.md). A mandated deadline stays here as a constraint.

CONFLICT: the template says the budget constraint is defined in the Project Executive Summary, but it also lists a set budget as a constraint on this page. Until this is resolved, make the two statements identical.

## 1. Assumptions

Add rows as needed.

| # | Assumption | Basis | Validation (how, by when) | Owner | Linked risk |
|---|---|---|---|---|---|
| A-01 | | | | | |
| A-02 | | | | | |
| A-03 | | | | | |

## 2. Constraints

Group constraints by category. Add rows as needed.

| # | Category | Constraints | Linked activities / risks |
|---|---|---|---|
| C-01 | | | |
| C-02 | | | |
| C-03 | | | |

## Example (illustrative only)

Scenario: a legal research assistant, a RAG chatbot over legal documents. All names, numbers and dates are illustrative.

| # | Assumption | Basis | Validation (how, by when) | Owner | Linked risk |
|---|---|---|---|---|---|
| A-01 | The document set (statutes and case summaries, 2015 onward) covers the 5 practice areas in scope, with at least 150 documents each. | Index listing published by the data provider | Per-area document count, end of Sprint 1 | Data Scientist (named member) | R-01 |
| A-02 | A legal expert is available at least 2 hours per week to review answers. | Verbal agreement at kick-off | Confirm in writing; check attendance at each sprint review | Business Analyst (named member) | R-06 |
| A-03 | Using the documents for retrieval is permitted under their licence. | Licence text on the provider's site | Confirm with the data owner before indexing, Sprint 1 | Business Analyst (named member) | R-07 |
| A-04 | The allocated GPU quota supports the latency target for 20 concurrent users. | Vendor benchmark for the chosen model size | Capacity test, end of Sprint 2 | Data Scientist, infrastructure (named member) | R-04 (the latency example in [Risks](03-project-canvas_v2/11-risks.md)) |

| # | Category | Constraints | Linked activities / risks |
|---|---|---|---|
| C-01 | People / process | Four students; no additional recruitment; at most 5 hours per member per week. | [Risks](03-project-canvas_v2/11-risks.md) R-08 |
| C-02 | Infrastructure | Compute is limited to the cloud credit allocated by the university. | [Facilities & Resources](03-project-canvas_v2/09-facilities-and-resources.md) row 1; [Risks](03-project-canvas_v2/11-risks.md) R-04 |
| C-03 | People / process | The system shall not persist PII in any database, log or vector index. | [Major Activities](03-project-canvas_v2/04-major-activities.md) rows 7 (in scope: masking) and 12 (out of scope: user accounts); [Risks](03-project-canvas_v2/11-risks.md) R-03 |
| C-04 | Model | Single-turn, fact-seeking questions about the indexed documents only; English text only. | [Major Activities](03-project-canvas_v2/04-major-activities.md) row 13 (out of scope: multi-turn memory) |
| C-05 | Integration | The hosted LLM API allows 500 calls per day on the academic tier. | [Facilities & Resources](03-project-canvas_v2/09-facilities-and-resources.md) row 2; [Risks](03-project-canvas_v2/11-risks.md) R-05 |

## Checklist before submitting

- [ ] Every assumption could turn out false, and being wrong would change the plan (rule 1)
- [ ] No assumption uses an undefined word such as "sufficient", "enough" or "stable" (rule 2)
- [ ] Every assumption has a Basis (rule 3)
- [ ] Every assumption has a validation method, a date or sprint, and a named owner (rule 4)
- [ ] Every assumption has a Linked risk, and that risk exists in [Risks](03-project-canvas_v2/11-risks.md) with the same ID (rule 5)
- [ ] No assumption is about the team's own work, model or API performance, user behaviour, available resources, goals or desired outcomes (rules 6–7)
- [ ] Every constraint is stated as a fact, with a number or a named rule and no adjectives (rules 8–9)
- [ ] Every constraint has one of the five categories, and constraints are grouped by category (rule 10)
- [ ] Every constraint that creates or removes work has its rows in [Major Activities](03-project-canvas_v2/04-major-activities.md), and the IDs point both ways (rules 11–12)
- [ ] No statement appears as both an assumption and a constraint (rule 14)
- [ ] The budget statement here matches the one in [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md)
