# Story Requirements for Epic E1.2: Duties, Deadlines and Provisions (v2)

> **Superseded on 25/10/2026** by [User Story Map (v3)](15-user-story-map-v3.md), the current version. Epic IDs changed between versions; see the [epic lineage](README.md#epic-lineage). Kept as the record of User Story Map (v2).


| Epic                    | E1.2 Duties, deadlines and provisions (charter feature F1 Plain-language questions; objectives O1, O2) |
| ----------------------- | ------------------------------------------------------------------------------------------------------ |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                                                |
| Designer                | TBD                                                                                                    |
| Developers              | TBD                                                                                                    |
| Release Target (Sprint) | Alpha (Sprint 2, 18/11/2026): US-4, US-5; Beta (Sprint 3, 09/12/2026): US-6                            |
| Jira                    |                                                                                                        |

## Requirements


| #    | User story title                       | User story description                                                                                                                                       | Priority | Notes                          |
| ---- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | ------------------------------ |
| US-4 | Find out who leads an action           | As a strategy-unit specialist, I want to know which institution leads an action, so that I know whom we must work with.                                      | High     | F1 · O2 · Alpha · Jira: new |
| US-5 | Find out what must be done and by when | As a strategy-unit specialist, I want to know what public institutions must do and by when, so that I can plan our AI work on time.                          | High     | F1 · O2 · Alpha · Jira: new |
| US-6 | Look up a provision by its number      | As a legal-unit staff member, I want to look up an article, action or measure by its number, so that I can read what it says without searching the document. | High     | F1 · O2 · Beta · Jira: new  |

## Acceptance criteria

### US-4 Find out who leads an action

1. When the user asks who is responsible for an action or measure (tag `responsibility`), the assistant shall name the lead institution as the source names it.
2. When the source also names cooperating institutions, the assistant shall list them separately from the lead.
3. If the source names no lead institution, then the assistant shall say so.

### US-5 Find out what must be done and by when

1. When the user asks what must be done (tag `procedural`), the assistant shall list the steps that the source gives.
2. When the source gives a deadline, the assistant shall state it in the same form as the source.
3. If the source gives no deadline, then the assistant shall say so.

### US-6 Look up a provision by its number

1. When the user gives an article, action or measure number from the collection (tag `provision-number`), the assistant shall answer from that provision.
