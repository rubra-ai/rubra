---
sidebar_position: 0
title: llama.cpp
---

tools.cpp is Rubra's fork of llama.cpp, offers inference of Rubra's function calling models (and others) in pure C/C++.
This guild will walk you through how to install and setup tools.cpp to serve Rubra's models for inference, along with a simply python function calling example.

### Quickstart
**1. build from source:**
```
# git clone the repo
git clone https://github.com/rubra-ai/tools.cpp.git
cd tools.cpp
```   

- Mac user
```
make
```

- Nvidia-Cuda user:
```
make LLAMA_CUDA=1
```

**2. Install a helper package that fixes some rare edgecases:**
```
npm install jsonrepair
```

**3. Download a compatible Rubra's gguf model:**
For example:
```
wget https://huggingface.co/sanjay920/Llama-3-8b-function-calling-alpha-v1.gguf/resolve/main/Llama-3-8b-function-calling-alpha-v1.gguf
```

**4. Start openai compatible server:**
```
./llama-server -ngl 37 -m Llama-3-8b-function-calling-alpha-v1.gguf   --port 1234 --host 0.0.0.0  -c 8000 --chat-template llama3
```

**5. Test the server, make sure it is available:**
```bash
curl localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer tokenabc-123" \
  -d '{
    "model": "rubra-model",
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

**6. Try a python function calling example:**
```python
# if openai not installed, do `pip install openai`
from openai import OpenAI
client = OpenAI(api_key="123", base_url = "http://localhost:1234/v1/")

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
  model="rubra-model",
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

For more function calling examples, you can checkout `test_llamacpp.ipynb` notebook.
