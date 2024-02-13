---
id: rubra-frontend-settings
title: Rubra Settings
sidebar_label: Settings
sidebar_position: 2
---

## Configured Models

The following information is available for each configured model:

- Model ID
- LLM Base API (if available)
- Max Tokens
- Input Cost per Token
- Output Cost per Token

The model with the name `custom` is always the locally running model.

## API Key Management

API keys for OpenAI and Anthropic can be managed in this section. You can add, remove, or update the keys as needed.

## Add a New Model

Once the API keys are configured, you can add a new model. The following information is required:

- Model Provider
- Model
- API Key (if required by the provider)
- API Base (if required by the provider)

The available models from each provider are listed in the table below:

| Provider | Models |
| -------- | ------ |
| OpenAI   | `gpt-4-0125-preview`, `gpt-4-1106-preview`, `gpt-4`, `gpt-4-32k`, `gpt-3.5-turbo`, `gpt-3.5-turbo-16k` |
| Anthropic | `claude-2.1` |
| Local | `custom` |