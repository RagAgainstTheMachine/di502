# Project Organization

This page defines the project team structure, the responsibilities assigned to each role and the team's relationship with the stakeholders who review, use, influence or provide services to the project. The Scrum Team consists of one Product Owner, one Scrum Master and three Data Scientists, with no hierarchy inside the team [1]. Outside stakeholders use the relevant stakeholder roles defined in ISO/IEC 5339 [2].

## 1. Project Team Structure

- **Project Review Committee:** Course instructors
- **Peer review groups:** Review project documents during Sprints 2, 3 and 4
- **Scrum Team — no hierarchy inside the team:**
  - **Product Owner:** Muhammed Batuhan Tezcan
  - **Scrum Master:** Deniz Şenkutlu
  - **Data Scientists:** Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu
- **Outside stakeholders:**
  - **AI customer:** Course instructors and peer groups
  - **Data providers:** Public bodies publishing the approved policy documents
  - **AI partner:** Google Cloud
  - **AI users:** Staff in Turkish public institutions and AI-policy researchers
  - **Regulators and policy makers:** Relevant ministries, the Cyber Security Presidency, KVKK and TBMM
  - **Community:** Citizens affected by the use of AI in public services

## 2. Roles and Responsibilities

| Project Role | Responsibilities | Assigned to |
|---|---|---|
| Product Owner | Define and communicate the product goal; write and order Product Backlog items; maintain user stories and their acceptance criteria in Jira; ensure that the backlog remains consistent with the objectives and scope in the Project Executive Summary; coordinate requirements and acceptance feedback with the AI customer; and track progress against the project's success criteria. | Muhammed Batuhan Tezcan |
| Scrum Master | Facilitate Sprint Planning, Sprint Review and Sprint Retrospective; track impediments in Jira; support team self-management; help the team keep backlog items clear and suitable for planning; and ensure that Scrum events and the Definition of Done are followed. | Deniz Şenkutlu |
| Data Scientist | **Utku Uçar:** prepare the approved document collection; develop the chat interface; and implement the session context required for follow-up questions. **Elif Yeşim Koçoğlu:** generate embeddings and maintain the search index; develop and evaluate the retrieval pipeline; and configure the Google Cloud services and deployment environment. **Deniz Şenkutlu:** integrate the language model with the retrieved evidence and develop prompts, grounded answer-generation logic and unsupported-request behaviour. **All:** record experiments, test increments against the Definition of Done and review pull requests. | Deniz Şenkutlu, Utku Uçar and Elif Yeşim Koçoğlu |
| Project Review Committee | Review the Project Charter and sprint deliverables and provide course-level feedback. | Course instructors |
| AI customer | Review customer-facing deliverables and the MVP against the agreed requirements and acceptance criteria and provide acceptance feedback. | Course instructors and peer groups; team contact: Muhammed Batuhan Tezcan |
| Data provider | Publish and maintain the official documents and source URLs included in the approved collection. | Public bodies publishing the approved policy documents; team contact: Utku Uçar |
| AI partner | Provide the Google Cloud services available under the project's cloud credit for development and deployment. | Google Cloud; team contact: Elif Yeşim Koçoğlu |
| AI user | Ask questions about Türkiye's AI policy and participate in usability and answer-evaluation activities. | Staff in Turkish public institutions and AI-policy researchers; team contact: Deniz Şenkutlu |
| Regulators and policy makers | Publish, coordinate or enforce the policy and legal requirements represented in the approved document collection. | Relevant ministries, the Cyber Security Presidency, KVKK and TBMM; team contact: Muhammed Batuhan Tezcan |
| Community | Be affected by the use of AI in public services; their data, rights and access to public services are considered in the project's scope and evaluation criteria. | Citizens affected by AI-supported public services; team contact: Muhammed Batuhan Tezcan |

## 3. Roles Not Assigned

The team does not assign separate Business Analyst, Group Manager, Team Lead or Project Lead roles in the first version of the Project Organization. Their potential responsibilities are already covered by the Product Owner, Scrum Master and Data Scientists. These roles may be reconsidered only if a separate, non-overlapping responsibility emerges during the project.

## References

[1] K. Schwaber and J. Sutherland, *The Scrum Guide: The Definitive Guide to Scrum: The Rules of the Game*, Nov. 2020. [Online]. Available: https://scrumguides.org/scrum-guide.html.

[2] ISO/IEC JTC 1/SC 42, *ISO/IEC 5339:2024 Information technology — Artificial intelligence — Guidance for AI applications*, 1st ed. Geneva, Switzerland: International Organization for Standardization and International Electrotechnical Commission, Jan. 2024.
