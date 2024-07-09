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
      <td>69.36</td>
      <td>27.01</td>
      <td>83.7</td>
      <td>32.92</td>
      <td>8.02</td>
      <td>21</td>
      <td>72</td>
      <td>67</td>
      <td>0.13125</td>
      <td>0.45000</td>
      <td>0.340625</td>
    </tr>
    <tr>
      <td>Rubra Enhanced Phi-3 Mini 128k Instruct</td>
      <td>70.0%</td>
      <td>67.87</td>
      <td>29.69</td>
      <td>79.45</td>
      <td>30.80 </td>
      <td>8.21</td>
      <td>72</td>
      <td>21</td>
      <td>67</td>
      <td>0.45000</td>
      <td>0.13125</td>
      <td><strong>0.659375</strong></td>
    </tr>
  </tbody>
</table>

* The above is based on the Phi-3 Mini that was updated by Microsoft in June 2024. The original Phi-3 mini came out in April and the Rubra enhanced model has been trained on both versions