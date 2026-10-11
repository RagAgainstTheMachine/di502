# Major Activities

Expand on the scope definition by outlining the major activities required to complete the project. Structure these around the AI system life cycle stages of ISO/IEC 5338 [1], listed below.

Include activities such as project management, feature engineering, model training, performance evaluation and analysis.

Mark each activity as In Scope or Out of Scope to reduce ambiguity.

Add rows as required. The table should give a summary view; add narrative explanation below it where more detail is needed. Activities can be linked to Jira from this page.

## Life cycle stages
 
Give every activity one stage from this table. The stage names and the processes in each stage come from ISO/IEC 5338 [1]; the typical activities are paraphrased for this course.
 
| Stage | Typical activities | ISO/IEC 5338 processes in this stage |
|---|---|---|
| **Inception** | Define the problem, the AI customer's needs and the success criteria; set model requirements; decide whether AI is needed at all | 6.4.1 Business or mission analysis; 6.4.2 Stakeholder needs and requirements definition; 6.4.3 System requirements definition |
| **Design and development** | Architecture and design; acquire, label, explore, clean and prepare data; protect sensitive data; feature engineering; train and tune models; integrate components | 6.4.4–6.4.6; 6.4.7 Knowledge acquisition; 6.4.8 AI data engineering; 6.4.9 Implementation; 6.4.10 Integration |
| **Verification and validation** | Test the model and system before deployment; check them against the AI customer's needs | 6.4.11 Verification; 6.4.13 Validation |
| **Deployment** | Move the model and system into the environment where AI users reach it | 6.4.12 Transition |
| **Operation and monitoring** | Run the system; fix and retrain it when needed | 6.4.15 Operation; 6.4.16 Maintenance |
| **Continuous validation** | Monitor data drift, concept drift and other changing requirements after deployment; decide when to retrain | 6.4.14 Continuous validation |
| **Re-evaluation** | Review results against the original needs; feed changes back to Inception or Design and development | 6.3.8 Quality assurance; 6.4.2; 6.4.13 |
| **Retirement** | Decommission the system and its data | 6.4.17 Disposal |
 
Project management work (sprint planning, documentation, reviews, risk tracking) runs across every stage, as risk management and governance do in the standard [1]. Write **All stages** for these rows.
 
Stages group work in a rough order, but they need not happen one after another. In agile work, stages can run at the same time and can repeat [1].

## In Scope and Out of Scope

| Status | What it means | Question it answers |
|---|---|---|
| **In Scope** | Work the team will do | What will we build or carry out? |
| **Out of Scope** | Work the team will not do at all | What are we deliberately not building? |

An out-of-scope activity is not the same as a constraint. A constraint is a rule that limits how the in-scope work is done; it goes in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md). If you want to show that the project's scope is narrow (for example, you plan no information-elicitation phase), list that here as Out of Scope. Limits on the system's inputs, such as a user-input boundary or English-only text, are constraints.

## Activities that come from a constraint

Many constraints create work and remove work at the same time. Write the decision as three statements, one per place, each pointing to the others:

| Where | What it says | Example wording |
|---|---|---|
| Constraint ([Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md)) | The rule the system must obey | "The system shall not persist personally identifiable information (e.g., names, email addresses, national ID numbers) in any database, log, or vector index." |
| In Scope (this page) | The work you do because of the constraint | "Implement PII detection and masking on user inputs before logging." "Configure logs to retain only anonymised interaction data." |
| Out of Scope (this page) | The features you give up because of it | "User accounts, personal profiles, and saved conversation history linked to an identity." |

**Do not skip the In Scope row.** Users will type names, emails or account numbers into a chatbot whether you invite them to or not. A rule such as "no PII stored" is not true just because you did not build a profile feature; enforcing it takes work. That work belongs here, in the backlog and in the estimates. Count its effort in [Cost & Funding](03-project-canvas_v2/07-cost-and-funding.md).

The uncertain part becomes a risk in [Risks](03-project-canvas_v2/11-risks.md), and the in-scope activity is its mitigation. For the example above, the risk is "Users submit PII in free-text queries, and it ends up in logs or the retrieval index".

## Knock-on effect on user stories

Once a constraint is in the charter, a user story that contradicts it is an inconsistency between documents. The review error types call this an External Inconsistency. For example, "As a returning analyst, I want to see my previous questions" contradicts a no-PII rule. Either drop such a story, or rewrite it so the history lives only in the session and is not stored.

## Rules

1. Every activity has exactly one stage from the life cycle table above, spelled as there, or **All stages** for project management work.
2. Every activity is marked In Scope or Out of Scope.
3. Every Out of Scope row says why in its Description, as row 2 below does.
4. Every constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) that creates work has at least one In Scope row here, and every constraint that removes features has at least one Out of Scope row here.
5. Rows created by a constraint name the constraint ID in their Description (for example "Because of C-03").
6. User authentication and PII storage, if you do not plan them, are listed as Out of Scope.
7. Activities do not increase the scope of the project beyond the first proposal.

## What doesn't belong here

- **Rules the system must obey** go in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) as constraints.
- **What could go wrong** with an activity goes in [Risks](03-project-canvas_v2/11-risks.md).
- **The order in which activities must happen**, when one blocks another, goes in [Dependencies](03-project-canvas_v2/06-dependencies.md).
- **Effort in person-hours** goes in [Cost & Funding](03-project-canvas_v2/07-cost-and-funding.md).

## Activities
 
| # | Stage | Activity | Description | Status | Jira Task |
|---|---|---|---|---|---|
| 1 | Inception | Define chatbot purpose, users, and success criteria | Completed as part of project chartering. (See Project Executive Summary above) | In Scope | |
| 2 | Inception | Market/competitive analysis of existing chatbot products | Not needed for an academic proof-of-concept | Out of Scope | |
| 3 | | | | | |
 
## Example (illustrative only)
 
An excerpt from a longer table for a legal research assistant (a RAG chatbot over legal documents). It shows the rows created by constraints C-03 and C-04 in the example on `03-assumptions-and-constraints.md`.
 
| # | Stage | Activity | Description | Status | Jira Task |
|---|---|---|---|---|---|
| 7 | Design and development | Mask PII in user inputs before logging | Because of C-03. Detect names, emails and ID numbers in queries and mask them before any log write. Mitigation for R-03. | In Scope | (link) |
| 8 | Deployment | Configure logs to keep only anonymized interaction data | Because of C-03. | In Scope | (link) |
| 12 | Design and development | User accounts, personal profiles and saved conversation history | Because of C-03: these would require storing PII. | Out of Scope | |
| 13 | Design and development | Multi-turn dialogue memory | Because of C-04: the system handles single-turn questions only. | Out of Scope | |

## Checklist before submitting

- [ ] Every activity has one ISO/IEC 5338 life cycle stage, or All stages (rule 1)
- [ ] Every activity is marked In Scope or Out of Scope (rule 2)
- [ ] Every Out of Scope row says why (rule 3)
- [ ] Every work-creating constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) has an In Scope row, and every feature-removing constraint has an Out of Scope row (rule 4)
- [ ] Rows created by a constraint name its ID (rule 5)
- [ ] User authentication and PII storage are listed as Out of Scope if you do not plan them (rule 6)
- [ ] No activity goes beyond the first proposal's scope (rule 7)
