---
sidebar_position: 0
title: What is Rubra?
---

# Introduction

## Overview
Rubra is an open-source ChatGPT. It's designed for users who want to:

* **Engage with LLMs:** Utilize a familiar and straightforward chat interface that offers benefits such as multi-model selection and caching to save on token costs.
* **Develop and Utilize Assistants:** Rubra enables the creation of assistants that utilize LLMs and tools like file knowledge and web browsing. Unlike OpenAI assistants, Rubra supports assistant streaming for OpenAI models, Claude, and local models.
* **Employ OpenAI Compatible API:** Rubra serves as a drop-in replacement for OpenAI's API, allowing the use of OpenAI python and javascript libraries to interact with Rubra.
* **Self-Host:** Rubra is designed for self-hosting, ensuring your data remains private and secure.

## Key Components

### Rubra Frontend
- **Offers a familiar, ChatGPT-style interface** 
  - Develop assistants with a few clicks - no coding necessary
    - Personalize your assistant's name, description, and enhance its knowledge by uploading files for automated RAG
  - Engage with your assistants and various proprietary LLMs like GPT4 and Claude

### Rubra Backend
- **OpenAI Compatibility:** Serves as a drop-in replacement for OpenAI's API, facilitating seamless integration with existing functionality. Refer to the [API](/api) for more details
- **Support for Multiple Models:** Supports a variety of AI models, including Claude, Gemini, and open-source options
- **Scalability:** Rubra is designed to scale to meet your usage requirements, without the need for complex configurations

## Getting Started
- **Self-Hosted:** Rubra is designed for self-hosting, ensuring your data remains private and secure. Refer to the [installation guide](/installation/installation) to get started
- **Cloud:** One-click deployment to [Acorn](https://www.acorn.io/) and AWS ECS instructions will be available soon

![Architecture Diagram](/img/application-architecture-diagram.svg)