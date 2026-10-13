# User Story Map v1

Plese present the full feature-epic-story-task hierarchy in a map.

Version 1, 11 October 2026. Features are taken from the Project Executive Summary (section 3.1, F1–F6). Jira keys and story points are filled in after the stories are created in Jira and estimated with poker planning.

## Epics


| Epic | Name                      | Charter features                                             | Objectives served | Details                                                                |
| ---- | ------------------------- | ------------------------------------------------------------ | ----------------- | ---------------------------------------------------------------------- |
| E1   | Policy Question Answering | F1, F4                                                       | O1, O2, O3        | [Story requirements for Epic E1](03-story-requirements-for-epic-e1.md) |
| E2   | Source Transparency       | F2, F3, F6                                                   | O2, O4            | [Story requirements for Epic E2](04-story-requirements-for-epic-e2.md) |
| E3   | Safe and Trustworthy Use  | Charter constraint: no personal data is requested from users | —                | [Story requirements for Epic E3](05-story-requirements-for-epic-e3.md) |

## Map: feature → epic → story → task


| Feature (charter 3.1)                  | Epic | User story                                          | Jira key | Story points | Known tasks                                                                                                                    |
| -------------------------------------- | ---- | --------------------------------------------------- | -------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------ |
| F1 Plain-language questions            | E1   | US-1 Ask AI-policy questions in Turkish             | gi       |              | Type in the text of D04 (Circular 2026/9); extract the AI-related Tedbir entries of D08; rebuild the D05 recommendation tables |
| F1 Plain-language questions            | E1   | US-3 Get answers that combine several documents     |          |              | —                                                                                                                             |
| F4 Follow-up questions                 | E1   | US-2 Ask follow-up questions                        |          |              | —                                                                                                                             |
| F2 Source reference                    | E2   | US-4 See the source of each answer                  |          |              | Record the official URL and download date of each corpus document                                                              |
| F3 Legal status label                  | E2   | US-5 See each source's legal status                 |          |              | Align the legal-status label set in charter F3 with the document inventory                                                     |
| F6 Collection date                     | E2   | US-6 See how current the collection is              |          |              | —                                                                                                                             |
| F5 Referral for unanswerable questions | —   | **No story**                                        |          |              | —                                                                                                                             |
| Constraint: no personal data requested | E3   | US-7 Use the assistant without giving personal data |          |              | —                                                                                                                             |

Tasks for building the system (retrieval, generation, interface, evaluation) are added at sprint planning.
