# Milestones

Record here the milestones of the project. A **milestone** is an event in time that shows the project is on track: a significant point or achievement, often a decision gate or a move from one phase to the next. A milestone is not a deliverable and not a task. By the end of the project, this table serves as the high-level project schedule.

Write each milestone as a **state that becomes true on a date**, not as work to do. Write "Baseline RAG answers the full evaluation set (18/11/2026)", not "Model training" (examples illustrative only).

## Milestone, deliverable or task?
Keep the three apart. Each one goes to a different page.
| | Milestone | Deliverable | Task |
|---|---|---|---|
| **What it is** | An event in time that marks status | A tangible artifact produced as a direct output of work | A piece of work someone does |
| **Question it answers** | What is true on this date? | What do we hand over? | What do we do? |
| **Example** | "Prototype features are integrated and testable locally (18/11/2026)" | "Chatbot prototype (18/11/2026)" | "Connect the retriever to the language model" |
| **Where it goes** | This page | [Deliverables](03-project-canvas_v2/05-deliverables.md) | [Major Activities](03-project-canvas_v2/04-major-activities.md) and the Jira backlog |

The deliverable is the output that **satisfies the milestone's condition**. Progress on a milestone is shown through its associated deliverables.

### Checkpoints

A **checkpoint** is a milestone that falls **between two sprints**. Consider adding checkpoints to the timeline. The gaps between sprints are listed in 10-release-plan.md.

## How to fill in each milestone

| Field | What it means | When it applies | Question it answers |
|---|---|---|---|
| **#** | A running number (M1, M2, …) | Every row | Which milestone is this? |
| **Project Milestone** | A short name for the event, written as a state reached ("… approved", "… runs", "… in pilot users' hands") | Every row | What will be true? |
| **Description** | The condition someone can check to say the milestone is reached | Every row | How will we know it is reached? |
| **Expected Date** | A calendar date (dd/mm/yyyy) inside the project timeline. For a checkpoint, a date between two sprints. | Every row | When? |
| **Associated Deliverable** | One or more deliverables from [Deliverables](03-project-canvas_v2/05-deliverables.md), given by number and name | Every row | Which artifact proves it? |

Dates may be changed slightly later on, but make no drastic changes in Sprint 2.

## Rules

Each rule is a condition you can check with yes or no.

1. Every milestone is an event or state, not an artifact and not a task.
2. Every milestone has at least one associated deliverable.
3. Every associated deliverable appears in [Deliverables](03-project-canvas_v2/05-deliverables.md) under the same number and name.
4. Deliverable deadlines are aligned with milestones: the associated deliverable is due in the same sprint as the milestone and not later than the milestone's Expected Date. For a checkpoint, the deliverable is due by the end of the sprint before it.
5. Every Expected Date is a calendar date between 07/10/2026 and 30/12/2026.
6. Every milestone named as a checkpoint has a date that falls between the end of one sprint and the start of the next.
7. If an objective in [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) sets a target that is measured later (for example user satisfaction), a milestone shows when it is measured and a deliverable holds the result.
8. Milestones and deliverables do not force a waterfall approach. For example, evaluation does not appear only once, at the end of the project.

## Test: the three alignment questions

Ask these three questions of every milestone.

1. **Is it an event?** Can you write "On [date], [X] is true"? If you can only write "We will do X", it is a task and belongs in 04-major-activities.md.
2. **What proves it?** Name the deliverable. If nobody can point to an artifact, the milestone has no evidence.
3. **Do the dates agree?** Compare the Expected Date with the deliverable's Due Date in [Deliverables](03-project-canvas_v2/05-deliverables.md) and with the sprint dates in [Release Plan](03-project-canvas_v2/10-release-plan.md).

| Not this | This | Defect |
|---|---|---|
| A checkpoint set at 11/11/2026, linked to a deliverable due 18/11/2026 | The checkpoint dated 11/11/2026 is linked to a deliverable that exists before 11/11/2026 | Deadlines not aligned with milestones |
| "Prototype tested" due by 16/12/2026, linked to an evaluation report due on 02/12/2026 | The report's due date moved into Sprint 4, after the test it reports on | Deadlines not aligned with milestones |
| Milestone dates given only as "Mid-Sprint 2" or "End of Week 1" | The same milestones with calendar dates, e.g., "18/11/2026" | Expected Date is not a calendar date |
| An Associated Deliverable cell that lists a deliverable plus "API tests + latency tests + unit logs" | "D2: Functional core chat application". The test logs go into that deliverable's acceptance criteria in [Deliverables](03-project-canvas_v2/05-deliverables.md). | The cell must name a deliverable; test logs are evidence, not deliverables |
| An objective in [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md): "Deploy MVP and conduct demo" | A milestone on this page: "MVP demo held and approved by the customer (30/12/2026)" | This is a milestone, not an objective |
| "Model training" | "Baseline RAG answers the full evaluation set (18/11/2026)" | A task, not an event |

