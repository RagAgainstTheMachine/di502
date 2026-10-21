# Story Requirements for Epic E1.1: Asking and Getting Answers

| Epic | E1.1 Asking and getting answers |
|---|---|
| Summary | AI users ask Turkish questions about Türkiye's AI policy and receive answers supported only by the approved official documents. |
| Document Owner | Muhammed Batuhan Tezcan (Product Owner) |
| Designer | TBD |
| Developers | Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu |
| Release Target (Sprint) | Sprint 2 |
| Jira | DI502-11 |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Notes | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | Ask a question about AI policy | As a strategy-unit specialist, I want to ask a question about AI policy and get an answer, so that I do not have to search each document. | Highest | | | Sprint 2 | US-1; F1; O2; Alpha | DI502-12 |
| S2 | Get answers only from the official texts | As a legal-unit staff member, I want answers to say only what the official documents say, so that I can use them in official work. | Highest | | | Sprint 2 | US-2; F1; O2; Alpha | |

## S1 · Ask a question about AI policy

**Acceptance criteria**

- When the user asks a question in Turkish, the assistant shall answer in Turkish.
- When the user asks a question that a passage in the collection answers, the assistant shall state the key points that this passage gives.

**Details**

Verified by: for each general factual question in the evaluation set, a team member checks that the answer states every key point listed in the question's reference answer.

## S2 · Get answers only from the official texts

**Acceptance criteria**

- When the assistant answers an in-scope question, the assistant shall make only statements that a passage in the collection supports.

**Details**

Verified by: a second team member checks every statement in the 30 in-scope answers.
