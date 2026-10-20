# Project Executive Summary

## Background

In August 2026, Presidential Circular 2026/9 put the Türkiye AI Action Plan (2026–2030) into force for public institutions [1, 2]. Under Action 7 of the plan, every public institution must appoint a senior executive responsible for AI transformation and, within 12 weeks of these appointments, prepare a three-year AI roadmap [2].

The policies, rules and terms this work depends on are spread across eight official documents totalling about 1,860 pages: the action plan (44 pages); the Twelfth Development Plan (253 pages) and the 2026 Presidential Annual Programme (465 pages), whose AI-related policies and measures are scattered across many sections; a parliamentary AI commission report (923 pages); TÜBİTAK's institutional AI policy (8 pages); a public-sector AI glossary (80 pages); the Personal Data Protection Law No. 6698 (21 pages); and the Personal Data Protection Authority's (KVKK) guide on generative AI and personal data (64 pages) [2–9]. These documents range from binding law to plans, guidance, parliamentary recommendations and an institutional policy. 

Türkiye has no AI-specific law yet; existing general laws apply to AI, including Law No. 6698 when AI systems process personal data [7]. 
Responsibility for AI governance also moved between institutions as recently as December 2025 [7]. Today, staff who are not AI-policy specialists must find these documents, locate the relevant parts, and work out for themselves which rules bind their institution and which are only plans or recommendations.

**Budget:** $100 of Google Cloud credits (fixed, per project). **Duration:** 4 sprints. **Timeline:** 14 October 2026 to 30 December 2026.

## 1. Stakeholders


| # | Stakeholder | Role (ISO 5339) | Perspective | Relationship to project | Benefit from project |
|---|---|---|---|---|---|
| 1 | Staff in the strategy, legal and training units of Turkish public institutions who must understand and explain Türkiye's AI policy | AI user (primary) | Use | Ask what Türkiye's AI policy says, who is responsible for what, and whether a rule is binding or only planned | Get answers from the official sources with citations and each source's legal status, instead of reading the documents one by one |
| 2 | AI-policy researchers and graduate students | AI user (secondary) | Use | Ask questions about Türkiye's AI policy documents | Find provisions across documents without reading each one in full, with references they can cite |
| 3 | DI 502 Project Review Committee (course instructors), joined by the peer review teams from Sprint 2 | AI customer | Use | Commissions the project, sets its constraints (including RAG), approves the charter and the acceptance criteria | Receives an assistant that meets the agreed acceptance criteria, with documentation they can review each sprint |
| 4 | Public bodies that publish the source documents | Data provider | Make | Publish the official documents the assistant answers from | Their documents are read and cited correctly by the staff who must apply them |
| 5 | Sanayi ve Teknoloji Bakanlığı (Millî Teknoloji ve Yapay Zekâ Genel Müdürlüğü) and Siber Güvenlik Başkanlığı | Regulators / policy makers | Impact | Coordinate the Action Plan and lead Action 7, which sets the users' obligations | Institutions understand and carry out their Action Plan obligations correctly |
| 6 | Kişisel Verileri Koruma Kurumu (KVKK) | Regulators / policy makers | Impact | Enforces Law 6698 in public institutions' use of AI | Personal-data rules are applied when institutions introduce AI |
| 7 | Türkiye Büyük Millet Meclisi (TBMM), as legislator for a future AI law | Regulators / policy makers | Impact | Its AI research commission report is part of the corpus | Users do not mistake the commission's recommendations for law in force |
| 8 | Citizens whose data and public services are affected by public institutions' AI use | Community | Impact | Do not use the assistant; affected by how public institutions apply AI rules | Public institutions handle their data and AI-based services in line with the applicable rules |

**Conflicts between stakeholders:**

- **Users (1) vs regulators (5, 6):** users want a yes/no answer on whether their own institution's plan or practice complies with the rules, but only the institution itself and the regulators can make that judgement. *Resolution:* the assistant answers with what the documents say, with citations and each source's legal status, and states that it does not judge whether a specific situation complies.
- **Regulators (5) vs primary users (1):** the bodies responsible for the Action Plan want institutions to apply it as published, while staff also need to know which parts are still open or only planned. *Resolution:* the assistant states only what the documents say, with each source's legal status, and does not fill in details the documents leave open.
- **Regulators (5) vs secondary users (2):** the coordinating bodies present the Action Plan as the reference policy, while researchers need a full picture that also covers parliamentary recommendations that differ from it. *Resolution:* the assistant presents every source with its issuer and legal status and favours none.
- **Primary (1) vs secondary users (2):** researchers may also want history and comparisons between strategies. *Resolution:* both groups can ask about the current documents; comparisons with earlier strategies are out of scope (see Major Activities).

## 2. Project Vision and Objectives

### 2.1 Project vision

Staff in Turkish public institutions, and the researchers who study AI policy, can find what Türkiye's AI policy says in one place and in their own words, and can tell binding rules apart from plans, and recommendations.


### 2.2–2.4 Objectives, success criteria and business outcomes

