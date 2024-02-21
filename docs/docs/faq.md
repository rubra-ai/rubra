---
sidebar_position: 4
title: FAQ
---

# Frequently Asked Questions

This page will cover common questions and issues that users may encounter when using Rubra.

### FAQ

#### Who is Rubra designed for?
Rubra is for anyone using OpenAI to develop LLM applications. Rubra allows you to locally develop your assistants, ensuring data privacy and reducing costs.

#### Why would I use Rubra instead of OpenAI’s Assistants API?
Rubra allows you to develop your assistants locally without having to pay for tools and chat completions.

#### Why would I use Rubra instead of ChatGPT?
Rubra allows you to chat with your LLMs and Assistants while keeping your data private, secure, and local.

#### How is Rubra different from Local AI, Ollama, and LM Studio?
Local AI, Ollama, and LM Studio are all great model inferencing engines for chat completions. In addition to model inferencing, Rubra provides an OpenAI compatible Assistants API powered by our optimized LLM.

#### How is Rubra different from Langchain OpenGPTs?
Rubra ships with an optimized LLM and includes built-in tools to get you started building assistants immediately. Additionally, Rubra is OpenAI API compatible, so you can easily shift back and forth between local and cloud development.

#### What makes Rubra private and secure?
Rubra runs on your machine. Additionally, your chat history and the files you use for knowledge retrieval (RAG) never leave your machine.

#### Does Rubra support other models?
Yes, Rubra supports OpenAI and Anthropic models in addition to the Rubra local model or one that [you configure yourself](https://github.com/rubra-ai/rubra/tree/main/deploy_local_llm). We are working on introducing larger, more capable local models in the near future.

#### Why isn't knowledge retrieval working?
Our RAG pipeline uses an embedding model. If you're running in quickstart mode, the model is running on CPU and could be very slow, depending on machine. If you just created the assistant, it may take a few minutes to index the knowledge base. If you're still having issues, please check the logs for any errors.

* On macOS:
  * You need to install the Xcode Command Line Tools: `xcode-select --install`
  * ```ImportError: libtorch_cpu.so: cannot enable executable stack as shared object requires: Invalid argument``` can be resolved by not using Rosetta for x86/amd64 emulation on Apple Silicon in Docker.

#### How do I force remove data?

If you need to [remove all Rubra data](/installation/uninstall), you can use the following command:

```bash
curl -sfL https://get.rubra.ai | sh -s -- delete
```
