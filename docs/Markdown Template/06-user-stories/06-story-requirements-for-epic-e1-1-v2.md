# Story Requirements for Epic E1.1: Asking and Getting Answers (v2)

> **Superseded on 25/10/2026** by [User Story Map (v3)](15-user-story-map-v3.md), the current version. Epic IDs changed between versions; see the [epic lineage](README.md#epic-lineage). Kept as the record of User Story Map (v2).

| Epic | E1.1 Asking and getting answers (charter feature F1 Plain-language questions; objectives O1, O2) |
|---|---|
| Document Owner | Muhammed Batuhan Tezcan (Product Owner) |
| Designer | TBD |
| Developers | TBD |
| Release Target (Sprint) | Alpha (Sprint 2, 18/11/2026): US-1, US-2 |
| Jira | DI502-11 |

## Requirements

| # | User story title | User story description | Priority | Notes |
|---|---|---|---|---|
| US-1 | Ask a question about AI policy | As a strategy-unit specialist, I want to ask a question about AI policy and get an answer, so that I do not have to search each document. | Highest | F1 · O2 · Alpha · Jira: DI502-12 |
| US-2 | Get answers only from the official texts | As a legal-unit staff member, I want answers to say only what the official documents say, so that I can use them in official work. | Highest | F1 · O2 · Alpha · Jira: new |

## Acceptance criteria

### US-1 Ask a question about AI policy

1. When the user asks a question in Turkish, the assistant shall answer in Turkish.
2. When the user asks a question that a passage in the collection answers, the assistant shall state the key points that this passage gives.

**Verified by:** for each general factual question in the evaluation set (tag `general`: questions that no other story checks), a team member checks that the answer states every key point listed in the question's reference answer.

### US-2 Get answers only from the official texts

1. When the assistant answers an in-scope question, the assistant shall make only statements that a passage in the collection supports.

**Verified by:** a second team member checks every statement in the 30 in-scope answers.
