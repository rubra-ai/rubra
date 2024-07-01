---
sidebar_position: 0
title: Llama 3
---

Llama 3 is a family of models developed by Meta. They are considered one of the most capable LLMs published till date.

:::::note

| Model               | Params | Context Length | GQA | Token Count | Knowledge Cutoff |
|---------------------|--------|----------------|-----|-------------|------------------|
| Llama-3 8B Instruct | 8B     | 8k             | Yes | 15T+        | March 2023       |
| Llama-3 70B Instruct| 70B    | 8k             | Yes | 15T+        | December 2023    |


:::tip
We recommend this model for complex tool calling scenarios, but users should be aware of the relatively short context length.
:::
:::::




## Llama-3 8B Instruct

- [rubra-ai/Meta-Llama-3-8B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct) 
- [rubra-ai/Meta-Llama-3-8B-Instruct-GGUF](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct-GGUF)

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
      <td>Llama-3 8B Instruct</td>
      <td>-</td>
      <td>65.69</td>
      <td>31.47</td>
      <td>77.41</td>
      <td>27.58</td>
      <td>8.07</td>
      <td>41</td>
      <td>42</td>
      <td>77</td>
      <td>0.25625</td>
      <td>0.2625</td>
      <td>0.496875</td>
    </tr>
    <tr>
      <td>Rubra Enhanced Llama-3 8B Instruct</td>
      <td>89.28%</td>
      <td>64.39</td>
      <td>31.70</td>
      <td>68.99</td>
      <td>23.76</td>
      <td>8.03</td>
      <td>42</td>
      <td>41</td>
      <td>77</td>
      <td>0.2625</td>
      <td>0.25625</td>
      <td><strong>0.503125</strong></td>
    </tr>
  </tbody>
</table>


## Llama-3 70B Instruct

- [rubra-ai/Meta-Llama-3-70B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct)
- [rubra-ai/Meta-Llama-3-70B-Instruct-GGUF](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct-GGUF)

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
      <td>Llama-3 70B Instruct</td>
      <td>-</td>
      <td>79.90</td>
      <td>38.17</td>
      <td>90.67</td>
      <td>44.24</td>
      <td>8.88</td>
      <td>58</td>
      <td>28</td>
      <td>74</td>
      <td>0.3625</td>
      <td>0.1750</td>
      <td><strong>0.59375</strong></td>
    </tr>
    <tr>
      <td>Rubra Enhanced Llama-3 70B Instruct</td>
      <td>97.85%</td>
      <td>75.90</td>
      <td>33.93</td>
      <td>82.26</td>
      <td>34.24</td>
      <td>8.36</td>
      <td>28</td>
      <td>58</td>
      <td>74</td>
      <td>0.1750</td>
      <td>0.3625</td>
      <td>0.40625</td>
    </tr>
  </tbody>
</table>