# Deploy Local Model Utility

This utility provides a convenient way to serve chat completion requests locally, without the need to install LM Studio or figure out how to start [`llama.cpp`](https://github.com/ggerganov/llama.cpp) yourself. We recommend using this model: [OpenHermes-2.5-neural-chat-v3-3-Slerp](https://huggingface.co/Weyaxi/OpenHermes-2.5-neural-chat-v3-3-Slerp). We download a quantized version by default, but you can change this in [serve.sh](./serve.sh#L55).

## Getting Started

### Prerequisites

- Python 3.9 or higher

You can run a local LLM a couple different ways. The goal is to have an OpenAI chat completions endpoint running on http://localhost:1234. We provide options that will do this for you. If you want to run it manually, you can follow the steps below.

### Installation

If you are a mac user on an Apple Silicon M-series, we suggest leveraging the iGPU. This will significantly speed up inference and we automatically do this for you in [serve.sh](./serve.sh#L55). If you are on an Intel device, you can remove the `--use_igpu` flag in the shell script. Run:


```sh
sh serve.sh
```

### Docker

You can serve the model using Docker. If you'd like to run just the model you can:
  
  1. Download the quantized LLM:
    ```sh
    wget https://huggingface.co/TheBloke/OpenHermes-2.5-neural-chat-v3-3-Slerp-GGUF/resolve/main/openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf
    ```
  2. Run the docker container using docker-compose:
    ```sh
    docker-compose up
    ```

You can set the `api_base` of your custom model in [llm-config.yaml](../llm-config.yaml#L10) to `"http://llama_cpp_python:1234/v1"`


## Alternatives

You may be more familiar or comfortable with a differnt tool to run a local LLM. To create Rubra assistants powered by locally running LLMs, you must use llama.cpp with the [grammar provided in this repo](./grammar/json_grammar.gbnf).

### llama.cpp

llama cpp has a variety of build options to leverage your hardware. Refer to this [section](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#usage) for more information.


### LM Studio

Download [here](https://lmstudio.ai/) and run local server to enable a chat completions endpoint.

This is not recommended if you'd like to create Rubra assistants that leverage locally running models as Rubra uses a specific grammar to better structure local LLM output




## Quantized Models

[serve.sh](./serve.sh#L55) downloads the 6 bit K quantized version by default. Depending on your memory constraints, you may want to download a smaller quanitzed model. You can view the [models](https://huggingface.co/TheBloke/OpenHermes-2.5-neural-chat-v3-3-Slerp-GGUF) here or refer to the table below.

| Quantization Name | Size |
| --- | --- |
| openhermes-2.5-neural-chat-v3-3-slerp.Q2_K.gguf | 3.08 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q3_K_L.gguf | 3.82 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q3_K_M.gguf | 3.52 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q3_K_S.gguf | 3.16 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q4_0.gguf | 4.11 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q4_K_M.gguf | 4.37 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q4_K_S.gguf | 4.14 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q5_0.gguf | 5 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q5_K_M.gguf | 5.13 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q5_K_S.gguf | 5 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q6_K.gguf | 5.94 GB |
| openhermes-2.5-neural-chat-v3-3-slerp.Q8_0.gguf | 7.7 GB |

## Testing

We've tested this on:
- Apple M2 Max
- Apple M1 Pro

Open up an issue if your platform is not supported and you'd like us to automate the process for you.
