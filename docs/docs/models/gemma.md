---
sidebar_position: 1
title: Gemma
---

Gemma is a family of lightweight models developed by Google. Rubra offers the 2B variant with function calling, which is most appropriate for single instruction chats. 

:::::note
| Model               | Params | Context Length | GQA | Token Count | Knowledge Cutoff |
|---------------------|--------|----------------|-----|-------------|------------------|
| Gemma-1.1 2B Instruct | 2B     | 8192             | No (MQA) | 6T        | Undisclosed
:::tip
We observe in the benchmarks and in our own testing that Gemma models do not perform well when the number of turns (chat messages) increases.
:::
:::::



## Gemma-1.1 2B Instruct

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
      <td>Gemma-1.1 2B Instruct</td>
      <td>-</td>
      <td>37.84</td>
      <td>22.99</td>
      <td>6.29</td>
      <td>6.14</td>
      <td>5.82</td>
      <td>33</td>
      <td>56</td>
      <td>71</td>
      <td>0.20625</td>
      <td>0.35000</td>
      <td>0.428125</td>
    </tr>
    <tr>
      <td>Rubra Enhanced Gemma-1.1 2B Instruct</td>
      <td>45.00%</td>
      <td>38.85</td>
      <td>24.55</td>
      <td>6.14</td>
      <td>2.38</td>
      <td>5.75</td>
      <td>56</td>
      <td>33</td>
      <td>71</td>
      <td>0.35000</td>
      <td>0.20625</td>
      <td><strong>0.571875</strong></td>
    </tr>
  </tbody>
</table>