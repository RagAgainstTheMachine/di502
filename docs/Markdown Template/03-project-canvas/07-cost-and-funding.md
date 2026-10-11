# Cost & Funding

This page shows what the project consumes and where it comes from. Count human effort in **person-hours**. Cover every human, material and financial resource needed to produce the deliverables and meet the objectives.

"No direct budget is allocated; costs are minimal" is a weak entry. It gives no table, no hours and no source, and "minimal" is an adjective. A strong entry is a table row: "Data preparation and cleaning ([Major Activities](03-project-canvas_v2/04-major-activities.md) rows 4–6). One-time. 40 person-hours." (illustrative only)

## What to cost

| Resource type | What it covers |
|---|---|
| **Human** | Team effort for every deliverable and in-scope activity |
| **Material** | Compute, cloud services, APIs, tools |
| **Financial** | Credits, quotas or allowances the project draws on |

Include **one-time** costs (set-up, building, a training run) and **ongoing** costs (for example, the effort to sustain data-related activities). Effort that is easy to miss in AI projects:

- Acquiring data can bring its own costs [1].
- Training models can need substantial computing power and waiting time [1].
- Operating an AI system uses compute and power, and GPUs add cost [1].
- Continuous validation is ongoing work after deployment [1].
- In-scope activities that exist only because of a constraint (for example PII masking) belong in the estimates.

## Fields

### Initial Cost Estimate

| Field | What it means | Question it answers |
|---|---|---|
| **Item** | The resource or the work, named with its [Major Activities](03-project-canvas_v2/04-major-activities.md) row or [Milestones](03-project-canvas_v2/02-milestones.md) deliverable where possible | What are we costing? |
| **Type (One-time/Ongoing)** | Whether the cost occurs once or repeats | Does it recur? |
| **Estimated Cost** | For human effort: person-hours. For material and financial items: the amount in currency, or in the unit the provider uses (credits, calls, GPU-hours) | How much? |
| **Notes** | Basis of the estimate and any limit it must stay within | Based on what? |

### Source of Funding

State the source(s) of funding that will support the project. Make clear where each resource comes from, and confirm that the necessary human resources have been committed. In this course there is no sponsor, and every team member manages the project in some capacity.

## Rules

1. Costs are given in table format.
2. Human effort is in person-hours.
3. Every in-scope activity in [Major Activities](03-project-canvas_v2/04-major-activities.md) and every deliverable in [Deliverables](03-project-canvas_v2/05-deliverables.md) is covered by at least one row.
4. The table has both one-time and ongoing rows.
5. Every row has a basis in Notes.
6. Every resource in [Facilities & Resources](03-project-canvas_v2/09-facilities-and-resources.md) that is used up (credits, quotas) has a row here.
7. The total person-hours fit the team-capacity constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md).
8. The Source of Funding names a source for every resource type.
9. The Source of Funding confirms that the team's effort is committed.

CONFLICT: the template says the budget constraint is defined in the Project Executive Summary, but it also lists a set budget as a constraint on the Assumptions & Constraints page. Until this is resolved, make the two statements identical and check this page against both.

TODO(not in sources): how person-hours relate to the story points estimated with poker planning.

## Test to apply to your draft

Pick any in-scope row in [Major Activities](03-project-canvas_v2/04-major-activities.md). Can you find its person-hours here? Then add up all the person-hours. Is the total within team size × hours per week × number of weeks from your constraints?

## Not this / this

The left column shows weak entries, each tagged with the rule it breaks.

| Not this | Rule broken | This (illustrative only) |
|---|---|---|
| A narrative only: "No direct financial budget is allocated. Human resources are provided entirely by the students. Computational resources such as local GPUs, lab computers or free cloud runtimes will be used. No licensing costs are anticipated." | No table, no figures (rules 1–3) | A table with one row per resource and per activity group, e.g. "Model fine-tuning experiments ([Major Activities](03-project-canvas_v2/04-major-activities.md) rows 15–17). One-time. 60 person-hours. Basis: 3 experiments × 20 h." and "Notebook GPU runtime. Ongoing. Up to the free-tier session limit per day. Basis: provider's published limit." |
| "Budget: resources limited to open datasets and the cloud service provided by the university. It represents a minimal cost." | Adjective instead of a figure; no table (rule 1) | Executive Summary: "Budget: 260 person-hours of team effort and the university cloud credit." This page: one row for the effort, one row for the credit with its allocation. |
| A risk "cloud cost may be higher than estimated", while no cost estimate exists anywhere in the charter. | Nothing to compare against (rule 6) | Add a row for cloud usage here, with the allocation in Notes. The risk in [Risks](03-project-canvas_v2/11-risks.md) can then use a trigger such as "usage exceeds 80% of the allocation before Sprint 4". |

