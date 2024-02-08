---
title: Intro
slug: /
position: 0
---

# Introduction

## Overview

Rubra is an open source platform that merges a ChatGPT-like interface with an OpenAI compatible backend. No need to change your existing LLM apps that leverage OpenAI assistants, Rubra is a drop in replacement for OpenAI's API.

With Rubra you get a chat inreface that is familiar to users, and a backend that is familiar to developers. Create assistants with a few clicks through the UI or through code. Use locally running LLMs or use proprietary ones like GPT4 and Claude. Rubra allows you to mix and match.

Most importantly, **you are in control of your data** - Rubra is designed to be self-hosted, allowing you to keep your data private and secure.

## Key Components

### Rubra Frontend

- **Features a familiar, ChatGPT-style interface**
  - Create assistants with a few clicks - no coding required
    - Customize your assistant's name, description, and give it knowledge by uploading files for automated RAG
  - Chat with your assistants and various proprietary LLMs like GPT4 and Claude

### Rubra Backend

- **OpenAI Compatibility:** Drop in replacement for OpenAI's API, allowing for seamless integration with existing functionality. Check out the [API](https://platform.openai.com/docs/introduction) for more information
- **Support for Multiple Models:** Accommodates various AI models, including Claude, Gemini, and open-source options
- **Scalability:** Rubra leverages docker - so you can easily scale up Rubra components to meet your consumption requirements

## Getting Started

- **Self-Hosted:** Rubra is designed to be self-hosted, allowing you to keep your data private and secure. Check out the [installation guide](/getting-started/installation) to get started
- **Cloud:** One click deploy to [Acorn](https://www.acorn.io/) and AWS ECS instructions coming soon

[Architecture Diagram] (/img/application-architecture-diagram.png)
