# Story Requirements for Epic E5: Clear Decline

| Epic | E5 Clear decline |
|---|---|
| Summary | AI users receive a clear decline instead of an unsupported answer, prediction or case-specific compliance verdict. |
| Document Owner | Muhammed Batuhan Tezcan (Product Owner) |
| Designer | TBD |
| Developers | Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu |
| Release Target (Sprint) | |
| Jira | |

## Requirements

| # | User story title | User story description | Priority | Points | Owner | Sprint | Notes | Jira |
|---|---|---|---|---|---|---|---|---|
| S1 | Be told when the documents have no answer | As an AI-policy researcher, I want to be told plainly when the documents have no answer, so that I look elsewhere instead of trusting a guess. | Highest | | | Sprint 2 | US-14; F5; O5; Alpha | |
| S2 | Get no guess when the documents only mention a topic | As a strategy-unit specialist, I want to hear only what the documents say when they just mention a topic, so that I do not plan on a guess. | High | | | Sprint 3 | US-15; F5; O5; Beta | |
| S3 | Get no verdict on my institution's case | As a legal-unit staff member, I want the assistant to say plainly that it does not judge my institution's own case, so that I do not act on a guess. | Highest | | | Sprint 3 | US-16; F5; O5; Beta | |

## S1 · Be told when the documents have no answer

**Acceptance criteria**

- If the documents contain nothing on the question, then the assistant shall say plainly that it cannot answer from the documents.
- If the documents contain nothing on the question, then the assistant shall give no other answer.

## S2 · Get no guess when the documents only mention a topic

**Acceptance criteria**

- If the user asks for details that a document says will be prepared later, then the assistant shall quote that passage and say the details are not in the documents.
- If the user asks for a prediction about future law or policy, then the assistant shall say that it does not make predictions.
- If the user asks for a prediction and the documents describe a plan, then the assistant shall state what the documents say about the plan.

## S3 · Get no verdict on my institution's case

**Acceptance criteria**

- If the user asks whether their own institution's plan or practice complies with the rules, then the assistant shall give no yes/no answer.
- If the user asks whether their own institution's plan or practice complies with the rules, then the assistant shall say that it does not judge a specific case.
- If the user asks this and the documents contain rules on the topic, then the assistant shall state what the documents say on those rules.
- If the user asks this and the documents contain no rule on the topic, then the assistant shall say plainly that it cannot answer.
