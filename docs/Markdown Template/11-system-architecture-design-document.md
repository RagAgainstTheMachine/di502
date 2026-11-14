# System Architecture Design Document

| Team | Sprint | Status | Last updated | Updated by |
|---|---|---|---|---|
| Rag Against The Machine | Sprint 2 | proposed | 2026-11-09 | Elif Yeşim Koçoğlu |

This document describes the proposed architecture at a technology-neutral level. Exact products, models, versions and cloud machine types will be selected after the related spikes. Accepted choices will then be added to this document and the relevant SBOM.

## 1. Summary

The system is a Turkish question-answering assistant for a fixed collection of eight official documents on Türkiye's public-sector AI policy. It uses retrieval-augmented generation (RAG): the system retrieves candidate passages, reranks them for relevance to the question and generates an answer from the selected passages.

The architecture has three parts:

1. **Document preparation:** approved documents are collected, checked, cleaned and prepared for search.
2. **Question answering:** requests pass through the web interface, middleware/API and a question-understanding step before retrieval and grounded answer generation.
3. **Evaluation:** controlled baseline and experiment runs measure system quality, with configurations and results recorded in Weights & Biases.

The system returns Turkish answers with traceable source information. It gives a clear decline instead of guessing when a request is outside the collection or asks for a case-specific compliance judgement. It does not use an external commercial language-model API and does not store persistent conversation history.

## 2. Goals and non-goals

### Goals

- Answer Turkish questions using evidence from the approved eight-document collection.
- Present the supporting document, article or section, page where available, official URL, publication date and legal status.
- Support up to five user questions, including follow-up questions, during one open chat.
- Understand and prepare a request before it reaches retrieval.
- Decline unsupported and case-specific questions without generating a guess.
- Evaluate retrieval, answer correctness, citation support, legal-status accuracy, refusal behaviour and latency.
- Keep prompts, retrieval settings and experiment parameters under version control.
- Operate within the fixed $100 Google Cloud credit.

### Non-goals

- Giving case-specific legal or administrative advice.
- Predicting future policy or legislation.
- Answering from documents outside the approved collection.
- Automatically monitoring or updating official documents.
- Fine-tuning or training a foundation model.
- Creating user accounts or storing persistent conversation history.
- Providing a mobile application, high availability, automatic scaling or continuous 24/7 operation.

## 3. System architecture diagram

**Version:** v2 (2026-11-09)

![System architecture: document indexing, question answering with retrieval and reranking, and controlled evaluation](../images/system-architecture.png)

During document preparation, approved documents are extracted, cleaned, divided into passages and embedded while retaining their source metadata. The resulting passage text, embeddings and metadata populate the vector search index. During question answering, Question Understanding checks the request's scope and prepares the question for retrieval. The question embedding is sent to the index, which returns top-k candidate passages and their source metadata. A reranker scores each candidate against the question and selects the top-n passages for answer generation. The application fills the answer prompt with the question and those passages and formats the source list from their stored metadata. Controlled evaluation uses responses from scheduled baseline and experiment runs and records their configurations and measurements in Weights & Biases.

## 4. Components

