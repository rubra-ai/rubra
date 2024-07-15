<p align="left">
    中文</a>&nbsp ｜ &nbsp<a href="README.md">English</a>&nbsp</a>
</p>
<br><br>


# Rubra

#### Rubra 是一系列开放权重、聚焦于工具调用的大模型（LLM）。

Rubra 增强了当前最流行的一系列开放权重大模型（LLM）的工具调用能力。以能够在和用户对话时以稳定的方式调用用户定义的外部工具，使 Rubra 大模型非常适用于Agent相关的场景。

所有模型均基于流行的Instruct模型，通过进一步的微调，有效地教授或增强模型调用工具的能力，同时尽可能减少模型在基础能力和知识上的流失。为了便于用户使用，我们扩展了流行的llm本地部署项目，让您可以轻松运行 Rubra 模型。

## Rubra模型系列

| 模型 | 最大上下文长度 | 大小 | 基础模型发布者 |
|---------------------------------------------------------------|----------------|------|----------------------|
| [rubra-ai/Meta-Llama-3-8B-Instruct](https://www.modelscope.cn/models/rubraAI/Meta-Llama-3-8B-Instruct)   | 8,000          | 8B   | Meta             |
| [rubra-ai/Meta-Llama-3-70B-Instruct](https://www.modelscope.cn/models/rubraAI/Meta-Llama-3-70B-Instruct) | 8,000          | 70B  | Meta             |
| [rubra-ai/gemma-1.1-2b-it](https://www.modelscope.cn/models/rubraAI/Gemma-1.1-2b-Instruct)                     | 8,192          | 2B   | Google                 |
| [rubra-ai/Mistral-7B-Instruct-v0.3](https://www.modelscope.cn/models/rubraAI/Mistral-7B-Instruct-v0.3)   | 32,000         | 7B   | Mistral              |
| [rubra-ai/Mistral-7B-Instruct-v0.2](https://www.modelscope.cn/models/rubraAI/Mistral-7B-Instruct-v0.2)   | 32,000         | 7B   | Mistral              |
| [rubra-ai/Phi-3-vision-128k-instruct](https://www.modelscope.cn/models/rubraAI/Phi-3-mini-128k-instruct)| 128,000        | 3B   | Microsoft              |
| [rubra-ai/Qwen2-7B-Instruct](https://www.modelscope.cn/models/rubraAI/Qwen2-7B-Instruct)                 | 131,072        | 7B   | Qwen                   |

## Demo

在我们的 [Huggingface Spaces](https://huggingface.co/spaces/sanjay920/rubra-v0.1-dev) 上可以免费试用以上的大模型，不需要登录！

## 在本地部署运行 Rubra 模型

查看我们的[文档](https://docs.rubra.ai/category/serving--inferencing)以了解如何在本地运行 Rubra 模型。
我们扩展了以下部署工具，支持OpenAI的工具调用格式，在本地运行Rubra模型：

- [llama.cpp](https://github.com/rubra-ai/tools.cpp)
- [vLLM](https://github.com/rubra-ai/vllm)

**注意**: Llama3 模型，包括8B和70B的gguf版本，在量化（quantization）后会出现perplexity增加和函数调用性能下降的问题。我们建议使用 vLLM 或 fp16或更高（bf16， fp32） 量化来部署运行它们。

## 基准测试

查看 Rubra 模型及其他模型的完整基准测试结果： https://docs.rubra.ai/benchmark

| 模型                                                     | 函数调用         | MMLU (5-shot) | GPQA (0-shot) | GSM-8K (8-shot, CoT) | MATH (4-shot, CoT) | MT-bench |
|-----------------------------------------------------------|------------------|---------------|---------------|----------------------|--------------------|----------|
| [**Rubra Llama-3 70B Instruct**](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct)       | 97.85%           | 75.90         | 33.93         | 82.26                | 34.24              | 8.36     |
| [**Rubra Llama-3 8B Instruct**](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct)        | 89.28%           | 64.39         | 31.70         | 68.99                | 23.76              | 8.03     |
| [**Rubra Qwen2 7B Instruct**](https://huggingface.co/rubra-ai/Qwen2-7B-Instruct)                 | 85.71%           | 68.88         | 30.36         | 75.82                | 28.72              | 8.08     |
| [**Rubra Mistral 7B Instruct v0.3**](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.3)   | 73.57%           | 59.12         | 29.91         | 43.29                | 11.14              | 7.69     |
| [**Rubra Phi-3 Mini 128k Instruct**](https://huggingface.co/rubra-ai/Phi-3-mini-128k-instruct)   | 70.00%           | 67.87         | 29.69         | 79.45                | 30.80              | 8.21     |
| [**Rubra Mistral 7B Instruct v0.2**](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.2)   | 69.28%           | 58.90         | 29.91         | 34.12                | 8.36               | 7.36     |
| [**Rubra Gemma-1.1 2B Instruct**](https://huggingface.co/rubra-ai/gemma-1.1-2b-it)               | 45.00%           | 38.85         | 24.55         | 6.14                 | 2.38               | 5.75     |


## 贡献

欢迎您参与对 Rubra 的进一步开发！我们希望根据您的反馈改进模型的工具调用能力。如果您的工具调用不起作用或出错，请创建一个Issue并分享您遇到的问题。

---

## 许可证

版权所有 (c) 2024 Acorn Labs, Inc.

根据 Apache License, Version 2.0（“许可证”）授权；您不得在不符合许可证的情况下使用此文件。您可以在以下网址获取许可证副本：

<http://www.apache.org/licenses/LICENSE-2.0>

除非适用法律要求或书面同意，按“原样”分发的软件不附带任何明示或暗示的保证或条件。请参阅许可证以了解特定语言的管理权限和限制。