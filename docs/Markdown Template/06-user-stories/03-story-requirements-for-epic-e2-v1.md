# Story Requirements for Epic E2: Source Transparency (v1)

> **Superseded on 20/10/2026** by [User Story Map (v2)](05-user-story-map-v2.md) and since 25/10/2026 by [User Story Map (v3)](15-user-story-map-v3.md), the current version. Epic IDs changed between versions; see the [epic lineage](README.md#epic-lineage). Kept as the record of User Story Map (v1).

This will be a space for you to elaborate on stories and requirements for a given epic. (Duplicate page for more story epics.)

| Epic | E2 Source Transparency (charter features F2, F3, F6; objectives O2, O4) |
|---|---|
| Document Owner | TBD |
| Designer | TBD |
| Developers | TBD |
| Release Target (Sprint) | TBD at sprint planning |

## Requirements

For more info you can visit: https://www.atlassian.com/agile/product-management/requirements.

| # | User story title | User story description | Priority | Notes |
|---|---|---|---|---|
| US-4 | See the source of each answer | As a legal-unit staff member, I want to see the document and the article or section behind each answer, with a link to the official source, so that I can verify it before using it in a written opinion. | Highest | F2; depends on the official URLs in the document inventory |
| US-5 | See each source's legal status | As a training-unit staff member, I want each cited source to show its legal status and date, so that I don't teach a plan or a recommendation as binding law. | Highest | F3 |
| US-6 | See how current the collection is | As an AI-policy researcher, I want to see the date up to which the document collection is current, so that I know whether later developments may change an answer. | Medium | F6 |

## Acceptance criteria

### US-4 See the source of each answer
- Every answer to an in-scope question names the document title and the article or section number for each source used.
- Each cited document has a link to its official URL as recorded in the document inventory.
- Selecting the link opens the official source.

### US-5 See each source's legal status
- Each cited source shows the legal status and date recorded for it in the document inventory.
- When one answer cites sources with different legal statuses, each source shows its own status.
- When a cited source is a recommendation, plan or bill, the answer does not present its content as an obligation in force.

### US-6 See how current the collection is
- The collection date is visible on the page before the user asks a question.
- For each test question marked as time-sensitive in the evaluation set, the answer states the date of each source it relies on.
- For each test question marked as time-sensitive in the evaluation set, the answer contains no statement about events after the collection date.