## Patterns to use if stuck

- **Decision gate:** a stakeholder decides go or no-go. ISO/IEC 5338 describes such points as "gates" for governance decisions [1]. Example: "Alpha reviewed; Product Owner approves move to beta."
- **Phase transition:** the work moves from one ISO/IEC 5338 life cycle stage to the next, such as Design and development → Verification and validation → Deployment [1].
- **Release reached:** an alpha, beta or release candidate from [Release Plan](03-project-canvas_v2/10-release-plan.md) is in the hands of its intended users.
- **Measurement point:** the date when a target from [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) is measured.
- **Checkpoint review:** between two sprints, results are reviewed before the next sprint starts.

## What doesn't belong on this page

| Item | Where it belongs |
|---|---|
| Artifacts, their acceptance criteria and their approvers | [Deliverables](03-project-canvas_v2/05-deliverables.md) |
| Work items and activities | [Major Activities](03-project-canvas_v2/04-major-activities.md) |
| Sprint start and end dates, and releases | [Release Plan](03-project-canvas_v2/10-release-plan.md) |
| Objectives and success criteria | [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) |
| "Milestones will be achieved on time" | This is a goal, not an assumption. If a milestone may slip, record that as a risk in [Risks](03-project-canvas_v2/11-risks.md). |

## Milestone table

Add rows as needed.

| # | Project Milestone | Description | Expected Date | Associated Deliverable |
|---|---|---|---|---|
| 1 |   |   |   |   |
| 2 |   |   |   |   |
| 3 |   |   |   |   |

## Example

The project, names, dates and deliverable numbers below are invented. They match the examples in [Deliverables](03-project-canvas_v2/05-deliverables.md) and [Release Plan](03-project-canvas_v2/10-release-plan.md). The project is a RAG assistant that answers students' questions about a university's course regulations.

| # | Project Milestone | Description | Expected Date | Associated Deliverable |
|---|---|---|---|---|
| M1 | Charter v1 approved | Product Owner signs off the charter; marked cells complete | 28/10/2026 | D1 Project Charter v1 |
| M2 | Baseline answers the full evaluation set | Baseline pipeline runs on all evaluation questions; results logged in an experiment card | 18/11/2026 | D2 Q&A Generation-Dataset v1; D3 Baseline experiment card |
| M3 | Charter v2 approved | Charter updated after Sprint 2 review; Product Owner signs off | 18/11/2026 | D5 Project Charter v2 |
| M4 | Checkpoint: go/no-go for beta | Product Owner reviews the alpha and decides whether to start the beta | 20/11/2026 | D4 Alpha prototype (due 18/11/2026) |
| M5 | Beta in pilot users' hands | Five pilot users can log in and ask questions | 09/12/2026 | D6 Beta release |
| M6 | Release candidate accepted | Customer accepts the release candidate at the final demo | 30/12/2026 | D7 Pilot feedback report; D8 Release candidate; D9 Final report |

## Checklist before submitting

- [ ] Every milestone is an event or state, not an artifact or task (Rule 1)
- [ ] Every milestone has at least one associated deliverable (Rule 2)
- [ ] Every associated deliverable exists in [Deliverables](03-project-canvas_v2/05-deliverables.md) under the same number and name (Rule 3)
- [ ] Every associated deliverable is due in the milestone's sprint and not after its Expected Date (Rule 4)
- [ ] Every Expected Date is a calendar date between 07/10/2026 and 30/12/2026 (Rule 5)
- [ ] Every checkpoint falls between two sprints (Rule 6)
- [ ] Every target in [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) that is measured later has a matching milestone and deliverable (Rule 7)
- [ ] Evaluation does not appear only once, at the end of the project (Rule 8)
- [ ] The table is complete in the first version of the canvas (red cell)

## References

[1] International Organization for Standardization & International Electrotechnical Commission. (2023). *Information technology — Artificial intelligence — AI system life cycle processes* (ISO/IEC 5338:2023, 1st ed.). Prepared by ISO/IEC JTC 1/SC 42, Artificial intelligence. Edition used: British Standards Institution. (2024). *BS ISO/IEC 5338:2023* (published 29 February 2024). BSI Standards Limited. ISBN 978 0 539 15220 3.
