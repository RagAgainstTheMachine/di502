# Story Requirements for Epic E5: Term Definitions


| Epic                    | E5 Term definitions (charter feature F7 Term definitions; objective O2)             |
| ----------------------- | ----------------------------------------------------------------------------------- |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                             |
| Designer                | TBD                                                                                 |
| Developers              | TBD                                                                                 |
| Release Target (Sprint) | Beta (Sprint 3, 09/12/2026): US-13; Release candidate (Sprint 4, 30/12/2026): US-14 |
| Jira                    | new                                                                                 |

## Requirements


| #     | User story title                    | User story description                                                                                                                                                       | Priority | Notes                                   |
| ----- | ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------- |
| US-13 | Ask what an AI term means           | As a training-unit staff member, I want to ask what an AI term means and get the glossary definition, so that I teach the definition the public sector uses.                 | High     | F7 · O2 · Beta · Jira: new              |
| US-14 | Find the English name of an AI term | As a graduate student, I want to know the English name of an AI term from its Turkish definition, so that I can match it with the terms used in English-language literature. | Medium   | F7 · O2 · Release candidate · Jira: new |

## Acceptance criteria

### US-13 Ask what an AI term means

1. When the user asks what a term means and the glossary has an entry for it, the assistant shall give that entry's definition.
2. When the user asks about a term by its English name, the assistant shall give the glossary entry with that English name.
3. If the glossary has no entry for the term, then the assistant shall not present a definition as coming from the glossary.

### US-14 Find the English name of an AI term

1. When the assistant gives a definition from the glossary, the assistant shall show, next to the Turkish term, the English name that the glossary entry gives.
2. If the glossary entry gives no English name, then the assistant shall show only the Turkish term.
