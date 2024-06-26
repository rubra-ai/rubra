---
sidebar_position: 0
title: Llama 3
---

Llama 3 is a family of models developed by Meta. They are considered one of the most capable LLMs published till date.

We recommend this model for complex tool calling scenarios, but users should be aware of the relatively short context length.

| Model               | Params | Context Length | GQA | Token Count | Knowledge Cutoff |
|---------------------|--------|----------------|-----|-------------|------------------|
| Llama-3 8B Instruct | 8B     | 8k             | Yes | 15T+        | March 2023       |
| Llama-3 70B Instruct| 70B    | 8k             | Yes | 15T+        | December 2023    |


## Llama-3 8B Instruct

| Model                              | MT-bench |  MMLU |  GPQA | GSM-8K | MATH  | Function Calling Basics | Function Calling Advanced
|------------------------------------|----------|-------|-------|--------|-------|-------------------------|--------------------------|
| Llama-3 8B Instruct                |   8.07   | 65.69 | 31.47 | 77.41  | 27.58 |                         |                          |
| Rubra Enhanced Llama-3 8B Instruct |   8.03   | 64.39 | 31.70 | 68.99  | 23.76 |                         |                          |

#### MT-bench Pairwise Comparison:
| Model                               | Win | Loss | Tie | Win Rate | Loss Rate | Win Rate Adjusted |
|-------------------------------------|-----|------|-----|----------|-----------|-------------------|
| Meta-Llama-3-8B-Instruct            |  41 |   42 |  77 | 0.25625  | 0.26250   | 0.496875          |
| Rubra Enhanced Llama-3 8B Instruct  |  42 |   41 |  77 | 0.26250  | 0.25625   | **0.503125**      |

* The Rubra enhanced model beats the base instruct model in a head to head comparison - demonstrating negligible regression in core capabilities from the parent model given other benchmark results.


## Llama-3 70B Instruct