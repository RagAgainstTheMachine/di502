# Story Requirements for Epic E2: Source Transparency (v3)


| Epic                    | E2 Source transparency (charter features F2 Source reference, F3 Legal status label and F6 Collection date; objectives O2, O4) |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                                                                        |
| Designer                | TBD                                                                                                                            |
| Developers              | TBD                                                                                                                            |
| Release Target (Sprint) | Alpha (Sprint 2, 18/11/2026): US-6, US-7; Beta (Sprint 3, 09/12/2026): US-8                                                    |
| Jira                    | DI502-15                                                                                                                       |

## Requirements


| #    | User story title                                       | User story description                                                                                                                                                       | Priority | Notes                            |
| ---- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------- |
| US-6 | See the source of each answer                          | As a legal-unit staff member, I want to see which source supports each point of an answer, with a link to the official text, so that I can check each point before I use it. | Highest  | F2 · O2 · Alpha · Jira: DI502-16 |
| US-7 | Know how binding and how recent each cited document is | As a legal-unit staff member, I want to know how binding and how recent each cited document is, so that I can tell law from plans and guidance.                              | Highest  | F3 · O4 · Alpha · Jira: DI502-17 |
| US-8 | See how current the documents are                      | As an AI-policy researcher, I want to see how current the documents are, so that I know if later changes may affect an answer.                                               | High     | F6 · O2 · Beta · Jira: DI502-18  |

## Acceptance criteria

### US-6 See the source of each answer

1. When the assistant gives an answer, the assistant shall name the document, and the article, section, action, measure or glossary entry, of each source that supports a factual statement in the answer.
2. When the assistant cites an article or section, the assistant shall cite the one that contains the supporting passage.
3. When the assistant cites a document, the assistant shall show a link to its official URL from the document inventory.
4. When an answer cites more than one source, the assistant shall show, in the same sentence as each factual statement or directly after it, the source that supports that statement.

### US-7 Know how binding and how recent each cited document is

1. When the assistant cites a source, the assistant shall show its legal status from the document inventory.
2. When the assistant cites a source, the assistant shall show its date from the document inventory.
3. When an answer cites sources with different legal statuses, the assistant shall show each source's own status.

### US-8 See how current the documents are

1. The assistant shall show the collection date on the chat page.
2. If the user asks about the current legal state of a document, then the assistant shall say that its answer reflects the documents as of the collection date.

## Terms

- **Current legal state:** whether a document or provision is in force, in which version, or whether it has been amended, replaced or repealed.
