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
| [rubra-ai/Phi-3-vision-128k-instruct](https://huggingface.co/rubra-ai/Phi-3-vision-128k-instruct)| 128,000        | 3B   | Microsoft              |
| [rubra-ai/Qwen2-7B-Instruct](https://huggingface.co/rubra-ai/Qwen2-7B-Instruct)                 | 131,072        | 7B   | Qwen                   |

## Demo

Try out the models immediately without downloading anything in Our [Huggingface Spaces](https://huggingface.co/spaces/sanjay920/rubra-v0.1-dev)! It's free and requires no login.

## Run Rubra Models Locally

We extend the following inferencing tools to run Rubra models in an OpenAI-compatible tool-calling format for local use:

- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [vllm](https://github.com/vllm-project/vllm)

## Contributing

Contributions to Rubra are welcome! We'd love to improve tool-calling capability in the models based on your feedback. Please open an issue if your tool doesn't work.

---

## License

Copyright (c) 2024 Acorn Labs, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
