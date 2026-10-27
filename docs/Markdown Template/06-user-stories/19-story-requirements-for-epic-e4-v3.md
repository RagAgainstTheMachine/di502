# Story Requirements for Epic E4: Clear Decline (v3)


| Epic                    | E4 Clear decline (charter feature F5 Clear decline; objective O5)              |
| ----------------------- | ------------------------------------------------------------------------------ |
| Document Owner          | Muhammed Batuhan Tezcan (Product Owner)                                        |
| Designer                | TBD                                                                            |
| Developers              | TBD                                                                            |
| Release Target (Sprint) | Alpha (Sprint 2, 18/11/2026): US-10; Beta (Sprint 3, 09/12/2026): US-11, US-12 |
| Jira                    | new                                                                            |

## Requirements


| #     | User story title                            | User story description                                                                                                                                                         | Priority | Notes                       |
| ----- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------- |
| US-10 | Be told when the documents have no answer   | As an AI-policy researcher, I want to be told plainly when the documents have no answer, so that I look elsewhere instead of trusting a guess.                                 | Highest  | F5 · O5 · Alpha · Jira: new |
| US-11 | Know what is mentioned but not prepared yet | As a strategy-unit specialist, I want to know when the documents only mention something that is still to be prepared, so that I do not plan on details that are not available. | High     | F5 · O5 · Beta · Jira: new  |
| US-12 | Find the rules for my institution's case    | As a legal-unit staff member, I want to know what the documents say about my institution's situation, so that I can judge compliance myself.                                   | Highest  | F5 · O5 · Beta · Jira: new  |

## Acceptance criteria

### US-10 Be told when the documents have no answer

1. If the documents contain nothing on the question, then the assistant shall say plainly that it cannot answer from the documents.
2. If the documents contain nothing on the question, then the assistant shall give no other answer.

### US-11 Know what is mentioned but not prepared yet

1. If the user asks for details that a document says will be prepared later, then the assistant shall quote that passage and say the details are not in the documents.
2. If the user asks for a prediction about future law or policy, then the assistant shall say that it does not make predictions.
3. If the user asks for a prediction and the documents describe a plan, then the assistant shall state what the documents say about the plan.

### US-12 Find the rules for my institution's case

1. If the user asks whether their own institution's plan or practice complies with the rules, then the assistant shall give no yes/no answer.
2. If the user asks whether their own institution's plan or practice complies with the rules, then the assistant shall say that it does not judge a specific case.
3. If the user asks this and the documents contain rules on the topic, then the assistant shall state what the documents say on those rules.
4. If the user asks this and the documents contain no rule on the topic, then the assistant shall say plainly that it cannot answer.