| Component | Responsibility | Technology and version | SBOM entry |
|---|---|---|---|
| AI user | Submits Turkish questions and reads answers and sources through a browser. | Standards-compatible browser | N/A — user-controlled |
| Eight official documents | Provide the fixed public-policy content and source metadata. | Official PDF and HTML publications | Third-Party Dataset Register |
| Document preparation | Imports and verifies approved files; extracts and cleans text; chunks it at meaningful source boundaries; and preserves source metadata. | Python-based processing pipeline; exact libraries and versions pending spikes | Project code and selected dependencies |
| Document chunks | Carries each prepared passage and its source metadata from document preparation to embedding and indexing. | Structured passage records; exact schema pending ingestion spike | Project data schema |
| Document files (PDF / JSONL) | Stores approved original files and reproducible processed records. | Cloud object storage; exact configuration pending | Managed-service record and client dependency if used |
| Vector database | Stores searchable passages, document embeddings and their document, section, page, date, legal-status and URL metadata; accepts a question embedding and returns the top-k matching passages and metadata. | Vector database; exact product and version pending | Pending decision |
| Web chat interface | Collects questions and displays answers, sources, legal status, dates and collection date. It does not access retrieval or model components directly. | Python-compatible web UI framework; exact framework and version pending | Pending decision |
| Middleware / API | Receives questions from the web interface, enforces the five-question chat limit, passes them to question understanding and returns the resulting response. | Python application layer; exact framework and implementation pending spike | Project code and selected dependencies |
| Question understanding and scope decision | Checks whether a question can be handled, routes out-of-scope requests to the clear-decline handler and prepares supported questions, including follow-ups from the current chat, for search. | Python application logic using the selected self-hosted open-source instruction model; exact implementation pending spike | Project code, prompt record, selected dependencies and AI SBOM entry pending |
| Embedding component | Creates compatible embeddings for prepared document passages and supported user questions. Document embeddings are stored during indexing; a question embedding is sent to the vector search index at request time. | Multilingual embedding model and inference library; exact model, revision and version pending spike | AI SBOM and selected runtime dependency pending |
| Retriever | Sends the query embedding and retrieval settings to the vector database, reads the top-k passages and source metadata, and passes them to the reranker. | Python retrieval logic and the selected vector-database client; exact implementation pending spike | Project code and selected client dependency |
| Reranker | Scores the top-k candidate passages against the question and selects the top-n passages while retaining their source metadata. | Self-hosted multilingual reranking model; exact model, revision and runtime pending comparative experiments | AI SBOM and runtime dependency pending |
| Grounded answer generation and source formatting | Fills a version-controlled prompt template with the question, reranked passages and answer instructions; generates a Turkish answer; and assembles the retrieved-source list from passage metadata. | Python application code and an open-source instruction model and runtime; exact framework, model and response format pending | Project code, prompt record, selected dependencies, AI SBOM and runtime entries pending |
| Clear-decline handler | Produces a consistent refusal for unsupported or case-specific requests and returns it through the middleware and web interface. | Application rules and response templates | Project code and prompt/template records |
| Final response | Represents either a source-backed answer or a clear decline in a consistent structure. | Application response schema; exact implementation pending | Project code |
| Controlled evaluation | Runs the fixed evaluation set through the normal application flow and calculates retrieval, answer, citation, legal-status, refusal and latency measurements. | Project evaluation scripts; exact dependencies pending | Project code and selected dependencies |
| Weights & Biases | Tracks controlled baseline and later experiment runs. Each run records its Git commit, committed configuration, model and retrieval identifiers, per-test-case measurements and aggregate results. | Weights & Biases; exact client version to be pinned when configured | Client dependency and managed-service record pending |

## 5. Design details

### Data pipeline

1. A document manifest identifies each of the eight approved documents by its official URL, licence or terms-of-use information, publication or version date, collection date and file hash.
2. Approved source files are copied to controlled document storage so that the collection can be reproduced.
3. Text is extracted page by page. Content that cannot be extracted reliably is handled through a controlled manual process and independently checked.
4. Cleaning preserves Turkish characters, headings, article numbers, action or measure numbers, page numbers and document boundaries.
5. Text is divided primarily at meaningful source boundaries such as headings, articles, measures and action items. Size and overlap rules are used only when a source section is too long.
6. Each searchable passage keeps at least the document identifier and title, issuer, legal status, publication and collection dates, article or section, page where available, official URL and passage text.
7. The selected embedding component creates a document embedding for every prepared passage.
8. The search index stores each passage, its embedding and its source metadata together.
9. The collection is rebuilt only when an approved source or processing configuration changes. Automatic monitoring and updating remain out of scope.

### Model pipeline

The web interface does not communicate directly with the search index, retrieval logic or language model. Every question first enters the middleware/API, which passes it to the question-understanding step.

Question understanding remains outside the retrieval and grounded-answer stages of the RAG pipeline. It uses the selected self-hosted language model with separate instructions to:

- determine whether the assistant can handle the question;
- enhance supported questions and turn follow-ups into clear standalone questions for search; and
- direct unsupported requests to the clear-decline handler.

The middleware/API coordinates this flow and returns the resulting response to the web interface. These responsibilities may be implemented in the same Python application even though they are shown separately in the logical design.

The application retains the question text produced by Question Understanding for the duration of the request. The embedding component, reranker and answer-generation prompt all use that same text. Creating an embedding does not replace or discard the question text.

