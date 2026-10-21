# Story Requirements for Epic E2: Cited Answers

| Epic | E2 Cited answers |
|---|---|
| Summary | AI users see the official source supporting each answer and each part of a multi-source answer. |
| Document Owner | Muhammed Batuhan Tezcan (Product Owner) |
| Designer | TBD |
| Developers | Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu |
| Release Target (Sprint) | |
| Jira | DI502-15 |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Notes | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | See the source of each answer | As a legal-unit staff member, I want to see the source of each answer with a link to the official text, so that I can check it before I use it. | Highest | | | Sprint 2 | US-9; F2; O2; Alpha | DI502-16 |
| S2 | See the source of each part of an answer | As a graduate student, I want each part of an answer to show its own source, so that I can cite each point correctly. | High | | | Sprint 3 | US-10; F2; O2; Beta | |

## S1 · See the source of each answer

**Acceptance criteria**

- When the assistant answers an in-scope question, the assistant shall name the document and the article, section, action, measure or glossary entry of each source it used.
- When the assistant cites an article or section, the assistant shall cite the one that contains the supporting passage.
- When the assistant cites a document, the assistant shall show a link to its official URL from the document inventory.

## S2 · See the source of each part of an answer

**Acceptance criteria**

- When an answer uses more than one source, the assistant shall place each citation next to the part it supports.
