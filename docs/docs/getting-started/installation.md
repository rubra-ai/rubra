---
title: Installation
---

:::note

Ensure you have met the [prerequisites](/getting-started/prerequisites) before proceeding with the installation.

:::

To install Rubra, follow these steps:

1. Clone the Rubra GitHub repository by running the following command in your terminal:

    ```shell
    git clone https://github.com/sanjay920/rubra.git
    ```

2. Change into the `rubra` directory:

    ```shell
    cd rubra
    ```

3. Specify the models you want to give Rubra access to by editing the `llm-config.yaml` file. See [LLM Configution instructions](/getting-started/llm-config) for more information.

4. Pull the required Docker images and start Rubra

    ```shell
    docker-compose pull  && docker-compose up -d
    ```

After following these steps, Rubra should be successfully installed and running on your local machine.

You can access the Rubra UI by visiting [http://localhost:8501](http://localhost:8501/) in your browser.

You can develop with Rubra backend by setting the OpenAI base URL to Rubra backend's URL. By default, Rubra backend runs on [http://localhost:8000](http://localhost:8000/).

```
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/", api_key="abc")
```