Supported questions enter the following proposed RAG model pipeline:

1. The embedding component creates a question embedding from the question text.
2. The retriever sends that embedding, the configured `top_k` candidate count and any permitted metadata filters to the vector search index.
3. The index returns the top-k matching passages together with their text, similarity scores and stored source metadata. The retriever passes these candidate records to the reranker.
4. A self-hosted multilingual reranker scores pairs of the retained question text and each candidate passage. It selects the top-n passages for the answer context, where `top_n` is no greater than `top_k`. The passage text and source metadata stay together throughout this step.
5. Within Grounded answer generation, the application fills a version-controlled prompt template with the retained question text, selected passages, source labels and answer instructions. The instructions require Turkish answers based on the supplied evidence, references to the supplied source labels and an insufficient-evidence response when the context does not support an answer.
6. The selected self-hosted language model generates the answer. The application assembles a separate source list from the top-n passages' stored document titles, sections or articles, pages where available, legal status, publication and collection dates and official URLs. Repeated source entries are merged using their document and passage identifiers.
7. The application returns the answer text, response type and source list to the web interface. The interface displays the answer and a labelled list of the retrieved sources used as context, with clickable official links and page or section details. Source labels in the prompt and source list use the same identifiers. Source titles, URLs and dates are taken from stored metadata rather than generated by the language model.

The candidate count `top_k`, context count `top_n` and reranker model identifier are version-controlled experiment settings. Reranking improves the ordering of the retrieved candidates; it cannot recover a passage that was absent from the initial retrieval results.

Unsupported requests bypass retrieval and the answer-generation call and are sent to the clear-decline handler. Both paths produce the same final response structure.

Each open chat accepts at most five user questions, including follow-up questions. The current chat context is held temporarily only for those exchanges and is discarded when the chat is reset or the application session ends. It is not written to persistent storage. A user who reaches the limit must begin a new chat.

### Evaluation

Controlled evaluation uses the normal application flow and receives its final structured responses. It is performed during planned baseline and experiment runs rather than during normal user conversations. Each W&B run records:

- the Git commit and committed configuration;
- the language-model, embedding and retrieval identifiers;
- the reranker identifier, candidate count `top_k` and selected context count `top_n`;
- a test-case ID without personal data;
- retrieval success against the expected document and section;
- answer correctness;
- citation support;
- legal-status accuracy;
- refusal behaviour;
- end-to-end latency; and
- aggregate results for the complete run.

Source documents, live user questions, personal data, complete conversations and complete prompts are not uploaded to W&B. Full test questions and generated answers remain in the controlled project evaluation files; W&B stores their test-case IDs and measurements so that runs can be compared without turning live conversations into evaluation data.

During controlled evaluation, team reviewers compare each sampled answer with its referenced passages and the original official documents. They record whether the passages support the answer, whether the displayed section or page matches the source and whether the legal-status label is correct. These results measure source support and formatting quality. Retrieval-only and retrieval-plus-reranking runs are compared using the same questions to measure changes in relevance and latency.

### Interfaces

| From | To | What passes | Format or protocol |
|---|---|---|---|
| Eight official documents | Document preparation | Approved source files and source information | HTTPS download or controlled manual import |
| Document preparation | Document files (PDF / JSONL) | Original files and processed records | Cloud storage interface |
| Document preparation | Document chunks | Prepared passage text and source metadata | Structured passage records |
| Document chunks | Embedding component | Passages and their source metadata | Internal model interface |
| Embedding component | Vector database | Document embeddings, passage text and source metadata | Database client or managed-service API |
| AI user | Web chat interface | Turkish question | Browser interaction over HTTPS |
| Web chat interface | Middleware / API | Current question and temporary chat identifier | Application request |
| Middleware / API | Question understanding | Current question and temporary context from the current five-question chat | Internal application interface |
| Question understanding | Embedding component | Question text | Internal model interface |
| Question understanding, through retained request data | Reranker | The same question text used to score each candidate passage | Internal model interface |
| Question understanding, through retained request data | Grounded answer generation and source formatting | The same question text used to construct the grounded prompt | Internal application interface |
| Question understanding | Clear-decline handler | Unsupported request category | Internal application interface |
| Embedding component | Retriever | Question embedding | Internal application object |
| Retriever | Vector database | Query embedding, `top_k` and permitted metadata filters | Search client or managed-service API |
| Vector database | Retriever | Top-k candidate passages, similarity scores and source metadata | Search client response |
| Retriever | Reranker | Candidate passages, similarity scores and source metadata | Internal application object |
| Reranker | Grounded answer generation and source formatting | Top-n selected passages, reranking scores and source metadata | Internal application object |
| Grounded answer generation and source formatting | Final response | Answer text, response type and source list assembled from selected passage metadata | Internal response object |
| Clear-decline handler | Final response | Decline message and refusal category | Internal response object |
| Final response | AI user, through Middleware / API and Web chat interface | Displayable answer or decline and the retrieved-source list | Application response and browser rendering |
| Final response | Controlled evaluation | Answers or declines and their measurements from controlled runs only | Project evaluation interface |
| Controlled evaluation | Weights & Biases | Git commit, configuration, test-case IDs, measurements and aggregate results | W&B API |

