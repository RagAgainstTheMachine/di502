# DI 502 — Weekly Expectations and Deliverables

This document tells you what to do each week, what to deliver at the end of each sprint, and where everything lives in your repository. It is a living document: changes are announced in class and made through pull requests.

---

## Working principles

- **Everything lives in Git as Markdown.** Charter, design notes, decisions, spike notes, evaluation results and sprint reports are `.md` files in your team repository.
- **Keep documents short.** No document should be longer than one or two pages. Specifications are not separate documents: parameters live in `config/rag.yaml`, and results live in Weights & Biases.
- **Jira is the single place for planning.** GitHub is the place for code and pull requests. GitHub Issues are disabled in team repositories.
- **Every branch, commit and pull request contains a Jira key**, for example `DI3-14-vector-store-adr`. This links your work to Jira automatically.
- **Decisions are recorded when they are made**, as Architecture Decision Records (ADRs), not written up front.
- **Everything that affects an answer is versioned**: code, dependencies, models, documents, prompts, configuration and the evaluation set. The AI Bill of Materials (`ai-bom.yaml`) lists them.

---

## Repository structure

```
<team-repo>/
├── README.md               # How to install and run the system
├── ai-bom.yaml             # AI Bill of Materials (from Sprint 2)
├── requirements.txt        # Pinned dependencies (exact versions)
├── config/
│   └── rag.yaml            # All parameters: chunking, models, top-k, prompt variant
├── prompts/                # Prompt templates, one file per template
├── data/
│   └── manifest.csv        # Source URL, licence, version date and hash of each document
├── src/                    # Code
└── docs/
    ├── Markdown Template/  # Sprint 1; later updated only through pull requests
        ├── 03-project-canvas/
        └── ...             
    ├── design.md           # Starts in the end of Sprint 1 as a one-page overview
    ├── adr/                # One file per decision, e.g. 0002-vector-store.md
    ├── spikes/             # Learning and hypothesis notes
    ├── eval/
    │   ├── eval-set-v1.csv # Question, type, gold answer, gold source
    │   └── results.md      # Metrics per sprint, compared with the baseline
    └── sprints/
        └── sprint-N.md     # One-page report per sprint
```

---

## Sprint 1 · Discovery (14/10 – 28/10)

### Week 2 — 07/10 · Start of Sprint 1 (early)

**Deliverables**
* Project Executive Summary
* Mini presentations of project topics (10 min per team)

**Milestones**
* Open a Github repository and invite your peers. Clone this git repository inside. Please note that only the Project Executive summary has been manually checked and updated. Other pages will be updated by October 8th.

If you are not familiar with Git and GitHub, such as using issues, pull requests, reviewing changes etc. please follow Datacamp guides on Intermediate Git and Advanced Git.


### Week 3 — 14/10 · Start of Sprint 1
> [!IMPORTANT]
> **Sprint goal** Know *what* you will build and *why*, and prepare everything needed to measure it. No production code is expected in this sprint.

**Deliverables**

- [ ] [Project Canvas](Markdown Template/README.md) : Scope, Milestones, Assumptions & Constraints, Deliverables and Project Organization
- [ ] User stories in Jira (you may plan them in Miro first, but this is optional)
- [ ] Learning spike notes in `docs/spikes/`

**Your tasks**

- [ ] Check the *Sprint 1 fundamentals* table in [Online Course Register](online-course-register/README.md/#sprint-1-fundementals) individually and plan how to close your gaps. Git and Jira courses are important for this week but plan ahead as well.
- [ ] Create your team repository from the course template (Use this template) and your Jira project.
- [ ] Revise your topic and scope based on the feedback from Week 2.
- [ ] Assign the Scrum roles, including the Product Owner for Sprint 1.
- [ ] Choose your document sources and check their terms of use and licences.

**Presentation (10 minutes):** Each team presents, repository, charter draft and Jira setup, the Scrum roles, the revised topic and scope, and the document sources.

---

### Week 4 — 21/10 · Middle of Sprint 1 (Early end of Sprint 1)

- [ ] [Project Canvas](Markdown Template/README.md): Major Activities, Dependencies, Facilities and Resources, Release Plan, Risks
- [ ] Updated user stories in Jira
- [ ] Learning spike notes in `docs/spikes/`

**Your tasks** (Checklist not yet completed)

- [ ] Iterate on user stories based on feedback from Week 3.
- [ ] Design initial versions of your system architecture diagram and design document (i.e. which technologies will be chosen and how they will connect)


### Week 5 — 21/10 · End of Sprint 1

TBD
