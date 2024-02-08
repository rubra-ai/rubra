---
id: prerequisites
title: Prerequisites
sidebar_label: Prerequisites
sidebar_position: 0
---

Before getting started with Rubra, make sure you have the following prerequisites installed on your machine:

## Docker Desktop

Rubra relies on Docker Desktop to run the application and manage the development environment. Docker Desktop includes Docker Compose, which allows you to define and run multi-container Docker applications.

### Mac

To install Docker Desktop on macOS, follow these steps:

1. Visit the [Docker Desktop for Mac installation guide](https://docs.docker.com/desktop/install/mac-install/) and follow the instructions provided.

### Linux

To install Docker Desktop on Linux, follow these steps:

1. Visit the [Docker Desktop for Linux installation guide](https://docs.docker.com/desktop/install/linux-install/) and follow the instructions provided.

### Windows

To install Docker Desktop on Windows, follow these steps:

1. Visit the [Docker Desktop for Windows installation guide](https://docs.docker.com/desktop/install/windows-install/) and follow the instructions provided.

---

## Local LLM Deployment (Optional)

You must run a model locally if you'd like to create assistants that run on 100% on your machine. We recommend the [OpenHermes model](https://huggingface.co/teknium/OpenHermes-2.5-Mistral-7B). We have tested Rubra with [this quanitized variant](https://huggingface.co/TheBloke/OpenHermes-2.5-neural-chat-v3-3-Slerp-GGUF) of the OpenHermes model, but you can use any model you want at your own risk. Let us know if you'd like support for other models!

### LM Studio

1. Download LM Studio from [https://lmstudio.ai/](https://lmstudio.ai/) and the model you want to use.
2. Go to the "local inference server" tab, load the model and configure your settings.
3. Click "Start server". By default, LM Studio runs on [http://localhost:1234](http://localhost:1234) but you can configure this.

### llama.cpp

#### Suggested approach

Follow instructions found in the [llama.cpp repo](https://github.com/ggerganov/llama.cpp).

#### Alternative approach

We have a pre-built docker image for llama.cpp that can be uncommented and enabled in docker-compose.yml

* Does not take advantage of GPU acceleration, so it is slower
* We will add NVIDIA GPU support soon
* Docker doesn't work with Apple Silicon. We recommend running llama.cpp natively if you're looking to leverage the iGPU found in M series Macs.
