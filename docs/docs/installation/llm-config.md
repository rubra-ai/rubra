---
id: llm-config
title: LLM Configuration
sidebar_label: LLM Configuration File
sidebar_position: 3
---

Before you start with Rubra, configure the models you want Rubra to access by editing the [`llm-config.yaml`](https://github.com/acorn-io/rubra/blob/main/llm-config.yaml) file.

The models currently supported:
* OpenAI
  * GPT-4-turbo (*gpt-4-1106-preview*)
* Anthropic
  * claude-2.1
* Local Models
  * Refer to [Local LLM Deployment](/installation/prerequisites#local-llm-deployment-optional) for more details
  * Must be named `openai/custom`

For OpenAI and Anthropic models, you must provide your API Key for the respective provider.

Your config file should look like this:

```yaml
model_list:
  - model_name: my-gpt-4-turbo
    litellm_params:
      model: gpt-4-1106-preview
      api_key: "OPENAI_API_KEY"  # Replace with your OpenAI API Key
      custom_llm_provider: "openai"

  - model_name: name-this-what-you-want-claude-2.1
    litellm_params:
      model: claude-2.1
      api_key: "CLAUDE_API_KEY"  # Replace with your Anthropic API Key

  # The following is for locally running LLMs. Do not deviate from the following definition
  - model_name: custom 
    litellm_params:
      model: openai/custom
      api_base: "http://host.docker.internal:1234/v1"  # host.docker.internal allows docker to use your local machine's IP address (localhost)
      api_key: "None"
      custom_llm_provider: "openai"
```

Edit the model list to include the models you want to use. You need to specify at least one model to use Rubra.

![Architecture Diagram](/img/llm-config.svg)
<sub>We currently use [LiteLLM](https://docs.litellm.ai/docs/proxy/configs#quick-start) as the chat completions server. This may change in the future.</sub>
