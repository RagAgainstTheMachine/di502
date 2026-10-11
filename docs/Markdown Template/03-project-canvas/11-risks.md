# Risks

Record here the strategic risks identified at the start of the project. Write each risk as an **event** that could happen, not as a general worry: "Recall@5 on the evaluation set stays below 0.60 at the end of Sprint 3", not "the model fails".

## Risks, assumptions and constraints

A risk is an uncertain event that would hurt the project if it happens. It is connected to two other entries in the charter:

- **Every assumption has a risk on its flip side.** Each assumption in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) has an ID (A-01, …) and names its linked risk. Register that risk here, give it an ID (R-01, …), and write the assumption's ID in **Linked to**. The IDs must point both ways. Example: the assumption "the dataset covers the in-scope categories" has the risk "the dataset under-represents some categories, leading to poor performance on them".
- **The uncertain part of a constraint is a risk.** A constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) is a fixed limit, but complying with it can fail. The in-scope activity in [Major Activities](03-project-canvas_v2/04-major-activities.md) that enforces the constraint is the risk's mitigation. Example: the constraint "no PII is stored" has the risk "users submit PII in free-text queries, and it ends up in logs or the retrieval index"; PII masking is the mitigation.

A risk can also come from a dependency in [Dependencies](03-project-canvas_v2/06-dependencies.md), for example an external API that changes or becomes unavailable. Write the dependency's row number in **Linked to**.

## How to fill in each risk

Each risk has three parts that act at different times. Keep them separate.

| Field | When it acts | Question it answers |
|---|---|---|
| **Mitigation** | **Before** the risk happens | How do I lower its probability or impact? |
| **Contingency plan (B plan)** | **After** the risk happens | If it happens anyway, what will I do? |
| **Probability / Impact** | The situation **after** mitigation | Given the mitigation, how likely is it and how bad would it be? |

**Probability is residual probability:** what remains after the mitigation is applied. Do not write "we will try several models, so probability is 1". The mitigation is already counted. If your mitigation really brings the probability down to 1, the item is not a risk.

### Probability (1–5)

| Value | Meaning |
|---|---|
| 1 | Very low (&lt;10%): rare in the literature, no sign in pilot tests |
| 2 | Low (10–30%): possible, but only under special conditions |
| 3 | Medium (30–50%): seen in about half of similar projects |
| 4 | High (50–75%): typical in this area; it would be a surprise if it did not happen |
| 5 | Very high (>75%): almost certain. If it is basically going to happen, treat it as a constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md). If some uncertainty remains, keep it as an assumption in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) and link this risk to it |

Every probability value needs a **basis**, written next to it: a pilot measurement, the literature, a data profile (e.g., the class or category distribution), a third-party dependency, or team experience. "3, because it feels medium" cannot be defended. "3, because the pilot retrieval test gave Recall@5 = 0.52" can.

### Impact (1–5)

Rate impact by the **worst** of the three columns:

| Value | Schedule | Budget (incl. cloud credits) | Target / Scope |
|---|---|---|---|
| 1 | &lt;2 weeks | &lt;2% | Not noticeable |
| 2 | 2–4 weeks | 2–5% | A secondary metric is affected |
| 3 | 1–2 months | 5–10% | A technical requirement is partly unmet |
| 4 | 2–4 months | 10–20% | An acceptance criterion is not met |
| 5 | >4 months | >20% | The output is unacceptable; the objective is not achieved |

**A risk that threatens an acceptance criterion or success criterion has an impact of at least 4.**

### Risk score and what each band requires

**Risk score = Probability × Impact** (1–25).

| Score | Band | Required |
|---|---|---|
| 1–4 | Low | Monitoring is enough |
| 5–9 | Medium | Define a mitigation |
| 10–14 | High | Mitigation **and** trigger **and** contingency plan **and** named owner are all required |
| 15–25 | Critical | Review the project design. Also explain below the table when the risk will be re-evaluated and which early measurement will test it |

A healthy table has a few high risks, mostly medium ones and a few low ones. If every row is 1–2, it reads as "no risk analysis was done". If every row is 4–5, the project looks infeasible.

### Contingency plan: three-question test

Ask these three questions of every contingency plan:

1. **Would I have done this anyway?** If yes, it belongs in the Major Activities, not here. "Try different models", "tune hyperparameters" and "keep testing and optimizing" are not contingency plans.
2. **What is the trigger?** A contingency plan needs a **numeric threshold** and a **date or sprint**. Write "If groundedness on the evaluation set is &lt; 0.70 at the end of Sprint 4, …", not "If performance stays low, …".
3. **Who is the owner?** Name the person who decides to narrow the scope, switch the model or renegotiate the target with the AI customer. "The project team" is not an owner. Every member manages the project in some capacity, so an owner is always a named person, together with the role they hold in [Project Organization](03-project-canvas_v2/08-project-organization.md).

| Not a contingency plan | Contingency plan |
|---|---|
| "Different models will be compared." | "If the target is not met, the system is released only for the categories that meet it; the rest stay manual." |
| "Expert validation will be done." | "If label agreement is κ < 0.70, those classes are excluded from the evaluation and the AI customer is informed in writing." |
| "Hyperparameter optimization will be done." | "If GPU memory is not enough, a 4-bit quantized model is used and the latency target is renegotiated." |

