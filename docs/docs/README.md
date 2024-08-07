---
sidebar_position: 0
title: What is Rubra?
---

# Rubra

#### Rubra is a collection of open-weight, tool-calling LLMs.

Rubra enhances the top open-weight large language models with tool-calling capability. The ability to call user-defined external tools in a deterministic manner while reasoning and chatting makes Rubra models ideal for agentic use cases.

All models are enhanced from the top open-source LLMs with further post-training and methods that effectively teach instruct-tuned models new skills while mitigating catastrophic forgetting. For easy use, we extend popular inferencing projects, allowing you to run Rubra models easily.

## Enhanced Models

| Enhanced Model                                                        | Context Length | Size  | GGUF Quants |
|-----------------------------------------------------------------------|----------------|-------|-------------|
| [rubra-ai/Meta-Llama-3-8B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct)             | 8,000          | 8B    | [rubra-ai/Meta-Llama-3-8B-Instruct-GGUF](https://huggingface.co/rubra-ai/Meta-Llama-3-8B-Instruct-GGUF)     |
| [rubra-ai/Meta-Llama-3-70B-Instruct](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct)           | 8,000          | 70B   | [rubra-ai/Meta-Llama-3-70B-Instruct-GGUF](https://huggingface.co/rubra-ai/Meta-Llama-3-70B-Instruct-GGUF)   |
| [rubra-ai/gemma-1.1-2b-it](https://huggingface.co/rubra-ai/gemma-1.1-2b-it)                               | 8,192          | 2B    | [rubra-ai/gemma-1.1-2b-it-GGUF](https://huggingface.co/rubra-ai/gemma-1.1-2b-it-GGUF)                         |
| [rubra-ai/Mistral-7B-Instruct-v0.3](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.3)             | 32,000         | 7B    | [rubra-ai/Mistral-7B-Instruct-v0.3-GGUF](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.3-GGUF)       |
| [rubra-ai/Mistral-7B-Instruct-v0.2](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.2)             | 32,000         | 7B    | [rubra-ai/Mistral-7B-Instruct-v0.2-GGUF](https://huggingface.co/rubra-ai/Mistral-7B-Instruct-v0.2-GGUF)       |
| [rubra-ai/Phi-3-mini-128k-instruct](https://huggingface.co/rubra-ai/Phi-3-mini-128k-instruct)             | 128,000        | 3B    | [rubra-ai/Phi-3-mini-128k-instruct-GGUF](https://huggingface.co/rubra-ai/Phi-3-mini-128k-instruct-GGUF)       |
| [rubra-ai/Qwen2-7B-Instruct](https://huggingface.co/rubra-ai/Qwen2-7B-Instruct)                           | 131,072        | 7B    | [rubra-ai/Qwen2-7B-Instruct-GGUF](https://huggingface.co/rubra-ai/Qwen2-7B-Instruct-GGUF)                     |

## Demo

Try out the models immediately without downloading anything in [Huggingface Spaces](https://huggingface.co/spaces/sanjay920/rubra-v0.1-function-calling)! It's free and requires no login.

<!-- <iframe 
  src="https://gokaygokay-florence-2.hf.space"
  frameborder="0"
  style={{ width: '120%', height: '1200px' }}
  allowfullscreen
></iframe> -->

## Run Rubra Models Locally

We extend the following inferencing tools to run Rubra models in an OpenAI-compatible tool-calling format for local use:

- [llama.cpp](https://github.com/rubra-ai/tools.cpp)
- [vLLM](https://github.com/rubra-ai/vllm)

**Note**: Llama3 models, including the 8B and 70B variants, are known to experience increased perplexity and a subsequent degradation in function-calling performance as a result of quantization. We recommend serving them with either vLLM or using the fp16 quantization.

## Contributing

Contributions to Rubra are welcome! We'd love to improve tool-calling capability in the models based on your feedback. Please submit issues to the GitHub repository.

## License

Rubra code is licensed under the Apache 2.0 License. Rubra enhanced models are published under the same license as the parent model.

---

For more details and documentation, visit the [Rubra GitHub page](https://github.com/rubra-ai/rubra).
