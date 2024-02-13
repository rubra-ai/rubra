---
sidebar_position: 0
title: Web Search and Browsing
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

Check out this code and no-code example of web browsing in Rubra using the OpenAI API. This example uses the local model and a browser tool to search for information on Google.

<Tabs
  defaultValue="code"
  values={[
    {label: 'Code', value: 'code'},
    {label: 'UI', value: 'ui'},
  ]}>
  
  <TabItem value="code">

#### Import the OpenAI package and point to your Rubra instance
```python
from openai import OpenAI
import time

client = OpenAI(
    base_url="http://localhost:8000",  # Rubra backend
    api_key="abc"
)
```

#### Create a new assistant with browsing enabled
```python
assistant = client.beta.assistants.create(
    name="Google Search GPT",
    instructions="You are a helpful assistant who helps user with access to google search.",
    tools=[{"type": "browser"}],
    # model="custom",  # should match model name in litellm config
    model="custom",
    file_ids=[]
)
# Assistant(id='asst_7687f9', created_at=1707818960, description='', file_ids=[], instructions='You are a helpful assistant who helps user with access to google search.', metadata={}, model='custom', name='Google Search GPT', object='assistant', tools=[ToolCodeInterpreter(type='browser')], _id='65cb3fd0e3013eec8abc4694')
```

#### Create a chat message
```python
message_thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": "What is Google Gemini?",
    },
  ],
  metadata={"foo": "bar"}
)
# Thread(id='thread_f64031', created_at=1707818969, metadata={'foo': 'bar'}, object='thread', _id='65cb3fd9e3013eec8abc4695')
```

#### Run the assistant
```python
run = client.beta.threads.runs.create(
  thread_id=message_thread.id,
  assistant_id=assistant.id
)
# Run(id='run_14040e', assistant_id='asst_7687f9', cancelled_at=None, completed_at=None, created_at=1707818970, expires_at=None, failed_at=None, file_ids=[], instructions='You are a helpful assistant who helps user with access to google search.', last_error=None, metadata={}, model='custom', object='thread.run', required_action=None, started_at=None, status='queued', thread_id='thread_f64031', tools=[ToolAssistantToolsCode(type='browser')], _id='65cb3fdae3013eec8abc4697')
```

#### Display the chat messages
```python
from IPython.display import display, Markdown

for tm in reversed(client.beta.threads.messages.list(message_thread.id).data):
    if tm.role == "user":
        display(Markdown(f"**USER:** {tm.content[0].text.value}"))
    else:
        display(Markdown(f"\n**AI:** {tm.content[0].text.value}"))
```
**Output:**
```
USER: What is Google Gemini?

AI: {"function": "GoogleSearchTool", "args": {"query": "What is Google Gemini?"}}

AI: I did a quick search, here's what I discovered:

Google Gemini is a powerful and general AI model developed by Google. It's designed to be multimodal, meaning it can process different types of data such as text, images, audio, and more. The model comes in three different sizes: Ultra, Pro, and Nano, each optimized for specific tasks. Gemini is a significant step forward in AI technology and has the potential to bring new waves of innovation and economic progress. It's being used in various Google products like Search, Bard, Pixel smartphones, Ads, Chrome, and Duet AI.
```
  </TabItem>
  <TabItem value="ui">

#### Create a new assistant with browsing enabled
![Create](/img/examples/browsing/create.png)

#### Create a chat message and run the assistant
![Run](/img/examples/browsing/run.png)

#### Output
![Output](/img/examples/browsing/output.png)

  </TabItem>
</Tabs>