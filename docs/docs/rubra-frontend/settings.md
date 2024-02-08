---
id: rubra-frontend-settings
title: Rubra Settings
sidebar_label: Settings
sidebar_position: 2
---

## Configured Models

### Proprietary Models

For proprietary models, the following information is available:

- Max Tokens
- Input Cost per Token
- Output Cost per Token

### Locally Running Models

For locally running models, the base API is provided so that the user knows where the model inference server is running.

## Features in Development

* Ability to add models in this settings page
  * Currently, users must edit the `llm-config.yaml` file to add models. The user that sets up the back end must set the `editable` flag to true to allow users to add/remove models in the UI.