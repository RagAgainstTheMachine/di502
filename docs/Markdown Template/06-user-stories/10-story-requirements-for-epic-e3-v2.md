# Story Requirements for Epic E3: Legal-Status Labels (v2)

> **Superseded on 25/10/2026** by [User Story Map (v3)](15-user-story-map-v3.md), the current version. Epic IDs changed between versions; see the [epic lineage](README.md#epic-lineage). Kept as the record of User Story Map (v2).


| Epic                    | E3 Legal-status labels (charter feature F3 Legal status label; objective O4) |
| ----------------------- | ---------------------------------------------------------------------------- |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                      |
| Designer                | TBD                                                                          |
| Developers              | TBD                                                                          |
| Release Target (Sprint) | Alpha (Sprint 2, 18/11/2026): US-11; Beta (Sprint 3, 09/12/2026): US-12      |
| Jira                    |                                                                              |

## Requirements


| #     | User story title                           | User story description                                                                                                           | Priority | Notes                               |
| ----- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------- |
| US-11 | See each source's legal status and date    | As a legal-unit staff member, I want to see each source's legal status and date, so that I can tell law from plans and guidance. | Highest  | F3 · O4 · Alpha · Jira: DI502-17 |
| US-12 | Know in the answer when a point is not law | As a training-unit staff member, I want the answer to say when a point is not law, so that I do not teach it as law.             | High     | F3 · O4 · Beta · Jira: new       |

## Acceptance criteria

### US-11 See each source's legal status and date

1. When the assistant cites a source, the assistant shall show its legal status and date from the document inventory.
2. When an answer cites sources with different legal statuses, the assistant shall show each source's own status.

### US-12 Know in the answer when a point is not law

1. When an answer states a point from a source that is not binding law, the assistant shall name the source's legal status in the same sentence.
