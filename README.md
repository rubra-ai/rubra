<p align="left">
    <a href="README_CN.md">中文</a>&nbsp ｜ &nbspEnglish&nbsp </a>
</p>
<br><br>

# Rubra

#### Rubra is a collection of open-weight, tool-calling LLMs.

Rubra enhances the top open-weight large language models with tool-calling capability. The ability to call user-defined external tools in a deterministic manner while reasoning and chatting makes Rubra models ideal for agentic use cases.

All models are enhanced from the top open-source LLMs with further post-training and methods that effectively teach instruct-tuned models new skills while mitigating catastrophic forgetting. For easy use, we extend popular inferencing projects, allowing you to run Rubra models easily.

## Enhanced Models

| Enhanced Model                                                        | Context Length | Size | Parent Model Publisher |
|-----------------------------------------------------------------------|----------------|------|------------------------|
| [rubra-ai/Meta-Llama-3-8B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct)   | 8,000          | 8B   | Meta             |
| [rubra-ai/Meta-Llama-3-70B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct) | 8,000          | 70B  | Meta             |
| [rubra-ai/gemma-1.1-2b-it](https://huggingface.co/rubra-ai/gemma-1.1-2b-it)                     | 8,192          | 2B   | Google                 |
| [rubra-ai/Mistral-7B-Instruct-v0.3](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.3)   | 32,000         | 7B   | Mistral              |
| [rubra-ai/Mistral-7B-Instruct-v0.2](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.2)    | 32,000         | 7B   | Mistral              |
| [rubra-ai/Phi-3-vision-128k-instruct](https://huggingface.co/rubra-ai/Phi-3-vision-128k-instruct)| 128,000        | 3B   | Microsoft              |
| [rubra-ai/Qwen2-7B-Instruct](https://huggingface.co/rubra-ai/Qwen2-7B-Instruct)                 | 131,072        | 7B   | Qwen                   |

## Demo

Try out the models immediately without downloading anything in Our [Huggingface Spaces]([https://huggingface.co/spaces/sanjay920/rubra-v0.1-dev](https://huggingface.co/spaces/sanjay920/rubra-v0.1-function-calling))! It's free and requires no login.

For more examples, please check out the `demo` directory.

## Run Rubra Models Locally

Check out our [documentation](https://docs.rubra.ai/category/serving--inferencing) to learn how to run Rubra models locally.
We extend the following inferencing tools to run Rubra models in an OpenAI-compatible tool-calling format for local use:

- [llama.cpp](https://github.com/rubra-ai/tools.cpp)
- [vLLM](https://github.com/rubra-ai/vllm)

**Note**: Llama3 models, including the 8B and 70B variants, are known to experience increased perplexity and a subsequent degradation in function-calling performance as a result of quantization. We recommend serving them with either vLLM or using the fp16 quantization.

## Benchmark

View full benchmark results for Rubra models and other models here: https://docs.rubra.ai/benchmark

| Model                                                     | Function Calling | MMLU (5-shot) | GPQA (0-shot) | GSM-8K (8-shot, CoT) | MATH (4-shot, CoT) | MT-bench |
|-----------------------------------------------------------|------------------|---------------|---------------|----------------------|--------------------|----------|
| [**Rubra Llama-3 70B Instruct**](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct)       | 97.85%           | 75.90         | 33.93         | 82.26                | 34.24              | 8.36     |
| [**Rubra Llama-3 8B Instruct**](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct)        | 89.28%           | 64.39         | 31.70         | 68.99                | 23.76              | 8.03     |
| [**Rubra Qwen2 7B Instruct**](https://huggingface.co/rubra-ai/Qwen2-7B-Instruct)                 | 85.71%           | 68.88         | 30.36         | 75.82                | 28.72              | 8.08     |
| [**Rubra Mistral 7B Instruct v0.3**](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.3)   | 73.57%           | 59.12         | 29.91         | 43.29                | 11.14              | 7.69     |
| [**Rubra Phi-3 Mini 128k Instruct**](https://huggingface.co/rubra-ai/Phi-3-mini-128k-instruct)   | 70.00%           | 67.87         | 29.69         | 79.45                | 30.80              | 8.21     |
| [**Rubra Mistral 7B Instruct v0.2**](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.2)   | 69.28%           | 58.90         | 29.91         | 34.12                | 8.36               | 7.36     |
| [**Rubra Gemma-1.1 2B Instruct**](https://huggingface.co/rubra-ai/gemma-1.1-2b-it)               | 45.00%           | 38.85         | 24.55         | 6.14                 | 2.38               | 5.75     |

## Contributing

Contributions to Rubra are welcome! We'd love to improve tool-calling capability in the models based on your feedback. Please open an issue if your tool doesn't work.

---

## License

Copyright (c) 2024 Acorn Labs, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
