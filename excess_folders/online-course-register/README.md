# DI 502: Online Course Register

## Sprint 1 fundamentals

Most of you are new to at least some of these topics. By the **end of Sprint 1 (28/10)**, every team member should be able to do the following. Use the timeboxed learning spikes in Sprint 1 to close your gaps, and pair with a teammate who already knows the topic.

| Topic | You should be able to… | Suggested resource |
| --- | --- | --- |
| **Git & GitHub** | Clone a repository, create a branch, commit, push, open a pull request, review a teammate's pull request and resolve a merge conflict. | [*Pro Git*](https://git-scm.com/book/en/v2) (free online book), chapters 1–3. Prefer a guided course? Take DataCamp's [Introduction to Git](https://app.datacamp.com/learn/courses/introduction-to-git), then [Intermediate Git](https://app.datacamp.com/learn/courses/intermediate-git) for branching and conflicts. |
| **Markdown** | Write headings, lists, tables, code blocks, links and GitHub note boxes (`> [!NOTE]`). | GitHub Docs: ["Basic writing and formatting syntax"](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) (note boxes are under [Alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts)) |
| **Scrum basics** | Explain the Scrum roles, events and artefacts, and the difference between a user story, a task and a spike. | Scrum.org ["What is Scrum?"](https://www.scrum.org/resources/what-scrum-module) and its [introductory video series](https://www.scrum.org/resources/introductory-video-series-scrum), and the [Scrum Guide](https://scrumguides.org/scrum-guide.html) |
| **Jira** | Create stories, spikes and sub-tasks, plan a sprint, move issues on the board and link issues to GitHub through Jira keys. | Coursera: [*Agile with Atlassian Jira*](https://www.coursera.org/learn/agile-atlassian-jira) (Scrum module and lab). A shorter, non-technical option is Atlassian Community's [Get the most out of Jira](https://community.atlassian.com/learning/path/get-the-most-out-of-jira). |
| **LLM basics** | Explain what a token, a context window, a prompt and temperature are, and why LLMs hallucinate. Run a small open-source model in Colab. | Workshop material (14/10) |
| **Embeddings & vector search** | Explain what an embedding is and how similarity search finds relevant passages. | Workshop material (14/10) |
| **RAG** | Explain the indexing and query phases of a RAG pipeline and why RAG reduces hallucination. | [Lewis et al. (2020)](https://arxiv.org/abs/2005.11401) and the lecture slides |
| **Prompt engineering** | Write a prompt that tells the model to answer only from the given passages and to say when it does not know. | Workshop material |
| **Evaluation basics** | Explain what an evaluation set is, why it must be fixed before experiments, and what "the gold article is in the top 5 results" measures. | Lecture slides: "Requirements, scope and acceptance criteria" |
| **Python environment** | Create a virtual environment, install packages and pin exact versions in `requirements.txt`. | Python documentation: ["venv"](https://docs.python.org/3/library/venv.html) |
| **Chat interface** | Build a "hello world" chat app with Gradio's `ChatInterface`. | Gradio documentation: [ChatInterface guide](https://www.gradio.app/guides/creating-a-chatbot-fast) |

## Optional course register

This register is a compilation of many online courses and other resources to help you achieve the goals you set forward.

Each material is provided with a link to access it, a summary of its contents, what kind of background is necessary beforehand as well as a suggested time window for its completion.

The courses listed here are only a **recommendation**, and you are free to search for and complete courses that interest you.

### Contents

1. [Prelude to Project](#prelude-to-project)
2. [Software Engineering / Coding](#software-engineering--coding)
3. [Large Language Models](#large-language-models)
4. [Retrieval Augmented Generation](#retrieval-augmented-generation)
5. [Deployment](#deployment)
6. [Graphical User Interface](#graphical-user-interface)
7. [More Courses](#more-courses)

### Prelude to Project

#### [Teamwork Foundations (LinkedIn Learning)](https://www.linkedin.com/learning/teamwork-foundations-2020)

- **Summary:** A non-technical course on how to use your strengths effectively in groups as well as how to solve common problems

- **Who is this for:** Anyone looking to improve their capacity to work in a team

- **Best time to take:** As early as possible

### Software Engineering / Coding

#### [Software Engineering Principles in Python](https://app.datacamp.com/learn/courses/software-engineering-principles-in-python)

- **Summary:** A technical course on how to write maintainable code with little repetition as well as writing unit tests for your applications

- **Who is this for:** Developers and data scientists looking to improve their coding skills with regards to OOP practices and other guidelines

- **Best time to take:** As early as possible

**Note:** *You can also check this blog post for the highlights: [6 Python Best Practices for Better Code \| DataCamp](https://www.datacamp.com/blog/python-best-practices-for-better-code)*

### Large Language Models

#### [Introduction to LLMs in Python](https://app.datacamp.com/learn/courses/introduction-to-llms-in-python)

- **Summary:** A technical course on how the transformer architecture works for different language tasks. It also introduces evaluation techniques and fine-tuning.

- **Who is this for:** Developers familiar with deep learning but not with transformers or natural language generation.

- **Best time to take:** Sprint 1

#### [Large Language Models (LLMs) Concepts](https://app.datacamp.com/learn/courses/large-language-models-llms-concepts)

- **Summary:** A non-technical course on how LLMs operate at a high level.

- **Who is this for:** Those not familiar with deep learning, but need to understand the product's capabilities and limitations.

- **Best time to take:** Sprint 1

#### [LLMops Concepts](https://app.datacamp.com/learn/courses/llmops-concepts)

- **Summary:** A non-technical course on how LLM based applications are developed and deployed at a high level.

- **Who is this for:** Those not familiar with deep learning, but need to lead a team that will develop such a product.

- **Best time to take:** Sprint 1

#### [LLMOps (DeepLearning.AI)](https://learn.deeplearning.ai/courses/llmops)

- **Summary:** A technical course demonstrating the integration of google cloud services to LLM based application development

- **Who is this for:** Developers with a good grasp of LLMs looking to explore google cloud

- **Best time to take:** Sprint 1

#### [Responsible AI Practices](https://app.datacamp.com/learn/courses/responsible-ai-practices)

- **Summary:** A non technical course on the ethical considerations of building and using AI applications, how to deal with them as well as the scope of regulations

- **Who is this for:** Product owners and developers who want to build a safe chatbot up to par with emerging AI regulations

- **Best time to take:** Sprint 1-2

### Retrieval Augmented Generation

#### [Retrieval Augmented Generation (RAG) with LangChain](https://app.datacamp.com/learn/courses/retrieval-augmented-generation-rag-with-langchain)

- **Summary:** A comprehensive, technical course showing many LangChain utilities for preparing data, as well as handling the generation of an LLM

- **Who is this for:** Developers with a good grasp on LLMs ready to test RAG apps.

- **Best time to take:** Sprint 2

**Tip:** *While this and many other courses use an OpenAI LLM, you can check this article for using an open source model: [RAG With Llama 3.1 8B, Ollama, and Langchain: Tutorial \| DataCamp](https://www.datacamp.com/tutorial/llama-3-1-rag)*

#### [LangChain Chat with Your Data](https://www.deeplearning.ai/courses/langchain-chat-with-your-data)

- **Summary:** Another comprehensive, technical course on building RAG applications with LangChain. Unlike in Datacamp, there is no handholding here in coding as sessions are run with singular notebooks instead of divided parts.

- **Who is this for:** Developers with a good grasp on LLMs ready to test RAG apps.

- **Best time to take:** Sprint 2

#### [Retrieval Augmented Generation](https://www.deeplearning.ai/courses/retrieval-augmented-generation)

- **Summary:** An intermediate level course on building scalable RAG applications with a focus on handling dataset changes and features like logging for debugging purposes. First two modules are covered by the two courses above.

- **Who is this for:** Developers with a basic understanding of RAG who want to improve their application.

- **Best time to take:** Sprint 3

#### [Building and Evaluating Advanced RAG Applications (DeepLearning.AI)](https://www.deeplearning.ai/short-courses/building-evaluating-advanced-rag/)

- **Summary:** A technical course demonstrating the development of a RAG application with LlamaIndex and the evaluation of the application with trulens.

- **Who is this for:** Developers with a good grasp on LLMs looking to test the LlamaIndex environment as well as evaluating the answers to given queries

- **Best time to take:** Sprint 2

#### [Evaluating and Debugging Generative AI (DeepLearning.AI)](https://www.deeplearning.ai/short-courses/evaluating-debugging-generative-ai/)

- **Summary:** A technical course demonstrating how Weights and Biases (wandb) can be integrated with many generative ai applications including LLMs

- **Who is this for**: Developers with a good grasp on LLMs looking to track their prompts and evaluate their application in systematic way

- **Best time to take**: Sprint 2

**Tip:** *To see how Weights and Biases can be used to track performance metrics you can check out the following: [Tutorial: Evaluate LLM application performance](https://github.com/wandb/examples/blob/master/colabs/prompts/prompts_evaluation.ipynb)*

### Deployment

#### [Kubernetes in Google Cloud](https://www.skills.google/course_templates/744?catalog_rank=%7B%22rank%22%3A8%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&search_id=102373164)

- **Summary:** A series of labs on using Docker for containerization, an deployment via Kubernetes engine.
- **Who is this for:** Developers who want to learn about conteinerizing and deploying an app.
- **Best time to take:** Sprint 2-3



#### [Google Cloud Billing: Interactive Tutorials](https://cloud.google.com/billing/docs/interactive-tutorials)

- **Summary:** A series of tutorials on how costs can be tracked with reports and managed with budgeting tools in google cloud

- **Who is this for:** Developers looking to optimize costs while deploying their product

- **Best time to take:** Sprint 2-3

**Tip:** You can also take a look at the following resources for more:

- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator?hl=en)

- [Understanding and Analyzing Your Costs with Google Cloud Billing Reports (Lab)](https://www.cloudskillsboost.google/catalog_lab/2004)

- [Optimize Your Google Cloud Costs](https://www.cloudskillsboost.google/course_templates/767)

**While the GCP lab on VertexAI integration with langchain was removed, feel free to check related documentation page to get an idea: [ChatVertexAI \| 🦜️🔗 LangChain](https://python.langchain.com/docs/integrations/chat/google_vertex_ai_palm/)**

### Graphical User Interface

#### [Building Generative AI Applications with Gradio](https://www.deeplearning.ai/short-courses/building-generative-ai-applications-with-gradio/)

- **Summary:** A technical course on how to design an interactive app for many generative ai applications including a chatbot.

- **Who is this for:** Developers with a prototype RAG looking to give their app a facelift and add new features.

- **Best time to take:** Sprint 2-3

**Note:** There are many more python based GUI options, such as Streamlit. Below you can find tutorials for it:

- [Build a basic LLM chat app - Streamlit Docs](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)

- [Build an LLM app using LangChain - Streamlit Docs](https://docs.streamlit.io/develop/tutorials/llms/llm-quickstart)

### More Courses

We highly recommend the following Carnegie Mellon course: [Machine Learning in Production / AI Engineering](https://mlip-cmu.github.io/s2026/)

This is not an online course but lecture videos, labs and reading materials are provided.

For Sprint 1, consider watching the "Setting Goals, Gathering Requirements" lecture, as it touches on many AI applications including  chatbots and computer vision. 

You can find more courses by visiting the following links:

[Learn - Datacamp](https://app.datacamp.com/learn)

[Courses - DeepLearning.AI](https://www.deeplearning.ai/courses/)

[Catalog - Google Cloud Skills Boost](https://www.cloudskillsboost.google/catalog)
