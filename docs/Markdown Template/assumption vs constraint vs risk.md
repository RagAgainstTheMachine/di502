"The dataset will be sufficient" is a weak assumption because it's vague and it hides a real uncertainty. The fix is to rewrite it so it can be checked, and to link it to a risk.

What an assumption actually is

An assumption is something you treat as true for planning purposes without having proven it yet. It isn't a shield ("we assumed it, so it's not our fault"). It's a documented bet that you commit to verifying. A good assumption has three properties: it's specific, it's testable, and it has an owner and a date by which it will be validated. "The dataset will be sufficient" fails all three, since "sufficient" isn't defined, nobody can test it, and nobody is responsible for checking it.

A useful rewrite answers "based on what?":

"The provided dataset of ~12,000 labeled customer queries covers the 8 intent categories in scope, with at least 300 examples per category. To be verified by the data team through an exploratory analysis by the end of Sprint 1."

This version can be proven wrong early, cheaply, before it sinks the project.

How assumptions, constraints and risks relate

A constraint is a fixed limit you must work within, not something uncertain. Examples: "We may only use the dataset supplied by the client," "Delivery in 10 weeks," "Model must run on CPU." If the dataset is given and you can't collect more, that part is a constraint.

An assumption is an uncertain belief you're planning around.

A risk is an uncertain event that would hurt the project if it happens. Every important assumption has a risk on its flip side. If you assume the dataset covers the in-scope categories, the matching risk is "the dataset under-represents some categories, leading to poor performance on them." That risk gets the action plan: a mitigation (early coverage analysis, data augmentation, targeted labeling budget) and a contingency (narrow scope to well-covered categories, flag low-confidence predictions to a human).

So it's not "assumption or risk." It's both. Log the assumption, and if it's uncertain and impactful, register the corresponding risk. Many teams cross-reference them directly (A-03 ↔ R-07).

"We can't prepare for everything"

Correct, and you shouldn't try. The way out is scoping. You don't promise the model handles "all use cases." You define the intended operating domain (which users, which inputs, which languages, which categories) and explicitly list what's out of scope. Then your assumption only has to hold within that boundary. If the system fails in real life on something outside it, that's a documented limitation, not a broken assumption. If it fails inside the boundary, your validation step should have caught it, which is why validation dates matter.

Examples of better assumptions for a data/AI project

The historical data (2021–2025) is representative of the data the system will see after deployment, with no major changes expected in user behavior or input format during the project.
Labels in the dataset have an error rate below roughly 5%, to be checked by manually reviewing a random sample of 200 records.
Domain experts will be available for at least 2 hours per week for labeling questions and result review.
The client will provide access to the production environment (or a staging copy) by week 4.
Using this data for model training is permitted under the existing data agreement and privacy regulations, to be confirmed with the legal/data owner before training begins.
Stakeholders agree that an accuracy (or F1) of X on the held-out test set is acceptable for the first release.

Each one is concrete, could turn out false, and would visibly change the plan if it did. That's the sign of a useful assumption. If an assumption couldn't possibly be wrong, or being wrong wouldn't matter, it doesn't belong in the log.
