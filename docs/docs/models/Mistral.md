---
sidebar_position: 2
title: Mistral
---

Mistral is a series of open weight models that set the bar for efficiency, and are available for free under Apache 2.0 that allows use of the models anywhere without any restriction. The Mistral-7b-instruct-v0.3 model offers 32k context length, making it an ideal LLM for scenarios that require longer context.

| Model               | Params | Context Length | GQA | Token Count | Knowledge Cutoff |
|---------------------|--------|----------------|-----|-------------|------------------|
| Mistral 7B Instruct v0.3 | 7B     | 32k             | Yes | Undisclosed        | Undisclosed (~February 2023)       |

## Mistral 7B Instruct v3

| Model                                     | MT-bench | MMLU | GPQA | GSM-8K | MATH | Function Calling Basics | Function Calling Advanced |
|-------------------------------------------|----------|------|------|--------|------|-------------------------|---------------------------|
| Mistral 7B Instruct v0.3                  | 7.50     | 62.10| 30.58| 53.07  | 12.98|                         |                           |
| Rubra Enhanced Mistral 7B Instruct v0.3   | 7.69     | 59.12| 29.91| 43.29  | 11.14|                         |                           |


#### MT-bench Pairwise Comparison:

| Model                                    | Win | Loss | Tie | Win Rate | Loss Rate | Win Rate Adjusted |
|------------------------------------------|-----|------|-----|----------|-----------|-------------------|
| Mistral 7B Instruct v0.3                 |  34 |   54 |  72 | 0.2125   | 0.3375    | 0.4375            |
| Rubra Enhanced Mistral 7B Instruct v0.3  |  54 |   34 |  72 | 0.3375   | 0.2125    | **0.5625**        |


## Mistral 7B Instruct v2

#### MT-bench Pairwise Comparison:

| Model                                         | Win | Loss | Tie | Win Rate | Loss Rate | Win Rate Adjusted |
|-----------------------------------------------|-----|------|-----|----------|-----------|-------------------|
| Mistral 7B Instruct v0.2                      |  34 |   54 |  72 | 0.2125   | 0.3375    | 0.4375            |
| Rubra Enhanced Mistral 7B Instruct v0.2       |  59 |   43 |  58 | 0.36875  | 0.26875   | **0.55**          |