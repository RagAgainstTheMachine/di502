"No PII stored" can't be both a constraint and an out-of-scope activity in the same wording, because the two sections answer different questions.

The distinction

A constraint is a rule that limits how the in-scope work is done. An out-of-scope activity is work the team won't do at all. "No PII stored" is phrased as a rule, which is why it reads like a constraint. But the reviewer is right that the underlying decision also removes work from the project. So write it as three statements, one per section, each saying something different and pointing to the others.

Section	What it says	Example wording
Constraint	The rule the system must obey	"The system shall not persist personally identifiable information (e.g., names, email addresses, national ID numbers) in any database, log, or vector index."
Activities in scope	The work you do because of the constraint	"Implement PII detection and masking on user inputs before logging." "Configure logs to retain only anonymised interaction data."
Activities out of scope	The features you're giving up because of it	"User accounts, personal profiles, and saved conversation history linked to an identity."

Read together, they tell a reviewer: here's the rule, here's what we'll build to comply with it, and here's what we won't build because of it. None of them repeats another.

Why the in-scope side matters most

Teams often skip the in-scope entry, and that's what makes the constraint look hollow. Users will type their names, emails or account numbers into a chatbot whether you invite them to or not. So "no PII stored" isn't automatically true just because you didn't build a profile feature. It takes active work to enforce, and that work belongs in the activities in focus, the backlog, and the estimates.

This also connects to your earlier question. The uncertain part becomes a risk: "Users submit PII in free-text queries, and it ends up in logs or the retrieval index." The masking activity is the mitigation. Your test or review of the logs is how you check it.

Knock-on effect on your stories

Once this is in the charter, any user story that needs remembered identity creates a conflict with it. Examples include "As a returning analyst, I want to see my previous questions…" Your course materials treat that as an external inconsistency. Either drop such stories, or rewrite them so the history lives only in the session and isn't stored.