### Deployment

During development, document preparation and interface work may run on team computers or scheduled cloud compute. End-to-end model experiments and the MVP will use Google Cloud because the team does not have a suitable local GPU and has a fixed $100 Google Cloud credit.

The MVP is expected to use the smallest scheduled GPU-capable Google Cloud environment that meets the measured model and latency needs. The exact machine type, GPU, region, UI framework, search-index product, language model and inference runtime remain open until the related spikes are complete.

Only the web application endpoint will be reachable by pilot users. The middleware, search index, model runtime and credentials will remain private. Secrets will be stored outside the Git repository. Cloud compute will be stopped outside scheduled development, evaluation and demonstration periods.

High availability, automatic scaling and continuous public operation are outside the MVP.

## 6. Decisions

### D1: Separate middleware/API and question understanding before the RAG pipeline

**Context:** User requests require a controlled application entry point and a question-understanding step before retrieval. The UI must not call retrieval directly.

**Options considered:**

| Option | Pros | Cons |
|---|---|---|
| Web UI → middleware/API → question understanding → RAG pipeline | Clear responsibilities; one controlled entry point; question understanding remains outside retrieval and answer generation | Adds one processing stage and may increase latency |
| Web UI directly calling RAG | Smaller prototype | Mixes input handling and retrieval responsibilities |
| Separate deployed services for middleware and question understanding | Strong deployment separation | Adds unnecessary operational complexity for the MVP |

**Decision:** Use middleware/API and Question Understanding as separate logical components before the RAG pipeline. They may share one application process. Question Understanding and answer generation use the same self-hosted language model with separate instructions. Unsupported requests go to the decline handler before retrieval.

**Why:** This distinguishes application request handling from model-assisted interpretation while keeping the MVP deployment simple.

**Consequences:** Middleware and question understanding must be testable separately even if they share one application process. A supported question can require one model call for understanding and another for answer generation.

**Evidence:** A spike will demonstrate one supported question, one follow-up and one unsupported request through the proposed flow and measure the added latency of model-assisted question understanding.

**Owner and date:** Utku Uçar and Deniz Şenkutlu, 2026-10-25.

**Status:** proposed

### D2: Use reproducible, structure-aware document preparation

**Context:** Long policy documents and selected sections must remain traceable to their original structures and pages.

**Options considered:**

| Option | Pros | Cons |
|---|---|---|
| Page-aware extraction and structure-aware splitting | Preserves traceability and meaningful policy units | Some content may require manual correction |
| Fixed-size splitting only | Easy to implement | Can break articles, headings and measures |
| OCR for every document | Handles scanned pages | Adds errors and cost where text extraction already works |

**Decision:** Use page-aware extraction and meaningful source boundaries, with configurable size and overlap only as fallbacks.

**Why:** This preserves the source information required for citations without unnecessary processing.

**Consequences:** Difficult pages and manually prepared content require an independent quality check.

**Evidence:** The ingestion spike will compare sampled passages and their metadata with the official documents.

**Owner and date:** Utku Uçar, 2026-10-25.

**Status:** proposed

### D3: Use multilingual semantic retrieval followed by reranking

**Context:** The system needs Turkish semantic search and metadata-based filtering within a small project budget.

