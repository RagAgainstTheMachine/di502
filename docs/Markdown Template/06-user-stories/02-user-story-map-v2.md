# User Story Map v2

Version 2, 20 October 2026.

It replaces [User Story Map v1](01-user-story-map-v1.md) and follows the Week 3 lecture *User Stories, Jira and Sprint Planning* and the charter pages updated on 20/10/2026: the [Project Executive Summary](../03-project-canvas/01-project-executive-summary.md), [Milestones](../03-project-canvas/02-milestones.md) and [Deliverables](../03-project-canvas/05-deliverables.md).

Features F1–F7 come from charter section 3.1. Each story's acceptance criteria are on the story requirements page of its epic. Story points will come from planning poker and assignees from sprint planning.

**17 user stories in 9 epics.** Every story stays inside the description of one charter feature and has one primary objective.

## 1. Personas

All personas are AI users from the Executive Summary (stakeholders 1 and 2). Stories are written from the AI-user perspective only.


| Persona                    | ISO/IEC 5339 role                  | Who they are                                                                                           | Typical questions                                                     |
| -------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Strategy-unit specialist   | AI user (primary), stakeholder 1   | Prepares the institution's AI roadmap after the Action 7 appointments and briefs management            | Who is responsible, what by when                                      |
| Legal-unit staff member    | AI user (primary), stakeholder 1   | Checks which rules apply to the institution and writes legal opinions; handles personal-data questions | Exact provisions, KVKK rules, transfers abroad                        |
| Training-unit staff member | AI user (primary), stakeholder 1   | Prepares AI-literacy training for colleagues                                                           | The full picture across documents, what a term means, what is binding |
| AI-policy researcher       | AI user (secondary), stakeholder 2 | Studies Türkiye's AI policy and compares positions between documents                                  | Dates, differing positions                                            |
| Graduate student           | AI user (secondary), stakeholder 2 | Writes a thesis or paper on AI policy                                                                  | Citable references                                                    |

## 2. Epics


| Epic | Name                             | Charter feature             | Objectives of the feature (charter 3.1) | Stories             | Jira               | Story requirements                                  |
| ---- | -------------------------------- | --------------------------- | --------------------------------------- | ------------------- | ------------------ | --------------------------------------------------- |
| E1.1 | Asking and getting answers       | F1 Plain-language questions | O1, O2                                  | US-1, US-2          | DI502-11 (renamed) | [Epic E1.1](06-story-requirements-for-epic-e1-1.md) |
| E1.2 | Duties, deadlines and provisions | F1 Plain-language questions | O1, O2                                  | US-4, US-5, US-6    | new                | [Epic E1.2](07-story-requirements-for-epic-e1-2.md) |
| E1.3 | Answers across documents         | F1 Plain-language questions | O1, O2                                  | US-7, US-8          | new                | [Epic E1.3](08-story-requirements-for-epic-e1-3.md) |
| E2   | Cited answers                    | F2 Source reference         | O2                                      | US-9, US-10         | DI502-15 (renamed) | [Epic E2](09-story-requirements-for-epic-e2.md)     |
| E3   | Legal-status labels              | F3 Legal status label       | O4                                      | US-11, US-12        | new                | [Epic E3](10-story-requirements-for-epic-e3.md)     |
| E4   | Follow-up questions              | F4 Follow-up questions      | O1, O2, O3                              | US-13               | new                | [Epic E4](11-story-requirements-for-epic-e4.md)     |
| E5   | Clear decline                    | F5 Clear decline            | O5                                      | US-14, US-15, US-16 | new                | [Epic E5](12-story-requirements-for-epic-e5.md)     |
| E6   | Collection currency              | F6 Collection date          | O2                                      | US-17               | new                | [Epic E6](13-story-requirements-for-epic-e6.md)     |
| E7   | Term definitions                 | F7 Term definitions         | O2                                      | US-18               | new                | [Epic E7](14-story-requirements-for-epic-e7.md)     |

## 3. Map: feature → epic → story → task

Tasks are added under each story at sprint planning (slide 11). Columns follow the user's journey from left to right (slide 12); rows are release slices tied to [Deliverables](../03-project-canvas/05-deliverables.md). The slices are a starting point for sprint planning, not a commitment: capacity and planning poker decide.


| Release slice                                | E6 Collection currency | E1.1 Asking and getting answers | E1.2 Duties, deadlines and provisions | E1.3 Answers across documents | E7 Term definitions | E2 Cited answers | E3 Legal-status labels | E4 Follow-up questions | E5 Clear decline |
| -------------------------------------------- | ---------------------- | ------------------------------- | ------------------------------------- | ----------------------------- | ------------------- | ---------------- | ---------------------- | ---------------------- | ---------------- |
| **Alpha**, Sprint 2, 18/11 (D5)              |                        | US-1, US-2                      | US-4, US-5                            |                               |                     | US-9             | US-11                  |                        | US-14            |
| **Beta**, Sprint 3, 09/12 (D7, D8)           | US-17                  |                                 | US-6                                  | US-7                          | US-18               | US-10            | US-12                  | US-13                  | US-15, US-16     |
| **Release candidate**, Sprint 4, 30/12 (D10) |                        |                                 |                                       | US-8                          |                     |                  |                        |                        |                  |

## 4. Stories


