# Story Requirements for Epic E1.3: Answers Across Documents

| Epic | E1.3 Answers across documents |
|---|---|
| Summary | AI users receive answers that combine relevant documents and distinguish positions where documents disagree. |
| Document Owner | Muhammed Batuhan Tezcan (Product Owner) |
| Designer | TBD |
| Developers | Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu |
| Release Target (Sprint) | |
| Jira | |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Notes | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | Get one answer from several documents | As a training-unit staff member, I want one answer that brings all relevant documents together, so that I can teach the full picture. | High | | | Sprint 3 | US-7; F1; O2; Beta | DI502-14 |
| S2 | See where documents disagree | As an AI-policy researcher, I want to see where documents take different positions, so that I can report the difference correctly. | Medium | | | Sprint 4 | US-8; F1; O2; Release candidate | |

## S1 · Get one answer from several documents

**Acceptance criteria**

- When a question needs more than one document, the assistant shall include the relevant point from each document.
- When the user asks how a Development Plan policy is carried out, the assistant shall give the Annual Programme measures for it.

## S2 · See where documents disagree

**Acceptance criteria**

- When documents take different positions on the question, the assistant shall say which document holds each position.
- When the assistant gives different positions, the assistant shall not say which one is right.
