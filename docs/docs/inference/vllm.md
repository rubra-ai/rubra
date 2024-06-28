---
sidebar_position: 2
title: vLLM
---

vLLM is a fast and easy-to-use library for LLM inference and serving.
Rubra offers a customized version of vllm to support Rubra's models inference and serving.
- vLLM supports NVIDIA GPUs, AMD GPUs, Intel CPUs and GPUs. It's recommended to use vLLM with at least one GPU.

This guild will walk you through how to install and setup vLLM to serve Rubra's models for inference, along with a simply python function calling example.

## Quickstart
**1. Install**
```
# git clone the rubra-vllm repo:
git clone https://github.com/rubra-ai/vllm.git
cd vllm
```

```
# export cuda path
export CUDA_HOME=/usr/local/cuda
export PATH="${CUDA_HOME}/bin:$PATH"

# install from source
pip install -e . # this can take 5-10 minutes
# install a helper package using npm, this handles some rare edgecases parsing function calls.
npm install jsonrepair
```

**2. Start the Server with a Rubra function calling model:**
```
python -m vllm.entrypoints.openai.api_server --model sanjay920/Phi-3-mini-128k-instruct-function-calling-alpha-v1  --dtype auto --api-key token-abc123 --max-model-len 8000 --gpu-memory-utilization 0.96 --enforce-eager
```
The model will get downloaded automatically from huggingface.

**3. Test the server, make sure it is available:**
```bash
curl localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer token-abc123" \
  -d '{
    "model": "sanjay920/Phi-3-mini-128k-instruct-function-calling-alpha-v1",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": "hello"
      }
    ]
  }'
```

**4. Try a python function calling example:**
```python
# if openai not installed, do `pip install openai`
from openai import OpenAI
client = OpenAI(api_key="token-abc123", base_url = "http://localhost:8000/v1/")

tools = [
  {
    "type": "function",
    "function": {
      "name": "get_current_weather",
      "description": "Get the current weather in a given location",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {
            "type": "string",
            "description": "The city and state, e.g. San Francisco, CA",
          },
          "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
      },
    }
  }
]
messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
completion = client.chat.completions.create(
  model="sanjay920/Phi-3-mini-128k-instruct-function-calling-alpha-v1",
  messages=messages,
  tools=tools,
  tool_choice="auto"
)

print(completion)
```

The output should look like this:
```
ChatCompletion(id='chatcmpl-EmHd8kai4DVwBUOyim054GmfcyUbjiLf', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='e885974b', function=Function(arguments='{"location":"Boston"}', name='get_current_weather'), type='function')]))], created=1719528056, model='rubra-model', object='chat.completion', system_fingerprint=None, usage=CompletionUsage(completion_tokens=29, prompt_tokens=241, total_tokens=270))
```

That's it! MAKE SURE you turn `stream` OFF when making api calls to the server, as the streaming feature is not supported yet. And we will support streaming too soon.
