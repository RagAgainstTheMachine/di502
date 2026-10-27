# Story Requirements for Epic E5: Clear Decline (v2)


| Epic                    | E5 Clear decline (charter feature F5 Clear decline; objective O5)              |
| ----------------------- | ------------------------------------------------------------------------------ |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                        |
| Designer                | TBD                                                                            |
| Developers              | TBD                                                                            |
| Release Target (Sprint) | Alpha (Sprint 2, 18/11/2026): US-14; Beta (Sprint 3, 09/12/2026): US-15, US-16 |
| Jira                    |                                                                                |

## Requirements


| #     | User story title                                     | User story description                                                                                                                               | Priority | Notes                          |
| ----- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------ |
| US-14 | Be told when the documents have no answer            | As an AI-policy researcher, I want to be told plainly when the documents have no answer, so that I look elsewhere instead of trusting a guess.       | Highest  | F5 · O5 · Alpha · Jira: new |
| US-15 | Get no guess when the documents only mention a topic | As a strategy-unit specialist, I want to hear only what the documents say when they just mention a topic, so that I do not plan on a guess.          | High     | F5 · O5 · Beta · Jira: new  |
| US-16 | Get no verdict on my institution's case              | As a legal-unit staff member, I want the assistant to say plainly that it does not judge my institution's own case, so that I do not act on a guess. | Highest  | F5 · O5 · Beta · Jira: new  |

## Acceptance criteria

### US-14 Be told when the documents have no answer

1. If the documents contain nothing on the question (tag `out-of-scope`), then the assistant shall say plainly that it cannot answer from the documents.
2. If the documents contain nothing on the question, then the assistant shall give no other answer.

### US-15 Get no guess when the documents only mention a topic

1. If the user asks for details that a document says will be prepared later (tag `missing-details`), then the assistant shall quote that passage and say the details are not in the documents.
2. If the user asks for a prediction about future law or policy (tag `prediction`), then the assistant shall say that it does not make predictions.
3. If the user asks for a prediction and the documents describe a plan, then the assistant shall state what the documents say about the plan.

### US-16 Get no verdict on my institution's case

1. If the user asks whether their own institution's plan or practice complies with the rules (tag `compliance-judgement`), then the assistant shall give no yes/no answer.
2. If the user asks whether their own institution's plan or practice complies with the rules, then the assistant shall say that it does not judge a specific case.
3. If the user asks this and the documents contain rules on the topic, then the assistant shall state what the documents say on those rules.
4. If the user asks this and the documents contain no rule on the topic, then the assistant shall say plainly that it cannot answer.
