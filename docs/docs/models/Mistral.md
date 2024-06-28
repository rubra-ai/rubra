---
sidebar_position: 2
title: Mistral
---

Mistral is a series of open weight models that set the bar for efficiency, and are available for free under Apache 2.0 that allows use of the models anywhere without any restriction. The Mistral-7b-instruct-v0.3 model offers 32k context length, making it an ideal LLM for scenarios that require longer context.

:::::note

| Model                    | Params | Context Length | GQA | Token Count  | Knowledge Cutoff          |
|--------------------------|--------|----------------|-----|--------------|---------------------------|
| Mistral 7B Instruct v0.3 | 7B     | 32k            | Yes | Undisclosed  | ~February 2023           |
| Mistral 7B Instruct v0.2 | 7B     | 32k            | Yes | Undisclosed  | ~February 2023           |

:::::

## Mistral 7B Instruct v3

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
      <td>Mistral 7B Instruct v0.3</td>
      <td>-</td>
      <td>62.10</td>
      <td>30.58</td>
      <td>53.07</td>
      <td>12.98</td>
      <td>7.50</td>
      <td>34</td>
      <td>54</td>
      <td>72</td>
      <td>0.2125</td>
      <td>0.3375</td>
      <td>0.4375</td>
    </tr>
    <tr>
      <td>Rubra Enhanced Mistral 7B Instruct v0.3</td>
      <td>73.57%</td>
      <td>59.12</td>
      <td>29.91</td>
      <td>43.29</td>
      <td>11.14</td>
      <td>7.69</td>
      <td>54</td>
      <td>34</td>
      <td>72</td>
      <td>0.3375</td>
      <td>0.2125</td>
      <td><strong>0.5625</strong></td>
    </tr>
  </tbody>
</table>


## Mistral 7B Instruct v2

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
      <td>Mistral 7B Instruct v0.2</td>
      <td>-</td>
      <td>59.27</td>
      <td>27.68</td>
      <td>43.21</td>
      <td>10.30</td>
      <td>7.50</td>
      <td>34</td>
      <td>54</td>
      <td>72</td>
      <td>0.2125</td>
      <td>0.3375</td>
      <td>0.4375</td>
    </tr>
    <tr>
      <td>Rubra Enhanced Mistral 7B Instruct v0.2</td>
      <td>69.28%</td>
      <td>58.90</td>
      <td>29.91</td>
      <td>34.12</td>
      <td>8.36</td>
      <td>7.36</td>
      <td>59</td>
      <td>43</td>
      <td>58</td>
      <td>0.36875</td>
      <td>0.26875</td>
      <td><strong>0.55</strong></td>
    </tr>
  </tbody>
</table>
