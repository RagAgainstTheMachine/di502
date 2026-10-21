# Story Requirements for Epic E1.2: Duties, Deadlines and Provisions

| Epic | E1.2 Duties, deadlines and provisions |
|---|---|
| Summary | AI users find the institution responsible for an action, its required work and deadline, or a numbered provision in the approved documents. |
| Document Owner | Muhammed Batuhan Tezcan (Product Owner) |
| Designer | TBD |
| Developers | Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu |
| Release Target (Sprint) | |
| Jira | |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Notes | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | Find out who leads an action | As a strategy-unit specialist, I want to know which institution leads an action, so that I know whom we must work with. | High | | | Sprint 2 | US-4; F1; O2; Alpha | |
| S2 | Find out what must be done and by when | As a strategy-unit specialist, I want to know what public institutions must do and by when, so that I can plan our AI work on time. | High | | | Sprint 2 | US-5; F1; O2; Alpha | |
| S3 | Look up a provision by its number | As a legal-unit staff member, I want to look up an article, action or measure by its number, so that I can read what it says without searching the document. | High | | | Sprint 3 | US-6; F1; O2; Beta | |

## S1 · Find out who leads an action

**Acceptance criteria**

- When the user asks who is responsible for an action or measure, the assistant shall name the lead institution as the source names it.
- When the source also names cooperating institutions, the assistant shall list them separately from the lead.
- If the source names no lead institution, then the assistant shall say so.

## S2 · Find out what must be done and by when

**Acceptance criteria**

- When the user asks what must be done, the assistant shall list the steps that the source gives.
- When the source gives a deadline, the assistant shall state it in the same form as the source.
- If the source gives no deadline, then the assistant shall say so.

## S3 · Look up a provision by its number

**Acceptance criteria**

- When the user gives an article, action or measure number from the collection, the assistant shall answer from that provision.
