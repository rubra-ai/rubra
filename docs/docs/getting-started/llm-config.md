---
id: llm-config
title: LLM Configuration
sidebar_label: Configure LLMs
---

Before getting started with Rubra, make sure you configure what models you want to give Rubra access to by editing the `llm-config.yaml` file.

We currently use [LiteLLM](https://docs.litellm.ai/docs/proxy/configs#quick-start) as the chat completions server. This may change in the future.

The models currently supported:

* OpenAI
  * GPT-4-turbo (*gpt-4-1106-preview*)
* Anthropic
  * claude-2.1
* Local Models
  * See [Local LLM Deployment](/getting-started/prerequisites#local-llm-deployment-optional) for more information
  * Must be named `openai/custom`

This is what you config file should look like:

```yaml
model_list:
  - model_name: gpt-4-1106-preview
    litellm_params:
      model: gpt-4-1106-preview
      api_key: "OPENAI_API_KEY"
      custom_llm_provider: "openai"
  - model_name: claude-2.1
    litellm_params:
      model: claude-2.1
      api_key: "CLAUDE_API_KEY"
  # the following is for locally running LLMs deployed with LM Studio or llama.cpp
  - model_name: custom 
    litellm_params:
      model: openai/custom
      api_base: "http://host.docker.internal:1234/v1"  # host.docker.internal allows docker to use your local machine's IP address (localhost)
      api_key: "None"
      custom_llm_provider: "openai"
  
litellm_settings:
  drop_params: True
  set_verbose: True
  cache: True

# For caching
environment_variables:
  REDIS_HOST: "redis"
  REDIS_PORT: "6379"
  REDIS_PASSWORD: ""
```

Edit model list to include the models you want to use. To use Rubra, you need to specify at least one model.

[Architecture Diagram] (/img/llm-config.svg)
