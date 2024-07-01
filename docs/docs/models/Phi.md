---
sidebar_position: 3
title: Phi 3
---

Phi-3 is a state of the art, lightweight model. It performs exceptionally well despite being half the size of Llama-3 8B. It is highly capable of being an on-device agentic LLM.

:::::note

| Model                  | Params | Context Length | GQA | Token Count | Knowledge Cutoff |
|------------------------|--------|----------------|-----|-------------|------------------|
| Phi-3 Mini 128k Instruct | 3.8B | 128,000        | Yes | 3.3T        | October 2023     |

:::::

## Phi-3 Mini 128k Instruct

- [rubra-ai/Phi-3-mini-128k-instruct](https://huggingface.co/rubra-ai/Phi-3-mini-128k-instruct)
- [rubra-ai/Phi-3-mini-128k-instruct-GGUF](https://huggingface.co/rubra-ai/Phi-3-mini-128k-instruct-GGUF)

<table>
  <thead>
    <tr>
      <th rowspan="2">Model</th>
      <th rowspan="2">Function Calling</th>
      <th rowspan="2">MMLU</th>
      <th rowspan="2">GPQA</th>
      <th rowspan="2">GSM-8K</th>
      <th rowspan="2">MATH</th>
      <th rowspan="2">MT-bench</th>
      <th colspan="6">MT-bench Pairwise Comparison</th>
    </tr>
    <tr>
      <th>Win</th>
      <th>Loss</th>
      <th>Tie</th>
      <th>Win Rate</th>
      <th>Loss Rate</th>
      <th>Adjusted Win Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Phi-3 Mini 128k Instruct</td>
      <td>-</td>
      <td>68.17</td>
      <td>30.58</td>
      <td>80.44</td>
      <td>28.12</td>
      <td>7.92</td>
      <td>51</td>
      <td>45</td>
      <td>64</td>
      <td>0.31875</td>
      <td>0.28125</td>
      <td><strong>0.51875</strong></td>
    </tr>
    <tr>
      <td>Rubra Enhanced Phi-3 Mini 128k Instruct</td>
      <td>65.71%</td>
      <td>66.66</td>
      <td>29.24</td>
      <td>74.09</td>
      <td>26.84</td>
      <td>7.45</td>
      <td>45</td>
      <td>51</td>
      <td>64</td>
      <td>0.28125</td>
      <td>0.31875</td>
      <td>0.48125</td>
    </tr>
  </tbody>
</table>