**Options considered:**

| Option | Pros | Cons |
|---|---|---|
| Multilingual semantic retrieval | Manageable baseline; captures similar meanings | May miss exact terms or article numbers |
| Combined semantic and keyword retrieval | Handles meaning and exact terms | Adds implementation and tuning work |
| Retrieval plus a separate reranker | May improve ordering | Adds another model and latency |

**Decision:** Use multilingual semantic retrieval with source-metadata filtering to return top-k candidate passages, then use a self-hosted multilingual reranker to select the top-n passages for answer generation. Select the embedding model, reranker and search-index product after comparative experiments.

**Why:** The initial vector search finds a candidate pool, and the reranker evaluates each candidate against the question before selecting the answer context.

**Consequences:** Reranking adds model inference time and memory use. Candidate and context counts must be tuned within the available compute budget. A retrieval-only configuration will be retained as an evaluation baseline. Keyword retrieval remains an optional improvement.

**Evidence:** The retrieval spike will compare retrieval-only and retrieval-plus-reranking configurations against expected documents and sections in the same evaluation set, recording relevance and latency.

**Owner and date:** Elif Yeşim Koçoğlu, 2026-10-25.

**Status:** proposed

### D4: Use a self-hosted open-source language model

**Context:** Turkish question understanding and grounded answer generation are required without depending on a paid external language-model API.

**Options considered:**

| Option | Pros | Cons |
|---|---|---|
| Self-hosted open-source instruction model | Keeps inference under team control; no per-token API charge | Requires compute capacity and operational work |
| Smaller self-hosted model | Lower compute cost | May reduce grounded-answer quality |
| Hosted commercial model API | Easy to use | Adds an external dependency and usage cost |

**Decision:** Evaluate open-source instruction models and inference runtimes that fit the available GPU and budget. Use the selected model for question understanding and answer generation with separate instructions. Do not select an exact model before the spike.

**Why:** Turkish quality, groundedness, refusal behaviour, latency and memory use must be measured rather than assumed.

**Consequences:** The accepted model, revision, quantization and runtime will be pinned in configuration and the AI SBOM.

**Evidence:** The generation spike will measure question understanding, grounded Turkish answers, refusal behaviour, latency and GPU memory.

**Owner and date:** Deniz Şenkutlu and Elif Yeşim Koçoğlu, 2026-10-25.

**Status:** proposed

### D5: Use scheduled Google Cloud compute

**Context:** The team has no suitable local GPU and must remain within the fixed $100 Google Cloud credit.

**Options considered:**

| Option | Pros | Cons |
|---|---|---|
| One scheduled GPU-capable cloud environment | Simple deployment and controlled cost | Limited availability and dependent on quota |
| Local-only deployment | No cloud spending | Insufficient compute and limited pilot access |
| Multiple managed services or Kubernetes | Better separation and scaling | Too complex and expensive for the MVP |

**Decision:** Use the smallest scheduled Google Cloud compute configuration that passes the model and end-to-end spikes. Keep machine type, GPU and region open until quota, performance and cost are verified.

**Why:** It meets the compute and browser-access needs without assuming continuous operation.

**Consequences:** Billing alerts, shutdown procedures and limited demonstration windows are required.

**Evidence:** The deployment spike will verify quota, model startup, one end-to-end question and projected credit usage.

**Owner and date:** Elif Yeşim Koçoğlu, 2026-10-25.

**Status:** proposed

### D6: Use Weights & Biases for controlled experiment tracking

**Context:** Weights & Biases is the required experiment-tracking platform for the project. Experiment tracking must still avoid uploading personal data, live conversations and unnecessary source content.

**Options considered:**

| Option | Pros | Cons |
|---|---|---|
| W&B with configuration, test-case IDs, measurements and aggregate results | Uses the required platform; supports reproducibility and run comparison without storing live conversations | Requires a reviewed logging schema |
| W&B with aggregate results only | Minimizes stored data | Makes individual test failures harder to compare |
| W&B with complete prompts, answers and conversations | Detailed debugging | Stores more content than required and may capture prohibited data |

**Decision:** Use Weights & Biases for controlled baseline and experiment runs. Record the Git commit, committed configuration, model and retrieval identifiers, test-case IDs, per-case measurements and aggregate results. Do not send live user conversations, personal data, source documents or complete prompts.

