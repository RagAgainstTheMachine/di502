# Front-end options for the web chat page

**Purpose:** compare ways to build the web chat page (Major Activities row 12, Jira DI502-65) so the team can choose one at sprint planning. This is a research note, not a decision.

## What the page must do

Taken from the charter, User Story Map v3 and the [System Architecture Design Document](../Markdown%20Template/11-system-architecture-design-document.md):

| # | Need | Source |
|---|---|---|
| 1 | Chat in Turkish: a question box and answers shown as formatted text | F1, US-1 |
| 2 | Show each answer's sources with document, article or section, and a link to the official URL | F2, US-6 |
| 3 | Show each cited source's legal status and date | F3, US-7 |
| 4 | Show the collection date before a question is asked | F6, US-8, D8 |
| 5 | Keep the conversation only while the chat is open (up to five questions), with a way to start a new chat | F4, US-9, architecture document |
| 6 | Show a "do not enter personal data" notice; no login and no personal-data fields | C-08, C-11 |
| 7 | Talk only to the middleware/API, never to the search index or model directly | Architecture document, D1 |
| 8 | Run locally for the alpha and on one Google Cloud machine for the beta | C-07, architecture document |
| 9 | Python, so the whole team can work on it | Architecture document |
| 10 | Send no usage data or conversations to outside services | C-11 |

## Options

### Gradio

A Python library for building simple web interfaces, widely used for machine-learning demos.

- **Chat support:** `gr.ChatInterface` gives a ready chat page; `gr.Blocks` allows a custom layout, for example a collection-date banner above the chat and a sources panel beside it.
- **Sources and links:** answers are rendered as Markdown, so citations can be shown as links. A separate panel for sources takes a little layout work.
- **Session context:** `gr.State` keeps data per browser tab and is lost when the tab closes, which fits need 5.
- **Middleware:** it can run as its own app that calls the middleware over HTTP, or be mounted inside a FastAPI app.
- **Watch out for:** turn off usage analytics (`analytics_enabled=False` or the `GRADIO_ANALYTICS_ENABLED` setting). Never use `share=True` with pilot users, because it sends traffic through Gradio's public relay servers.
- **Effort:** low.

### Streamlit

A Python library for data apps, where the page is a script that reruns on each interaction.

- **Chat support:** `st.chat_message` and `st.chat_input` give a chat layout in a few lines.
- **Sources and links:** Markdown, expanders and columns make a sources section easy.
- **Session context:** `st.session_state` keeps data per browser session.
- **Middleware:** it calls the middleware over HTTP. It does not mount inside FastAPI.
- **Watch out for:** turn off usage statistics (`browser.gatherUsageStats = false`). Because the whole script reruns on each message, long model calls must not be repeated by accident.
- **Effort:** low.

### Chainlit

A Python framework made specifically for chat assistants built on language models.

- **Chat support:** a full chat page out of the box, including streaming answers and a "new chat" button.
- **Sources and links:** built-in "elements" can show source passages next to an answer, which suits needs 2 and 3 well.
- **Session context:** a per-chat user session, held in memory.
- **Middleware:** it can call the middleware over HTTP; it runs on FastAPI underneath.
- **Watch out for:** turn off telemetry in its configuration file. Do not enable its optional login or chat-history storage, which C-08 and C-11 rule out.
- **Effort:** low to medium.

### NiceGUI

A Python library for general web interfaces, built on FastAPI and Vue.

- **Chat support:** has chat-message components, but the page is assembled by hand.
- **Strength:** more freedom over layout than Gradio or Streamlit while staying in Python.
- **Effort:** medium.

### FastAPI with a plain HTML page

The middleware serves one HTML page, with a little JavaScript or HTMX for sending questions.

- **Strength:** full control over layout and what is sent where; no extra framework to learn or configure.
- **Weakness:** the team writes the chat behaviour, styling and error handling itself.
- **Effort:** medium to high.

### Reflex

A Python framework that compiles to a React web app.

- **Strength:** looks like a modern web app.
- **Weakness:** a build step and a larger framework than this project needs.
- **Effort:** high.

### Open WebUI (not suitable)

A complete open-source chat application for language models. It is built around user accounts and saved chat history, which conflicts with C-08 and C-11, so it is not considered further.

## Comparison

| | Gradio | Streamlit | Chainlit | NiceGUI | FastAPI + HTML |
|---|---|---|---|---|---|
| Ready chat page | Yes | Yes | Yes | Partly | No |
| Showing sources and labels | Good with Blocks | Good | Very good | Good | Full control |
| Per-chat memory only | Yes | Yes | Yes | Yes | Yes |
| Usage data to turn off | Analytics | Usage stats | Telemetry | – | – |
| Fits the middleware design | Yes | Yes | Yes | Yes | Yes |
| Effort for the alpha | Low | Low | Low–medium | Medium | Medium–high |

Record the final choice in the System Architecture Design Document (Open design areas: "Web-interface and middleware frameworks").
