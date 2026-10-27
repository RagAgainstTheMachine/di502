# Story Requirements for Epic E1.3: Answers Across Documents (v2)

> **Superseded on 25/10/2026** by [User Story Map (v3)](15-user-story-map-v3.md), the current version. Epic IDs changed between versions; see the [epic lineage](README.md#epic-lineage). Kept as the record of User Story Map (v2).


| Epic                    | E1.3 Answers across documents (charter feature F1 Plain-language questions; objectives O1, O2) |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                                        |
| Designer                | TBD                                                                                            |
| Developers              | TBD                                                                                            |
| Release Target (Sprint) | Beta (Sprint 3, 09/12/2026): US-7; Release candidate (Sprint 4, 30/12/2026): US-8              |
| Jira                    |                                                                                                |

## Requirements


| #    | User story title                      | User story description                                                                                                                | Priority | Notes                                      |
| ---- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------ |
| US-7 | Get one answer from several documents | As a training-unit staff member, I want one answer that brings all relevant documents together, so that I can teach the full picture. | High     | F1 · O2 · Beta · Jira: DI502-14         |
| US-8 | See where documents disagree          | As an AI-policy researcher, I want to see where documents take different positions, so that I can report the difference correctly.    | Medium   | F1 · O2 · Release candidate · Jira: new |

## Acceptance criteria

### US-7 Get one answer from several documents

1. When a question needs more than one document (tag `multi-document`), the assistant shall include the relevant point from each document.
2. When the user asks how a Development Plan policy is carried out, the assistant shall give the Annual Programme measures for it.

### US-8 See where documents disagree

1. When documents take different positions on the question (tag `differing-positions`), the assistant shall say which document holds each position.
2. When the assistant gives different positions, the assistant shall not say which one is right.
