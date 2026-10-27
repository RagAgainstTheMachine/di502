# User Story Map v3

Version 3, 25 October 2026.

It replaces [User Story Map v2](02-user-story-map-v2.md).


**14 user stories in 5 epics.** Every story stays inside the description of one charter feature and has one primary objective.

## 1. Personas

All personas are AI users from the Executive Summary (stakeholders 1 and 2). Stories are written from the AI-user perspective only.


| Persona                    | ISO/IEC 5339 role                  | Who they are                                                                                           | Typical questions                                                     |
| -------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| Strategy-unit specialist   | AI user (primary), stakeholder 1   | Prepares the institution's AI roadmap after the Action 7 appointments and briefs management            | Who is responsible, what by when                                      |
| Legal-unit staff member    | AI user (primary), stakeholder 1   | Checks which rules apply to the institution and writes legal opinions; handles personal-data questions | Exact provisions, KVKK rules, transfers abroad                        |
| Training-unit staff member | AI user (primary), stakeholder 1   | Prepares AI-literacy training for colleagues                                                           | The full picture across documents, what a term means, what is binding |
| AI-policy researcher       | AI user (secondary), stakeholder 2 | Studies Türkiye's AI policy and compares positions between documents                                   | Dates, differing positions                                            |
| Graduate student           | AI user (secondary), stakeholder 2 | Writes a thesis or paper on AI policy                                                                  | Citable references                                                    |

## 2. Epics


| Epic | Name                       | Charter feature                                                | Objectives of the feature (charter 3.1) | Stories                      | Jira     | Story requirements                                 |
| ---- | -------------------------- | -------------------------------------------------------------- | --------------------------------------- | ---------------------------- | -------- | -------------------------------------------------- |
| E1   | Asking and getting answers | F1 Plain-language questions                                    | O1, O2                                  | US-1, US-2, US-3, US-4, US-5 | DI502-11 | [Epic E1](15-story-requirements-for-epic-e1-v3.md) |
| E2   | Source transparency        | F2 Source reference, F3 Legal status label, F6 Collection date | O2, O4                                  | US-6, US-7, US-8             | DI502-15 | [Epic E2](16-story-requirements-for-epic-e2-v3.md) |
| E3   | Follow-up questions        | F4 Follow-up questions                                         | O1, O2, O3                              | US-9                         | new      | [Epic E3](17-story-requirements-for-epic-e3-v3.md) |
| E4   | Clear decline              | F5 Clear decline                                               | O5                                      | US-10, US-11, US-12          | new      | [Epic E4](18-story-requirements-for-epic-e4-v3.md) |
| E5   | Term definitions           | F7 Term definitions                                            | O2                                      | US-13, US-14                 | new      | [Epic E5](19-story-requirements-for-epic-e5-v3.md) |

## 3. Map: feature → epic → story → task

Tasks are added under each story at sprint planning (slide 11). Columns follow the user's journey from left to right (slide 12); rows are release slices tied to [Deliverables](../03-project-canvas/05-deliverables.md). The slices are a starting point for sprint planning, not a commitment: capacity and planning poker decide.


| Release slice                                | E1 Asking and getting answers | E5 Term definitions | E2 Source transparency | E3 Follow-up questions | E4 Clear decline |
| -------------------------------------------- | ----------------------------- | ------------------- | ---------------------- | ---------------------- | ---------------- |
| **Alpha**, Sprint 2, 18/11 (D5)              | US-1, US-2, US-3              |                     | US-6, US-7             |                        | US-10            |
| **Beta**, Sprint 3, 09/12 (D7, D8)           | US-4, US-5                    | US-13               | US-8                   | US-9                   | US-11, US-12     |
| **Release candidate**, Sprint 4, 30/12 (D10) |                               | US-14               |                        |                        |                  |

## 4. Stories


