# Facilities & Resources

This page lists the infrastructure, tools and resources the team needs to support development, who obtains each one, and where it stands.

"Cloud service from the university" is a weak entry. It does not say what is needed, who requests it, or whether it is ready. A strong entry answers all three: "GPU runtime for experiments, one shared allocation under the university cloud credit. Responsible: the Data Scientist who handles infrastructure. Status: access granted on <date>." (illustrative only)

## Resource categories

Cover each category that applies:

| Category | Examples from the template | AI-specific points from the ISO standards |
|---|---|---|
| **Compute & hosting** | GPU access, cloud credits, vector database hosting, deployment environment | Training can need substantial computing power and waiting time [1]. AI systems can consume considerable compute and memory, and GPUs add cost [1]. The runtime environment can differ from the development environment [1]. |
| **APIs & third-party services** | An LLM provider, an embedding service, and any usage/rate limits to plan around | A project can depend on other organizations for infrastructure or capability [1]. |
| **Software & licenses** | Development tools, orchestration frameworks, monitoring/eval tools | — |
| **Data access** | Storage for the corpus, access permissions, special environments for sensitive data | Datasets can be large and are often stored apart from code [1]. Data stores holding sensitive data enlarge the attack surface and need protection [1]. |
| **Physical/logistical needs** | Lab space, shared workstations | — |

Say also *where* each resource runs: on-premise, as a cloud service, or through a third party [2]. A cloud service is a capability offered through cloud computing and used through a defined interface [2].

## Fields

| Field | What it means | Question it answers | Source |
|---|---|---|---|
| **Resource** | The item, named precisely (type, size, provider) | What exactly do we need? | |
| **Description** | What it is used for, where it runs, and any usage or rate limit | Why do we need it, and what limits apply? | [2] |
| **Responsible Person/Team** | Who obtains or provisions it (e.g., requests API credits, sets up cloud accounts, configures shared repositories) | Who makes it happen? | |
| **Status** | Where the item stands now, with a date | Is it ready? | |

Write Status as a short dated fact, such as "requested on <date>" or "access granted on <date>".

## Rules

1. Every category in the table above is either covered or marked as not needed.
2. Every row names a Responsible Person/Team.
3. Every API or third-party service row states its usage or rate limits.
4. Every compute row says what hardware is used and where it runs [2].
5. The deployment environment has its own row.
6. Every data-access row names the storage and the access permissions, and says whether sensitive data needs a special environment [1].
7. Every row has a dated Status.
8. A fixed limit on a resource is also written as a constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md).
9. The chance that a resource fluctuates or fails is a risk in [Risks](03-project-canvas_v2/11-risks.md).
10. When work waits for someone else to deliver a resource, that wait is also a row in [Dependencies](03-project-canvas_v2/06-dependencies.md).

## Test to apply to your draft

Could a new team member start work using only this table: knowing what to use, where it runs, whom to ask, and whether it is ready?

## Not this / this

Each row below shows a resource problem that this page would have caught.

| Not this | Rule broken | This (illustrative only) |
|---|---|---|
| The charter names "the cloud service provided by the university" as the project's resource, while the experiment cards report runs on a team member's laptop GPU. | The resource used is not the resource listed (rule 4) | Two compute rows: "Laptop GPU (12 GB VRAM), member-owned, for development runs" and "Cloud GPU under the university credit, for staging and load tests", each with its Responsible person and dated Status. |
| A retrospective notes that API rate limits and latency spikes disrupted response-time tests, and that limited GPU resources forced a mid-sprint move to a paid notebook tier. | Limits not planned in advance (rules 3, 4) | "External data API, free tier: 60 calls per minute; test scripts cache responses." "Notebook GPU, free tier: session limit per day; fine-tuning runs scheduled within it." Plus a constraint for each limit in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md). |

Two good practices to copy:

- Recording access as a precondition: "Team members were granted access permissions for the documentation, task-tracking and repository tools."
- Confirming compute before the work that needs it: "GPU or notebook runtime confirmed for fine-tuning."

## Patterns to use if you are stuck

One row each for:

