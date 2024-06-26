---
sidebar_position: 0
title: What is Rubra?
---


# Rubra

#### Rubra is a series of open source, agentic LLMs.

Rubra offers the best open-source, function/tool calling models. All models are enhanced from the top open source LLMs by further training after block expansion - a unique approach that is effective in teaching instruct-tuned models new skills while mitigating catastrophic forgetting. For easy use, we extend popular inferencing projects, allowing you to run Rubra models anywhere.

## Enhanced Models

| Enhanced Model                                                        | Context Length | Size | Parent Model Publisher |
|-----------------------------------------------------------------------|----------------|------|------------------------|
| [rubra-ai/Meta-Llama-3-8B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct)   | 8,000          | 8B   | Meta             |
| [rubra-ai/Meta-Llama-3-70B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct) | 8,000          | 70B  | Meta             |
| [rubra-ai/gemma-1.1-2b-it](https://huggingface.co/rubra-ai/gemma-1.1-2b-it)                     | 8,192          | 2B   | Google                 |
| [rubra-ai/Mistral-7B-Instruct-v0.3](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.3)   | 32,000         | 7B   | Mistral              |
| [rubra-ai/Phi-3-vision-128k-instruct](https://huggingface.co/rubra-ai/Phi-3-vision-128k-instruct)| 128,000        | 3B   | Microsoft              |
| [rubra-ai/Qwen2-7B-Instruct](https://huggingface.co/rubra-ai/Qwen2-7B-Instruct)                 | 131,072        | 7B   | Qwen                   |

## Run Rubra Models Locally

We extend the following inferencing tools to run Rubra models in an OpenAI-compatible tool calling format:

- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [vllm](https://github.com/vllm-project/vllm)


## Getting Started

TODO:

```
LLAMAFILE EXAMPLE
```

## Contributing

Contributions to Rubra are welcome! We'd love to improve tool calling capability in the models based on your feedback. Please submit issues or pull requests to the GitHub repository.

## License

Rubra code is licensed under the Apache 2.0 License. Rubra enhanced models are published under the same license as the base model. 

---

For more details and documentation, visit the [Rubra GitHub page](https://github.com/your-repo/rubra).