| Story | Title                                                             | Persona          | Feature | Epic | Primary objective | Priority | Release | Jira key      | Story points | Story requirements                                 |
| ----- | ----------------------------------------------------------------- | ---------------- | ------- | ---- | ----------------- | -------- | ------- | ------------- | ------------ | -------------------------------------------------- |
| US-1  | Ask a question about AI policy                                    | Strategy unit    | F1      | E1   | O2                | Highest  | Alpha   | DI502-12      | TBD          | [Epic E1](15-story-requirements-for-epic-e1-v3.md) |
| US-2  | Find out what an AI policy action or measure requires and by when | Strategy unit    | F1      | E1   | O2                | High     | Alpha   | to be created | TBD          | [Epic E1](15-story-requirements-for-epic-e1-v3.md) |
| US-3  | Find out who is responsible for an action                         | Strategy unit    | F1      | E1   | O2                | High     | Alpha   | to be created | TBD          | [Epic E1](15-story-requirements-for-epic-e1-v3.md) |
| US-4  | Read a provision I know by number                                 | Legal unit       | F1      | E1   | O2                | High     | Beta    | to be created | TBD          | [Epic E1](15-story-requirements-for-epic-e1-v3.md) |
| US-5  | See what all the documents say on a topic                         | Training unit    | F1      | E1   | O2                | High     | Beta    | DI502-14      | TBD          | [Epic E1](15-story-requirements-for-epic-e1-v3.md) |
| US-6  | See the source of each answer                                     | Legal unit       | F2      | E2   | O2                | Highest  | Alpha   | DI502-16      | TBD          | [Epic E2](16-story-requirements-for-epic-e2-v3.md) |
| US-7  | Know how binding and how recent each cited document is            | Legal unit       | F3      | E2   | O4                | Highest  | Alpha   | DI502-17      | TBD          | [Epic E2](16-story-requirements-for-epic-e2-v3.md) |
| US-8  | See how current the documents are                                 | Researcher       | F6      | E2   | O2                | High     | Beta    | DI502-18      | TBD          | [Epic E2](16-story-requirements-for-epic-e2-v3.md) |
| US-9  | Ask a follow-up without repeating myself                          | Legal unit       | F4      | E3   | O2                | High     | Beta    | DI502-13      | TBD          | [Epic E3](17-story-requirements-for-epic-e3-v3.md) |
| US-10 | Be told when the documents have no answer                         | Researcher       | F5      | E4   | O5                | Highest  | Alpha   | to be created | TBD          | [Epic E4](18-story-requirements-for-epic-e4-v3.md) |
| US-11 | Know what is mentioned but not prepared yet                       | Strategy unit    | F5      | E4   | O5                | High     | Beta    | to be created | TBD          | [Epic E4](18-story-requirements-for-epic-e4-v3.md) |
| US-12 | Find the rules for my institution's case                          | Legal unit       | F5      | E4   | O5                | Highest  | Beta    | to be created | TBD          | [Epic E4](18-story-requirements-for-epic-e4-v3.md) |
| US-13 | Ask what an AI term means                                         | Training unit    | F7      | E5   | O2                | High     | Beta    | to be created | TBD          | [Epic E5](19-story-requirements-for-epic-e5-v3.md) |
| US-14 | Find the English name of an AI term                               | Graduate student | F7      | E5   | O2                | Medium   | RC      | to be created | TBD          | [Epic E5](19-story-requirements-for-epic-e5-v3.md) |

Slice totals: Alpha 6, Beta 7, Release candidate 1. Priorities: Highest 5, High 8, Medium 1. Story points are TBD until planning poker.

## 5. Changes from V2


