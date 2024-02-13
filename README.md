# Rubra

Rubra is an open-source ChatGPT. It's designed for users who want:

- **Multi-Model Support:** Rubra integrates with a variety of LLMs, including a local model optimized for Rubra, as well as models from OpenAI and Anthropic. More providers will be added in the future.
- **Assistant Tools:** Create powerful assistants using tools for web search, knowledge retrieval, and more, all designed to augment your LLMs with the information they need to be truly helpful.
- **OpenAI API Compatibility:** Use Rubra's OpenAI-compatible Assistants API, allowing you to use OpenAI's Python and JavaScript libraries to create and manage Assistants.
- **Self-Hosting:** Keep your data private and secure by running Rubra on your own hardware.

## Getting Started

### Prerequisites

- M-series Mac or Linux with GPU
  - On MacOS you need to have Xcode Command Line Tools installed: `xcode-select --install`
- At least 16 GB RAM
- At least 10 GB of available disk space
- Docker and Docker Compose installed

### Installation

Rubra offers a simple one-command installation:

```bash
curl -sfL https://get.rubra.ai | sh -s -- start
```

After installation, access the Rubra UI at `http://localhost:8501` and start exploring the capabilities of your new ChatGPT-like assistant.

## Usage

Here's a quick example of how to create an assistant using Rubra's API, compatible with OpenAI's libraries:

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000",  # Rubra backend
    api_key=""
)

assistant = client.beta.assistants.create(
  instructions="You are a customer support chatbot. Use your knowledge base to best respond to customer queries.",
  model="rubra_local",
  tools=[{"type": "retrieval"}],
  file_ids=[client.files.create(file=open("knowledge.txt", "rb"), purpose='assistants').id]
)
```

## Contributing

We welcome contributions from the developer community! Whether it's adding new features, fixing bugs, or improving documentation, your help is invaluable. Check out our [contributing guidelines](CONTRIBUTING.md) for more information on how to get involved.

## Support

If you encounter any issues or have questions, please file an issue on GitHub. For more detailed guidance and discussions, join our community on [Discord](https://discord.gg/swvAH2DXZH) or [Slack](https://slack.acorn.io) or start a [Github discussion](https://github.com/acorn-io/rubra/discussions).

---

## License

Copyright (c) 2024 Acorn Labs, Inc.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
