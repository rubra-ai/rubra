---
sidebar_position: 0
title: What is Rubra?
---


# Rubra

Rubra is a series of popular open source LLMs that are enhanced with function (tool) calling capabilities.

## Models

| Base Model                                                            | Context Length | Size | Enhanced Model |
|-----------------------------------------------------------------------|----------------|------|----------------|
| [meta-llama/Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct) | 8,000          | 8B   | todo           |
| [google/gemma-1.1-2b-it](https://huggingface.co/google/gemma-1.1-2b-it)                       | 8,192          | 2B   | todo           |
| [mistralai/Mistral-7B-Instruct-v0.3](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3) | 32,000         | 7B   | todo           |
| [microsoft/Phi-3-vision-128k-instruct](https://huggingface.co/microsoft/Phi-3-vision-128k-instruct) | 128,000        | 3B   | todo           |
| [Qwen/Qwen2-7B-Instruct](Qwen2-7B-Instruct)                                                      | 131,072        | 7B   | todo           |

## Run Rubra Models Locally

We extend the following inferencing tools to run Rubra models in an OpenAI-compatible tool calling format:

- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [vllm](https://github.com/vllm-project/vllm)
- [llamafile](https://github.com/Mozilla-Ocho/llamafile)


## Getting Started

TODO:

```
LLAMAFILE EXAMPLE
```

## Contributing

Contributions to Rubra are welcome! We'd love to improve tool calling capability in the models based on your feedback. Please submit issues or pull requests to the GitHub repository.

## License

Rubra python code is licensed under the MIT License. Rubra enhanced models are published under the same license as the base model. 

---

For more details and documentation, visit the [Rubra GitHub page](https://github.com/your-repo/rubra).