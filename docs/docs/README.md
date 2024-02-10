---
sidebar_position: 0
title: What is Rubra?
---

# Introduction

## Overview
Rubra is an open-source ChatGPT. It's designed for users who want to:

* **Engage with LLMs:** Utilize a chat UI that offers benefits such as multi-model selection and caching to save on token costs.
* **Develop and Utilize Assistants:** An Assistant is an LLM with access to tools. With Rubra, you can select from a variety of LLMs, including a Rubra-optimized local one, and tools to create your own assistant.
* **OpenAI Compatible API:** Rubra provides an API that is compatible with OpenAI's assistants API, allowing you to use OpenAI's Python and JavaScript libraries to interact with Rubra.
* **Self-Host:** Rubra is designed to be self-hosted, which helps ensure that your data stays private and secure.

## Key Components

### Large Language Models
Rubra allows you to interact with a variety of large language models in one place. Rubra ships with a local model and allows you to connect to other models, such as ones from OpenAI and Anthropic.

### Tools
Rubra provides a variety of tools to help you develop and utilize your own assistants. These tools include:
- **Web Search**: Allow your assistant to utilize the web to find information.
- **Knowledge Retrieval**: Augment your assitant with knowledge from files you upload. Once you upload your files, Rubra will automatically chunk your documents, index and store the embeddings, and implement retrieval augmented generation (RAG) to answer queries related to the documents.

OpenAI's tools cost money. Code interpreter costs $0.03 per session and Knowledge Retrieval costs $0.20/GB per assistant per day. Rubra runs on your own hardware and is free.

Function calling, code interpreter, and more tools will be available soon.

### Interfaces

#### Chat UI
Rubra provides a familiar chat interface that allows you to interact with your models and assistants. You can:

- Create assistants with a few clicks - no coding necessary
- Manage models and API keys
- Chat with your LLMs and assistants

#### OpenAI Compatible API

Rubra provides an API that is compatible with OpenAI's assistants API, allowing you to use OpenAI's Python and JavaScript libraries to interact with Rubra. Simply:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000",  # points at locally running Rubra backend
    api_key=""
)

assistant = client.beta.assistants.create(
  instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
  model="rubra_local",
  tools=[{"type": "retrieval"}],
  file_ids=[client.files.create(file=open("knowledge.txt", "rb"),purpose='assistants').id]
)
```

## Getting Started

Rubra is designed to run on your machine, ensuring your data remains private and secure. Refer to the [quickstart guide](./quickstart) to get started!