A good statement to copy for the Source of Funding: "All human-resource effort will be contributed in-kind by the student project team, with no paid labour or external contractors." It confirms that human resources are committed, as the template requires.

## Patterns to use if you are stuck

- **Team capacity:** members × hours per week × weeks gives the person-hours available. Take the inputs from your constraints in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md).
- **Activity groups:** one row per group of related [Major Activities](03-project-canvas_v2/04-major-activities.md) rows, with the row numbers in Item.
- **University-provided cloud:** one row with the allocation in Notes. In the course, the cloud environment can be provided by the university.
- **Free-tier service:** one row with the provider's limit in Notes.
- **Ongoing work:** one row for monitoring and re-evaluation after deployment [1].

## What doesn't belong here

- **The budget or capacity limit itself** goes in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) as a constraint (see CONFLICT above).
- **The list of resources, who provisions them and their status** goes in [Facilities & Resources](03-project-canvas_v2/09-facilities-and-resources.md).
- **A cost overrun** is a risk in [Risks](03-project-canvas_v2/11-risks.md).
- **The breakdown of deliverables into components** (work breakdown structure) belongs in [Deliverables](03-project-canvas_v2/05-deliverables.md).

## 1. Initial Cost Estimate

Note: cost estimates should align with the budget constraint defined in the [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md).

| # | Item | Type (One-time/Ongoing) | Estimated Cost | Notes |
|---|---|---|---|---|
| 1 | | | | |

## 2. Source of Funding

State the source(s) of funding that will support the project, and confirm that the necessary human resources have been committed to the project.

## Example (illustrative only)

Scenario: a legal research assistant. Four members × 5 hours per week × 13 weeks = 260 person-hours available. All figures are illustrative.

| # | Item | Type (One-time/Ongoing) | Estimated Cost | Notes |
|---|---|---|---|---|
| 1 | Chartering and sprint documentation ([Major Activities](03-project-canvas_v2/04-major-activities.md) rows 1–3) | Ongoing | 40 person-hours | 4 sprints × 10 h |
| 2 | Data acquisition, cleaning, PII masking and log anonymization ([Major Activities](03-project-canvas_v2/04-major-activities.md) rows 4–8) | One-time | 45 person-hours | Includes rows 7–8, which exist because of C-03 |
| 3 | Indexing and retrieval pipeline ([Major Activities](03-project-canvas_v2/04-major-activities.md) rows 9–11) | One-time | 50 person-hours | Based on the Sprint 1 spike |
| 4 | Evaluation set and experiments ([Major Activities](03-project-canvas_v2/04-major-activities.md) rows 14–17) | One-time | 60 person-hours | 3 experiment cards × 20 h |
| 5 | Monitoring and re-evaluation after deployment | Ongoing | 25 person-hours | Weekly checks in Sprint 4 |
| 6 | Reviews, demos and retrospectives | Ongoing | 30 person-hours | Includes peer review at Sprints 2–4 |
| 7 | Cloud GPU usage | Ongoing | Up to $100 | Allocation from the university; tracked weekly |
| | **Total effort** | | **250 person-hours** | Within the 260 available (C-01) |

Source of Funding: team effort (250 person-hours) is contributed in-kind by the four members, who have committed to the hours in C-01. Compute comes from the university cloud credit. The document set is used under its published licence, at no charge.

## Checklist before submitting

- [ ] Costs are in a table (rule 1)
- [ ] Human effort is in person-hours (rule 2)
- [ ] Every in-scope activity and deliverable is covered (rule 3)
- [ ] The table has one-time and ongoing rows (rule 4)
- [ ] Every row has a basis in Notes (rule 5)
- [ ] Every used-up resource in [Facilities & Resources](03-project-canvas_v2/09-facilities-and-resources.md) has a row (rule 6)
- [ ] Total person-hours fit the capacity constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) (rule 7)
- [ ] The Source of Funding names a source for every resource type and confirms that effort is committed (rules 8–9)
- [ ] The budget statement matches [Project Executive Summary](03-project-canvas_v2/01-project-executive-summary.md) and [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) (CONFLICT above)

---

## References

[1] ISO/IEC JTC 1/SC 42, *ISO/IEC 5338:2023 Information technology — Artificial intelligence — AI system life cycle processes*, 1st ed. Geneva, Switzerland: International Organization for Standardization and International Electrotechnical Commission, Dec. 2023. UK implementation: BS ISO/IEC 5338:2023, London, UK: BSI Standards Limited, 2024.
