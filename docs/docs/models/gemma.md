---
sidebar_position: 1
title: Gemma
---

Gemma is a family of lightweight models developed by Google. Rubra offers the 2B variant with function calling, which is most appropriate for single instruction chats. 

Note: We observe in the benchmarks and in our own testing that Gemma models do not perform well when the number of turns (chat messages) increases.

| Model               | Params | Context Length | GQA | Token Count | Knowledge Cutoff |
|---------------------|--------|----------------|-----|-------------|------------------|
| Gemma-1.1 2B Instruct | 2B     | 8192             | No (MQA) | 6T        | Undisclosed

## Gemma-1.1 2B Instruct

| Model                                | MT-bench | MMLU |  GPQA | GSM-8K | MATH | Function Calling Basics | Function Calling Advanced |
|--------------------------------------|----------|------|-------|--------|------|-------------------------|---------------------------|
| Gemma-1.1 2B Instruct                | 5.82     |      | 22.99 | 6.29   | 6.14 |                         |                           |
| Rubra Enhanced Gemma-1.1 2B Instruct | 5.75     |      | 24.55 | 6.14   | 2.38 |                         |                           |

#### MT-bench Pairwise Comparison:

| Model                                      | Win | Loss | Tie | Win Rate | Loss Rate | Win Rate Adjusted |
|--------------------------------------------|-----|------|-----|----------|-----------|-------------------|
| Gemma-1.1 2B Instruct                      |  33 |   56 |  71 | 0.20625  | 0.35000   | 0.428125          |
| Rubra Enhanced Gemma-1.1 2B Instruct       |  56 |   33 |  71 | 0.35000  | 0.20625   | **0.571875**      |