If you are stuck, use one of these four patterns:

- **Narrow the scope:** release on the subset that meets the target and leave the rest manual.
- **Degrade gracefully:** give a narrower output instead of the full one (e.g., retrieved passages and a structured summary instead of a generated answer).
- **Hand over to a human (human-in-the-loop):** below a confidence threshold, the system stops producing output and routes the case to a person.
- **Renegotiate the target:** document what cannot be measured and revise the scope with the AI customer.

## Where risks come from

Do not write only "the model may not work". Write **at least one risk from each of the five layers**. A table with only technical risks is incomplete. The same five layers are used as the constraint categories in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md).

| Layer | Typical risks |
|---|---|
| **Data** | Label noise, class imbalance, delayed data access, distribution shift (data drift, concept drift) |
| **Model** | Target metric not met, collapse on rare classes, uncalibrated confidence scores, bias |
| **Infrastructure** | Not enough GPU or memory, latency target not met, failure to scale, fluctuation or loss of assigned resources |
| **Integration** | An external API changes, authorization or access is delayed |
| **People / process** | No domain expert available for labelling or evaluation, user acceptance not obtained, a team member leaves |

Across the layers, cover the whole life cycle: data preparation, model development, deployment and maintenance. Include model decay after deployment and say what will trigger maintenance.

**Not risks:**

- A fixed limit is a **constraint**. For example, "limited computational resources" belongs under Assumptions & Constraints. The resources fluctuating or failing *is* a risk.
- An **assumption** is logged in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md), not here. Its flip-side risk is registered here, with the assumption's ID in **Linked to**.
- Work the team will not do is an **out-of-scope activity** in [Major Activities](03-project-canvas_v2/04-major-activities.md).

## Risk register

Add rows as needed. Rows with a score of 10 or more also need a detail block (next section).

| # | Layer | Risk (event) | When / where | Probability | Impact | Score | Owner | Linked to |
|---|---|---|---|---|---|---|---|---|
| R-01 | | | | | | | | |

"When / where" gives the sprint(s) and whether the risk arises during development or after deployment. "Linked to" gives the IDs of the assumption (A-xx) or constraint (C-xx) in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md), or the row number in [Dependencies](03-project-canvas_v2/06-dependencies.md), that the risk comes from.

## Risk details

Copy this block for each risk.

### Risk R-01: short name>

| Field | Content |
|---|---|
| **Risk (event)** | |
| **Linked to** | Assumption or constraint ID in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md), or row number in [Dependencies](03-project-canvas_v2/06-dependencies.md) |
| **Cause** | Why this could happen |
| **When / where** | Sprint(s); during development or after deployment |
| **Mitigation** | What is done beforehand to lower probability or impact |
| **Probability (basis)** | Residual value (1–5), plus its basis |
| **Impact (basis)** | 1–5, plus which schedule, budget or target/scope effect sets it |
| **Score** | Probability × Impact |
| **Trigger** | Numeric threshold + date or sprint |
| **Contingency plan (B plan)** | What is done if the trigger fires |
| **Owner** | Named person and the role they hold in [Project Organization](03-project-canvas_v2/08-project-organization.md) |
| **Schedule effect** | Expected delay if the contingency plan is used |

### Example (illustrative only)

| Field | Content |
|---|---|
| **Risk (event)** | End-to-end latency does not meet the target on the available hardware |
| **Linked to** | A-04: "The allocated GPU quota supports the latency target for 20 concurrent users" |
| **Cause** | The GPU quota comes from shared cloud credits; the final allocation is not known at project start |
| **When / where** | Sprints 2-4; during development and after deployment |
| **Mitigation** | Early capacity test in Sprint 2; batching, caching and quantization trials |
| **Probability (basis)** | 3: the Sprint 2 pilot measured p95 latency at 1.6× the target |
| **Impact (basis)** | 4: latency is an acceptance criterion of the MVP deliverable |
| **Score** | 12 (High) |
| **Trigger** | p95 end-to-end latency > 2× target at the end of Sprint 4 |
| **Contingency plan (B plan)** | Switch to a smaller quantized model; renegotiate the number of concurrent users with the AI customer; move to queue-based asynchronous answers |
| **Owner** | A named team member in the Data Scientist role |
| **Schedule effect** | About 2 weeks |

## Checklist before submitting

- [ ] At least 5 risks
- [ ] At least one risk from each of the five layers (data / model / infrastructure / integration / people-process)
- [ ] Every risk is written as an event, with when and where
- [ ] Every assumption in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) has a risk here, and the IDs match both ways
- [ ] Every risk that comes from a constraint names the in-scope activity in [Major Activities](03-project-canvas_v2/04-major-activities.md) that mitigates it
- [ ] Probability values are residual (after mitigation), and each has a basis
- [ ] Risks that threaten an acceptance criterion or success criterion have an impact of at least 4
- [ ] Every risk scoring 10 or more has a mitigation, a numeric trigger with a date or sprint, a contingency plan and a named owner
- [ ] Every owner is a named person listed in [Project Organization](03-project-canvas_v2/08-project-organization.md)
- [ ] No contingency plan repeats work already planned under [Major Activities](03-project-canvas_v2/04-major-activities.md)
- [ ] Scores are spread out (not all low, not all high)
- [ ] Risk timings fall inside the project's sprint timeline
