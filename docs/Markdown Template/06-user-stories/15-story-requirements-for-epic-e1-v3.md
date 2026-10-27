# Story Requirements for Epic E1: Asking and Getting Answers (v3)


| Epic                    | E1 Asking and getting answers (charter feature F1 Plain-language questions; objectives O1, O2) |
| ----------------------- | ---------------------------------------------------------------------------------------------- |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                                        |
| Designer                | TBD                                                                                            |
| Developers              | TBD                                                                                            |
| Release Target (Sprint) | Alpha (Sprint 2, 18/11/2026): US-1, US-2, US-3; Beta (Sprint 3, 09/12/2026): US-4, US-5        |
| Jira                    | DI502-11                                                                                       |

## Requirements


| #    | User story title                                                  | User story description                                                                                                                                                             | Priority | Notes                            |
| ---- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------- |
| US-1 | Ask a question about AI policy                                    | As a strategy-unit specialist, I want to ask a question about AI policy and get an answer from the official documents, so that I do not have to search each document.              | Highest  | F1 · O2 · Alpha · Jira: DI502-12 |
| US-2 | Find out what an AI policy action or measure requires and by when | As a strategy-unit specialist, I want to know what an AI policy action or measure requires of public institutions and by when, so that I can plan our AI work on time.             | High     | F1 · O2 · Alpha · Jira: new      |
| US-3 | Find out who is responsible for an action                         | As a strategy-unit specialist, I want to know which institutions are responsible for an action, so that I know whom we must work with.                                             | High     | F1 · O2 · Alpha · Jira: new      |
| US-4 | Read a provision I know by number                                 | As a legal-unit staff member, I want to read what a specific article, action or measure says when I know its specific number, so that I do not have to search the document for it. | High     | F1 · O2 · Beta · Jira: new       |
| US-5 | See what all the documents say on a topic                         | As a training-unit staff member, I want to know what the official documents together say about a topic, so that I can teach the full picture.                                      | High     | F1 · O2 · Beta · Jira: DI502-14  |

## Acceptance criteria

### US-1 Ask a question about AI policy

1. When the user asks a question in Turkish, the assistant shall answer in Turkish.
2. When the official documents contain the answer to the user's question, the assistant shall give the complete answer, not only part of it.
3. When the assistant returns an answer, each factual statement in the answer shall be supported by text in the official documents.

### US-2 Find out what an AI policy action or measure requires and by when

1. When the user asks what a specific AI policy action or measure requires, the assistant shall state what the official documents say is to be done under it.
2. When the official documents give a time limit or date for that action or measure, the assistant shall state it in the form the documents give it.
3. If the official documents give no time limit or date for that action or measure, then the assistant shall say so.

### US-3 Find out who is responsible for an action

1. When the user asks who is responsible for an action or measure, the assistant shall name each institution that the official documents state as responsible for it, using the names the documents give.
2. When the official documents also name institutions that cooperate on that action or measure, the assistant shall list them separately from the responsible institutions.
3. If the official documents name no responsible institution for that action or measure, then the assistant shall say so.

### US-4 Read a provision I know by number

1. When the user gives the number of a provision that exists in the official documents, the assistant shall state what that provision says.
2. When the number the user gives matches provisions in more than one official document, the assistant shall give each of them and name the document of each.
3. If no provision with the number the user gives exists in the official documents, then the assistant shall say so.

### US-5 See what all the documents say on a topic

1. When more than one official document answers the user's question, in whole or in part, the assistant shall include in its answer the relevant point from each of those documents.

## Terms

- **Official documents:** the documents listed in the document inventory.
- **Factual statement:** a statement about what the documents contain or require. The assistant's own notices, such as saying that it cannot answer, are not factual statements.
- **Supported:** a reviewer can find text in the official documents that says the same thing, in the same words or other words, or says it when read together with other text in them. For a document's legal status and date, its entry in the document inventory is the support.
- **Responsible institution:** an institution that a document marks as responsible for an action or measure ("Ana sorumlu" in the Action Plan, "(S)" in the Annual Programme). Other institutions named in the same place are cooperating institutions.
- **AI policy action or measure:** a numbered item in an official document that sets out work for public institutions to do under AI policy and names the institutions responsible for it.
- **Time limit or date:** a period or date stated in the item itself.
- **Provision:** an article of a law, or a numbered action or measure of a policy document, among the official documents.
- **Answers in part:** an official document answers a question in part when it has text that gives some of the information the user asked for. A document that only names the subject of the question does not.