| Item                                 | Change                                                                                                                                                     | Reason                                                                                                                                                                                                              |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v2 E1.1, E1.2, E1.3                  | Merged into one epic, E1 Asking and getting answers (F1)                                                                                                   | All three held F1 stories for the same objectives (O1, O2)                                                                                                                                                          |
| v2 E2, E3, E6                        | Merged into one epic, E2 Source transparency (F2, F3, F6)                                                                                                  | E6 held one story in one release                                                                                                                                                                                    |
| v2 US-2                              | Merged into v3 US-1 as criterion 3, reworded; the term definitions added to the E1 page                                                                    | Answering only from the official documents is part of F1 and constraint C-05, not a separate user goal                                                                                                              |
| v3 US-1                              | Criteria 2 and 3 reworded (complete answer; each factual statement supported by the official documents)                                                    | The old wording ("in-scope question", "key points that a passage gives") was unclear                                                                                                                                |
| v2 US-4, v2 US-5                     | Order swapped: v3 US-2 is what an action or measure requires and by when, v3 US-3 is who is responsible. v3 US-2 reworded, criteria rewritten, Terms added | Product Owner decision on order; the old criteria asked for "steps" and "the source", words the documents do not use                                                                                                |
| v2 US-6 (v3 US-4)                    | Story and title reworded; two criteria added (number in several documents, number not found); Term "Provision" added                                       | The story described an interaction, and a missing or ambiguous number was not specified                                                                                                                             |
| v2 US-7 (v3 US-5)                    | Story, title and criterion reworded; Term "Answers in part" added                                                                                          | The story described a system action, and the trigger ("needs more than one document") was a judgement                                                                                                               |
| v2 US-8                              | Deleted; no replacement story                                                                                                                              | Product Owner decision: v3 US-5 and the source stories already deliver each document's point with its source. The charter's "favours none" resolution for regulators vs researchers is no longer carried by a story |
| v2 US-9 (v3 US-6)                    | Story reworded; criterion 4 added from v2 US-10                                                                                                            | Checking each point is the same need as checking the answer                                                                                                                                                         |
| v2 US-10                             | Merged into v3 US-6 (criterion 4)                                                                                                                          | Same feature and objective as v2 US-9                                                                                                                                                                               |
| v2 US-11 (v3 US-7)                   | Story and title reworded; criterion 1 split into legal status and date                                                                                     | The story described a display; legal status and date are checked separately                                                                                                                                         |
| v2 US-12                             | Deleted; no replacement story                                                                                                                              | Product Owner decision                                                                                                                                                                                              |
| v2 US-17 (v3 US-8)                   | Criterion 2 trigger rewritten ("current legal state"); Term added                                                                                          | "Time-sensitive question" was a judgement                                                                                                                                                                           |
| v2 US-13 (v3 US-9)                   | Criterion 2 added: a question with a Turkish reference word that refers to an item in the most recent answer is answered about that item; Terms added      | Gives the follow-up a trigger that a reviewer can observe                                                                                                                                                           |
| v2 US-15 (v3 US-11)                  | Story and title reworded                                                                                                                                   | Teammates did not understand the old wording                                                                                                                                                                        |
| v2 US-16 (v3 US-12)                  | Story and title reworded                                                                                                                                   | The story described the assistant's behaviour, not the user's goal                                                                                                                                                  |
| v3 US-14 (new)             | Added to E5: the English name of a term is found from its Turkish definition (story and title reworded)                                                    | Graduate students need the English term for English-language literature                                                                                                                                             |
| All stories                          | Test-set tags and "Verified by" lines removed from the acceptance criteria                                                                                 | The criteria describe behaviour; the evaluation set is planned separately                                                                                                                                           |

Story IDs were renumbered in v3 so that they run without gaps from US-1 to US-14, in epic order. Four v2 stories have no v3 ID because they were merged or deleted (see the table):


| v2 ID | v3 ID            | Story                                                             |
| ----- | ---------------- | ----------------------------------------------------------------- |
| US-1  | US-1             | Ask a question about AI policy                                    |
| US-2  | merged into US-1 | Get answers only from the official texts                          |
| US-4  | US-3             | Find out who is responsible for an action                         |
| US-5  | US-2             | Find out what an AI policy action or measure requires and by when |
| US-6  | US-4             | Read a provision I know by number                                 |
| US-7  | US-5             | See what all the documents say on a topic                         |
| US-8  | deleted          | See where documents disagree                                      |
| US-9  | US-6             | See the source of each answer                                     |
| US-10 | merged into US-6 | See the source of each part of an answer                          |
| US-11 | US-7             | Know how binding and how recent each cited document is            |
| US-12 | deleted          | Know in the answer when a point is not law                        |
| US-17 | US-8             | See how current the documents are                                 |
| US-13 | US-9             | Ask a follow-up without repeating myself                          |
| US-14 | US-10            | Be told when the documents have no answer                         |
| US-15 | US-11            | Know what is mentioned but not prepared yet                       |
| US-16 | US-12            | Find the rules for my institution's case                          |
| US-18 | US-13            | Ask what an AI term means                                         |
| New   | US-14            | Find the English name of an AI term                               |

Epic IDs were renumbered in v3 so that they run from E1 to E5:


| v2 ID            | v3 ID | Epic                       |
| ---------------- | ----- | -------------------------- |
| E1.1, E1.2, E1.3 | E1    | Asking and getting answers |
| E2, E3, E6       | E2    | Source transparency        |
| E4               | E3    | Follow-up questions        |
| E5               | E4    | Clear decline              |
| E7               | E5    | Term definitions           |
