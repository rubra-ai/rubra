---
sidebar_position: 4
title: Qwen 2
---

Qwen2 is a series of state of the art, multi-lingual LLMs that range  from 0.5 to 72 billion parameters. It excels in a variety of tasks. The only variant offered by Rubra at the moment is the 7B one.

:::::note

| Model               | Params | Context Length | GQA | Token Count | Knowledge Cutoff |
|---------------------|--------|----------------|-----|-------------|------------------|
| Qwen2 7B Instruct   | 7.6B   | 131,072        | Yes | 3T          | 2023             |

:::tip
The Rubra enhanced Qwen2-7b-Instruct model is capable of doing tool/function calling in Chinese! 

We recommend this model for any task exceeding the context limit found in Llama-3 models.

:::


:::::

## Qwen2 7B Instruct


#### MT-bench Pairwise Comparison:

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
      <td>Qwen2-7B-Instruct</td>
      <td>-</td>
      <td>70.78</td>
      <td>32.14</td>
      <td>78.54</td>
      <td>30.10</td>
      <td>8.29</td>
      <td>49</td>
      <td>33</td>
      <td>78</td>
      <td>0.30625</td>
      <td>0.20625</td>
      <td><strong>0.55</strong></td>
    </tr>
    <tr>
      <td>Rubra Enhanced Qwen2-7B-Instruct</td>
      <td>85.71%</td>
      <td>68.88</td>
      <td>30.36</td>
      <td>75.82</td>
      <td>28.72</td>
      <td>8.08</td>
      <td>33</td>
      <td>49</td>
      <td>78</td>
      <td>0.20625</td>
      <td>0.30625</td>
      <td>0.45</td>
    </tr>
  </tbody>
</table>