**Why:** This supports reproducibility while following data-minimization constraints.

**Consequences:** Evaluation files remain the source of full test questions and answers. The W&B logging schema must be reviewed before the first baseline run.

**Evidence:** An evaluation spike will confirm that a run can be traced to its Git commit and configuration without prohibited content.

**Owner and date:** All Data Scientists, 2026-10-25.

**Status:** proposed

### D7: Assemble source information from passage metadata

**Context:** Answers must show traceable document, section, page, date and legal-status information. The application needs a consistent way to present this information alongside generated text.

**Options considered:**

| Option | Pros | Cons |
|---|---|---|
| Application-built source list from selected passage metadata | Consistent fields and official links; straightforward implementation | Lists the supplied context; source support still needs evaluation |
| Model-generated answer and complete source list | Less formatting code | Titles, dates and URLs can be generated incorrectly |
| Fixed extractive response template | Easy to trace each excerpt to a source | Less flexible for Turkish explanations and comparisons |

**Decision:** Generate the answer from the reranked passages using a version-controlled prompt template. Give each context passage a source label and carry the same label into an application-built source list. Assemble document titles, section or article details, page numbers, legal status, dates and official links from the selected passages' metadata. Present the answer and retrieved-source list as separate fields in the response.

**Why:** This keeps source presentation consistent with the indexed collection and gives reviewers the original passages and links needed to assess the answer.

**Consequences:** The application needs a response schema and a source-list formatter. Missing page information must be shown as unavailable, and repeated source entries must be merged. The displayed list identifies the context supplied to the model; the team measures whether the answer is supported by that context during controlled evaluation.

**Evidence:** A prototype response will show one generated Turkish answer and a source list built from fixed passage metadata. Reviewers will compare its fields and links with the original documents and assess answer support using the evaluation rubric.

**Owner and date:** Elif Yeşim Koçoğlu and Deniz Şenkutlu, 2026-11-03.

**Status:** proposed

## 7. Open design areas

- Text-extraction library and exact version.
- Passage size, overlap and document-specific splitting rules.
- Multilingual retrieval model, revision and search representation.
- Multilingual reranker model, revision, runtime and inference batch size.
- Vector database or equivalent search-index implementation.
- Web-interface and middleware frameworks.
- Question-understanding instructions and implementation.
- Open-source language model, revision, quantization and inference runtime.
- Retrieval candidate count `top_k`, reranked context count `top_n` and any retrieval acceptance threshold.
- Whether keyword retrieval is required.
- Final-response schema, source-label format and handling of unavailable source fields.
- Google Cloud machine type, GPU, region and operating schedule.
- W&B workspace access, client version and retention policy.

## 8. Change log

| Version | Date | Change | Pull request |
|---|---|---|---|
| v1 | 2026-10-27 | First proposed system architecture with high-level and detailed RAG views | — |
| v2 | 2026-11-09 | Added the PNG architecture diagram covering document indexing, retrieval, reranking and controlled evaluation; aligned component and interface descriptions with the diagram | — |

## Checklist before submitting

- Every box in the architecture diagram has a corresponding row in Components or is an explicitly named use of the shared Embedding component.
- Every arrow in the architecture diagram has a corresponding row in Interfaces.
- The retriever sends the question embedding to the vector database and forwards the returned top-k passages and source metadata to the reranker.
- The application retains question text for reranking and answer generation; the reranker passes the top-n selected passages and metadata to answer generation.
- Middleware/API and question understanding occur before retrieval and grounded answer generation.
- The web interface does not connect directly to retrieval or the model.
- The model pipeline describes prompt assembly and response formatting, with displayed source metadata read from index records.
- Every accepted technology is covered by a decision in section 6 and will be recorded in the relevant SBOM under the same name and version.
- Every unresolved implementation choice appears in Open design areas.
- The diagram version matches the latest change-log entry.

## References

1. [GitLab Design Document Template](https://gitlab.com/gitlab-com/content-sites/handbook/-/blob/main/content/handbook/engineering/architecture/design-documents/_template.md)
2. [GitLab Architecture Design Workflow](https://handbook.gitlab.com/handbook/engineering/architecture/workflow/)
