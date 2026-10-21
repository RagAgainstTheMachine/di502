# Story Requirements for Epic E3: Legal-Status Labels

| Epic | E3 Legal-status labels |
|---|---|
| Summary | AI users see each source's legal status and date and are told when a cited point is not law. |
| Document Owner | Muhammed Batuhan Tezcan (Product Owner) |
| Designer | TBD |
| Developers | Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu |
| Release Target (Sprint) | |
| Jira | |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Notes | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | See each source's legal status and date | As a legal-unit staff member, I want to see each source's legal status and date, so that I can tell law from plans and guidance. | Highest | | | Sprint 2 | US-11; F3; O4; Alpha | DI502-17 |
| S2 | Know in the answer when a point is not law | As a training-unit staff member, I want the answer to say when a point is not law, so that I do not teach it as law. | High | | | Sprint 3 | US-12; F3; O4; Beta | |

## S1 · See each source's legal status and date

**Acceptance criteria**

- When the assistant cites a source, the assistant shall show its legal status and date from the document inventory.
- When an answer cites sources with different legal statuses, the assistant shall show each source's own status.

## S2 · Know in the answer when a point is not law

**Acceptance criteria**

- When an answer states a point from a source that is not binding law, the assistant shall name the source's legal status in the same sentence.