| # | Objectives | Success Criteria | Business Outcomes |
|---|---|---|---|
| 1 (strategic) | By the end of Sprint 4 (30 Dec 2026), reduce the time public institution staff and AI-policy researchers need to answer a question about Türkiye's AI policy, compared with searching the official documents directly. | Median time for pilot participants to answer a fixed set of 10 policy questions falls from **[default state, measured in Sprint 2 with participants using only the official documents and websites]** to at most half of that value (level set from the team's own research). **Method:** timed task test with 10 participants. **Owner:** Project Review Committee (AI customer). **Date:** end of Sprint 4. **Maps to:** task completion time, supported by response time and answer correctness. | At least 8 of 10 pilot participants answer the fixed question set faster with the assistant than with the official documents alone, and receive source citations with every answer. |
| 2 (Phase-1 MVP) | By the end of Sprint 3 (9 Dec 2026), validate that an MVP assistant gives correct, source-backed answers to AI-policy questions from public institution staff. | At least **24 of 30** test questions (including follow-up questions) are answered correctly, and at least **24 of 30** answers cite a document and section that support them (levels informed by reported Turkish RAG results [10]). **Method:** review against the reference answers in the question inventory. **Owner:** Project Review Committee (AI customer). **Date:** end of Sprint 3. **Maps to:** answer correctness, citation support and retrieval quality in the experiment cards. | Pilot participants need to open an original document for fewer than 1 in 4 questions. |
| 3 | By the end of Sprint 4 (30 Dec 2026), public institution staff and AI-policy researchers prefer the assistant to searching the official documents for AI-policy questions. | At least **7 of 10** pilot participants say they would use the assistant again (level set from the team's own research). **Method:** post-test survey. **Owner:** Project Review Committee (AI customer). **Date:** end of Sprint 4. **Maps to:** survey score. | At least half of the pilot participants say they would recommend the assistant for AI-policy questions. |
| 4 | By the end of Sprint 4 (30 Dec 2026), public institution staff are not misled into treating plans, guidance or recommendations as binding law. | In at least **27 of 30** test answers, the legal status stated for each cited source matches the document inventory (binding law, policy/plan, guidance, report or institutional policy) (level informed by reported Turkish RAG results [10]). **Method:** review against the inventory. **Owner:** Project Review Committee (AI customer). **Date:** end of Sprint 4. **Maps to:** legal-status labelling accuracy. | In the post-test survey, no pilot participant reports having taken a plan or a recommendation for a law in force. |
| 5 | By the end of Sprint 4 (30 Dec 2026), public institution staff who ask questions the assistant cannot answer, or who ask whether their own institution's plan or practice complies with the rules, are told that the assistant cannot answer instead of receiving a guess. | The assistant declines without guessing for at least **8 of 10** out-of-scope and compliance-judgement test questions (level informed by reported Turkish RAG results [10]; the Scope lecture's example uses 100%). **Method:** scripted test set reviewed against the reference answers. **Owner:** Project Review Committee (AI customer). **Date:** end of Sprint 4. **Maps to:** refusal rate on out-of-scope questions. | No pilot participant receives a judgement from the assistant on whether their own institution's plan or practice complies with the rules. |

Objectives 1–5 cover performance, quality, adoption/UX, and safety/compliance (objectives 4 and 5), in that order.

## 3. Project Scope

### 3.1 Scope Definition

A question-answering assistant in Turkish for Türkiye's official documents on AI policy and the related personal-data rules, used through a web page by staff in the strategy, legal and training units of public institutions, and by AI-policy researchers and graduate students.

| # | Feature | What the user can do with it | Objective(s) it serves |
|---|---|---|---|
| 1 | Plain-language questions | Ask about Türkiye's AI policy in their own words and get an answer drawn from the official documents | 1, 2 |
| 2 | Source reference | See the document and section or article each answer comes from, with a link to the official source | 2 |
| 3 | Legal status label | See, for each cited source, whether it is binding law, a policy or plan, guidance, a report or an institutional policy, with its date | 4 |
| 4 | Follow-up questions | Ask a follow-up question in the same conversation without repeating the context | 1, 2, 3 |
| 5 | Clear decline | Be told plainly that the assistant cannot answer, instead of receiving a guess, when a question is outside the document collection or asks whether their own institution's plan or practice complies with the rules | 5 |
| 6 | Collection date | See the date up to which the document collection is current | 2 |
| 7 | Term definitions | Ask what an AI term means and get the definition from the public-sector AI glossary, with its source | 2 |

The following exclusions are listed as **Out of Scope** under Major Activities:

- Judgements on whether a specific institution's plan or practice complies with the rules
- Predictions about future legislation or policy
- Details the documents in the collection do not contain, including implementation steps that a plan says will be prepared later
- Institutions' internal rules
- Foreign regulation
- Documents outside the collection, including parliamentary bills
- History of Türkiye's AI policy and comparisons with earlier strategies


## References

[1] Presidential Circular 2026/9, Official Gazette No. 33344, 18 August 2026.
[2] Türkiye Yapay Zekâ Eylem Planı (2026–2030), T.C. Sanayi ve Teknoloji Bakanlığı.
[3] On İkinci Kalkınma Planı (2024–2028), approved by TBMM Decision No. 1396, Official Gazette No. 32356 (Mükerrer), 1 November 2023.
[4] T.C. Cumhurbaşkanlığı Strateji ve Bütçe Başkanlığı, 2026 Yılı Cumhurbaşkanlığı Yıllık Programı, Official Gazette No. 33062 (Mükerrer), 30 October 2025.
[5] Law No. 6698 on the Protection of Personal Data.
[6] KVKK, Üretken Yapay Zekâ ve Kişisel Verilerin Korunması Rehberi, November 2025.
[7] TBMM Yapay Zekâ Araştırma Komisyonu Raporu, Sıra Sayısı 260, March 2026.
[8] TÜBİTAK, TÜBİTAK Yapay Zekâ Politikası, March 2026.
[9] T.C. Cumhurbaşkanlığı İletişim Başkanlığı, Kamu Kurumları İçin Yapay Zekâ Sözlüğü, 2026.
[10] S. K. Köse et al., "RAGTurk: Best Practices for Retrieval Augmented Generation in Turkish," EACL 2026 SIGTURK, arXiv:2602.03652.