| Story | Title                                                | Persona          | Feature | Epic | Primary objective | Priority | Release | Jira key      | Story points | Story requirements                                  |
| ----- | ---------------------------------------------------- | ---------------- | ------- | ---- | ----------------- | -------- | ------- | ------------- | ------------ | --------------------------------------------------- |
| US-1  | Ask a question about AI policy                       | Strategy unit    | F1      | E1.1 | O2                | Highest  | Alpha   | DI502-12      | TBD          | [Epic E1.1](06-story-requirements-for-epic-e1-1.md) |
| US-2  | Get answers only from the official texts             | Legal unit       | F1      | E1.1 | O2                | Highest  | Alpha   | to be created | TBD          | [Epic E1.1](06-story-requirements-for-epic-e1-1.md) |
| US-4  | Find out who leads an action                         | Strategy unit    | F1      | E1.2 | O2                | High     | Alpha   | to be created | TBD          | [Epic E1.2](07-story-requirements-for-epic-e1-2.md) |
| US-5  | Find out what must be done and by when               | Strategy unit    | F1      | E1.2 | O2                | High     | Alpha   | to be created | TBD          | [Epic E1.2](07-story-requirements-for-epic-e1-2.md) |
| US-6  | Look up a provision by its number                    | Legal unit       | F1      | E1.2 | O2                | High     | Beta    | to be created | TBD          | [Epic E1.2](07-story-requirements-for-epic-e1-2.md) |
| US-7  | Get one answer from several documents                | Training unit    | F1      | E1.3 | O2                | High     | Beta    | DI502-14      | TBD          | [Epic E1.3](08-story-requirements-for-epic-e1-3.md) |
| US-8  | See where documents disagree                         | Researcher       | F1      | E1.3 | O2                | Medium   | RC      | to be created | TBD          | [Epic E1.3](08-story-requirements-for-epic-e1-3.md) |
| US-9  | See the source of each answer                        | Legal unit       | F2      | E2   | O2                | Highest  | Alpha   | DI502-16      | TBD          | [Epic E2](09-story-requirements-for-epic-e2.md)     |
| US-10 | See the source of each part of an answer             | Graduate student | F2      | E2   | O2                | High     | Beta    | to be created | TBD          | [Epic E2](09-story-requirements-for-epic-e2.md)     |
| US-11 | See each source's legal status and date              | Legal unit       | F3      | E3   | O4                | Highest  | Alpha   | DI502-17      | TBD          | [Epic E3](10-story-requirements-for-epic-e3.md)     |
| US-12 | Know in the answer when a point is not law           | Training unit    | F3      | E3   | O4                | High     | Beta    | to be created | TBD          | [Epic E3](10-story-requirements-for-epic-e3.md)     |
| US-13 | Ask a follow-up without repeating myself             | Legal unit       | F4      | E4   | O2                | High     | Beta    | DI502-13      | TBD          | [Epic E4](11-story-requirements-for-epic-e4.md)     |
| US-14 | Be told when the documents have no answer            | Researcher       | F5      | E5   | O5                | Highest  | Alpha   | to be created | TBD          | [Epic E5](12-story-requirements-for-epic-e5.md)     |
| US-15 | Get no guess when the documents only mention a topic | Strategy unit    | F5      | E5   | O5                | High     | Beta    | to be created | TBD          | [Epic E5](12-story-requirements-for-epic-e5.md)     |
| US-16 | Get no verdict on my institution's case              | Legal unit       | F5      | E5   | O5                | Highest  | Beta    | to be created | TBD          | [Epic E5](12-story-requirements-for-epic-e5.md)     |
| US-17 | See how current the documents are                    | Researcher       | F6      | E6   | O2                | High     | Beta    | DI502-18      | TBD          | [Epic E6](13-story-requirements-for-epic-e6.md)     |
| US-18 | Ask what an AI term means                            | Training unit    | F7      | E7   | O2                | High     | Beta    | to be created | TBD          | [Epic E7](14-story-requirements-for-epic-e7.md)     |

Slice totals: Alpha 7, Beta 9, Release candidate 1. Priorities: Highest 6, High 10, Medium 1. Story points are TBD until planning poker.

## 5. Changes from V1


| Story        | V1 ID | Change                                                                                                              | Reason                                                                                             |
| ------------ | ----- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| US-1         | US-1  | Retitled; criteria rewritten in EARS                                                                                | "In Turkish" is slide 8's*unneeded* pattern; F1 is about the user's own words                      |
| US-13        | US-2  | "New conversation" criterion removed (parked)                                                                       | Two independently verified behaviours in one story; starting a new conversation is not a follow-up |
| US-7         | US-3  | "Each part cites its document" moved to US-9                                                                        | Belonged to F2                                                                                     |
| US-9         | US-4  | Official link kept; "cite the section that contains the supporting passage" added; per-part citation moved to US-10 | F2 describes both the citation and the link; multi-source answers arrive in the beta               |
| US-11        | US-5  | "Not presented as an obligation" moved to US-12                                                                     | Distinct behaviour; v1 wording was an unverifiable negative                                        |
| US-17        | US-6  | Source dates dropped (already US-11); time-sensitive criterion kept                                                 | Overlap with F3                                                                                    |
| Removed      | US-7  | Removed from the backlog; its rules go to the Definition of Done                                                    | Privacy is a constraint, not a feature                                                             |
| US-4, US-5   | New   | Kept as two stories (who leads; what must be done and by when); "my institution" → "public institutions"           | "Who leads" is asked on its own; judging a specific institution is excluded                        |
| US-6         | New   | Cross-feature criterion removed; reworded as a lookup                                                               | One feature per story                                                                              |
| US-8         | New   | Moved from F2 + F3 to F1 (E1.3); legal status left to US-11                                                         | One feature per story                                                                              |
| US-15, US-16 | New   | Rewritten to the charter's clear decline                                                                            | Charter F5                                                                                         |
| US-2         | New   | Moved into E1.1 (F1); second criterion moved to US-14                                                               | Its earlier epic was not a charter feature; distinct behaviour                                     |
| Removed      | New   | Removed from the backlog; its masking rule goes to the Definition of Done                                           | Privacy is a constraint, not a feature                                                             |
