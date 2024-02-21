---
id: uninstall
title: Uninstall
sidebar_label: Delete Data & Uninstall
sidebar_position: 4
---

## Uninstall Rubra

This removes all Rubra data and configuration from your system.

```bash
curl -sfL https://get.rubra.ai | sh -s -- uninstall
```

## Delete Data only

This removes all Rubra data from your system, including Assistants, Threads, Messages, and Files. The local LLM is not deleted.

```bash
curl -sfL https://get.rubra.ai | sh -s -- delete
```