- **Development compute:** hardware, owner, where it runs.
- **Training or experiment compute:** GPU type and allocation; credit or quota.
- **LLM and embedding access:** hosted locally or through an API; rate limits.
- **Vector database:** where it is hosted.
- **Data storage:** location of raw and processed data; who has access.
- **Shared repository and experiment tracking:** who configures them.
- **Deployment environment:** where the MVP runs.

## What doesn't belong here

- **Costs and person-hours** go in [Cost & Funding](03-project-canvas_v2/07-cost-and-funding.md).
- **Fixed limits** (a credit amount, a quota) are constraints in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md).
- **A resource failing or fluctuating** is a risk in [Risks](03-project-canvas_v2/11-risks.md).
- **Waiting for an outside party** is a dependency in [Dependencies](03-project-canvas_v2/06-dependencies.md).
- **Every third-party library, tool and model with its version and license** goes in [Software Bill of Materials](10-software-bill-of-materials.md). List here only what the team needs access to.
- **Documentation of the datasets themselves** goes in the [Datasheets](11-datasheets/README.md) pages. List here only storage and access.

## Resources

| # | Resource | Description | Responsible Person/Team | Status |
|---|---|---|---|---|
| 1 | | | | |

## Example (illustrative only)

Scenario: a legal research assistant. Names, limits and dates are illustrative.

| # | Resource | Description | Responsible Person/Team | Status |
|---|---|---|---|---|
| 1 | Cloud GPU (1 × 24 GB) under the university credit | Experiments and staging deployment; cloud service; limited to the allocated credit (C-02) | Member 1 (Data Scientist, infrastructure) | Requested on 14/10/2026; granted on 17/10/2026 |
| 2 | Hosted LLM API | Answer generation in staging; 500 calls per day on the academic tier (C-05) | Member 2 | API key issued on 20 Oct |
| 3 | Embedding model, run locally | Document and query embeddings; on the cloud GPU | Member 2 | Downloaded and tested on 22/10/2026 |
| 4 | Vector database | Index of the document set; hosted on the cloud project | Member 3 | Planned for 28/11/2026 |
| 5 | Shared storage for raw and processed documents | Encrypted bucket; access for team members only; no PII stored (C-03) | Member 3 (Business Analyst; contact with the data provider) | Created on 15/10/2026 |
| 6 | Shared code repository and experiment tracker | Version control and run logs | Member 4 | Configured on 10/10/2026 |
| 7 | Staging environment for the MVP | Web app on the cloud project; used by pilot AI users | Member 4 (Data Scientist, staging deployment) | Planned for 02/12/2026 ([Dependencies](03-project-canvas_v2/06-dependencies.md) row 4) |

## Checklist before submitting

- [ ] Every category is covered or marked as not needed (rule 1)
- [ ] Every row names a Responsible Person/Team (rule 2)
- [ ] Every API or third-party service row states its usage or rate limits (rule 3)
- [ ] Every compute row says what hardware is used and where it runs (rule 4)
- [ ] The deployment environment has its own row (rule 5)
- [ ] Every data-access row names storage, permissions and any sensitive-data needs (rule 6)
- [ ] Every row has a dated Status (rule 7)
- [ ] Every fixed limit also appears as a constraint in [Assumptions & Constraints](03-project-canvas_v2/03-assumptions-and-constraints.md) (rule 8)
- [ ] Every resource that could fail has a risk in [Risks](03-project-canvas_v2/11-risks.md) (rule 9)
- [ ] Every wait on an outside party is a row in [Dependencies](03-project-canvas_v2/06-dependencies.md) (rule 10)

---

## References

[1] ISO/IEC JTC 1/SC 42, *ISO/IEC 5338:2023 Information technology — Artificial intelligence — AI system life cycle processes*, 1st ed. Geneva, Switzerland: International Organization for Standardization and International Electrotechnical Commission, Dec. 2023. UK implementation: BS ISO/IEC 5338:2023, London, UK: BSI Standards Limited, 2024.

[2] ISO/IEC JTC 1/SC 42, *ISO/IEC 5339:2024 Information technology — Artificial intelligence — Guidance for AI applications*, 1st ed. Geneva, Switzerland: International Organization for Standardization and International Electrotechnical Commission, Jan. 2024. UK implementation: BS ISO/IEC 5339:2024, London, UK: BSI Standards Limited, 2024.
