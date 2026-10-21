# Story Requirements for Epic E1: Policy Question Answering

> **Superseded on 20/10/2026** by [User Story Map v2](02-user-story-map-v2.md) and its story requirement pages. Kept as the record of User Story Map v1.

This will be a space for you to elaborate on stories and requirements for a given epic. (Duplicate page for more story epics.)

| Epic | E1 Policy Question Answering (charter features F1, F4; objectives O1, O2, O3) |
|---|---|
| Document Owner | TBD |
| Designer | TBD |
| Developers | TBD |
| Release Target (Sprint) | TBD at sprint planning |

## Requirements

For more info you can visit: https://www.atlassian.com/agile/product-management/requirements.

| # | User story title | User story description | Priority | Notes |
|---|---|---|---|---|
| US-1 | Ask AI-policy questions in Turkish | As a strategy-unit staff member, I want to ask questions about Türkiye's AI policy in Turkish in my own words, so that I can brief management without reading each document myself. | Highest | F1 |
| US-2 | Ask follow-up questions | As a legal-unit staff member, I want to continue asking question without repeating my earlier question, so that I can narrow down a rule quickly. | High | F4 |
| US-3 | Get answers that combine several documents | As a training-unit staff member, I want one answer that brings together what different documents say on the same topic, so that I can teach the full picture in one session. | High | F1 (multi-hop question type) |

## Acceptance criteria

### US-1 Ask AI-policy questions in Turkish
- The user can type a question in Turkish and submit it.
- The answer is written in Turkish.
- For each answerable test question in the evaluation set that is not a follow-up question, the answer matches the reference answer.

### US-2 Ask follow-up questions
- When a follow-up question refers to something in the previous exchange, the answer interprets the reference as that item and answers about it.
- The user can start a new conversation that keeps no context from the previous one.

### US-3 Get answers that combine several documents
- For a test question whose reference answer draws on more than one document, the answer includes the relevant information from each of those documents.
- Each part of the answer cites the document it comes from.
