---
sidebar_position: 3
title: HuggingFace Transformers
---

Hugging Face's [transformers](https://huggingface.co/docs/transformers/index) is an open-source library designed to facilitate the use of natural language processing (NLP) models.
You can directly run Rubra's LLMs using the `transformers` library with the support of Rubra's inferencing tool package, [rubra_tools](https://github.com/rubra-ai/rubra-tools/tree/main). This guide will walk you through the steps to seamlessly integrate and utilize Rubra's models with the `transformers` library.


## Prerequisites
:::info 
Before you move forward, it's recommended to use a GPU, which can significantly speed up the inference processes.
:::

*pip install rubra-tools, torch, transformers:*
```
pip install rubra_tools torch==2.3.0 transformers accelerate
```

*Use npm to install package `jsonrepair` to help fix some rare edgecases.*
```
npm install jsonrepair
```

## Quickstart

### 1. load a rubra function calling model:
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from rubra_tools import preprocess_input, postprocess_output

model_id = "rubra-ai/Meta-Llama-3-8B-Instruct"

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
```

### 2. Define functions

Here we use 4 functions for a simple math chaining question.
```python
functions = [
    {
            'type': 'function',
            'function': {
                'name': 'addition',
                'description': "Adds two numbers together",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to add',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Second number to add',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'subtraction',
                'description': "Subtracts two numbers",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to be subtracted from',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Number to subtract',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'multiplication',
                'description': "Multiply two numbers together",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to multiply',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Second number to multiply',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
        {
            'type': 'function',
            'function': {
                'name': 'division',
                'description': "Divide two numbers",
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'a': {
                            'description': 'First number to use as the dividend',
                            'type': 'string'
                        },
                        'b': {
                            'description': 'Second number to use as the divisor',
                            'type': 'string'
                        }
                    },
                    'required': []
                }
            }
        },
]
```

### 3. Start the Conversation with a Simple Math Chaining Question:
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the result of four plus six? Take the result and add 2? Then multiply by 5 and then divide by two"},
]

def run_model(messages, functions):
    ## Format messages in Rubra's format
    formatted_msgs = preprocess_input(msgs=messages, tools=functions)

    input_ids = tokenizer.apply_chat_template(
        formatted_msgs,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    terminators = [
        tokenizer.eos_token_id,
        tokenizer.convert_tokens_to_ids("<|eot_id|>")
    ]

    outputs = model.generate(
        input_ids,
        max_new_tokens=1000,
        eos_token_id=terminators,
        do_sample=True,
        temperature=0.1,
        top_p=0.9,
    )
    response = outputs[0][input_ids.shape[-1]:]
    raw_output = tokenizer.decode(response, skip_special_tokens=True)
    return raw_output

raw_output = run_model(messages, functions)
# Check if there's a function call
function_call = postprocess_output(raw_output)
if function_call:
    print(function_call)
else:
    print(raw_output)
```

You should see this output, which is a function call made by the ai assistant:
```
[{'id': 'fc65a533', 'function': {'name': 'addition', 'arguments': '{"a": "4", "b": "6"}'}, 'type': 'function'}]
```

### Add Executed Tool Result to Message History & Continue the Conversation

```python
if function_call:
    # append the assistant tool call msg
    messages.append({"role": "assistant", "tool_calls": function_call})
    # append the result of the tool call in openai format, in this case, the value of add 6 to 4 is 10.
    messages.append({'role': 'tool', 'tool_call_id': function_call[0]["id"], 'name': function_call[0]["function"]["name"], 'content': '10'})
    raw_output = run_model(messages, functions)
    # Check if there's a function call
    function_call = postprocess_output(raw_output)
    if function_call:
        print(function_call)
    else:
        print(raw_output)
```

The LLM will make another call
```
[{'id': '2ffc3de4', 'function': {'name': 'addition', 'arguments': '{"a": "10", "b": "2"}'}, 'type': 'function'}]
```

