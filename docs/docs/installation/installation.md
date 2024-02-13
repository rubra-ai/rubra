---
sidebar_position: 1
title: Installation
---

:::note

Before proceeding with the installation, ensure you have met the [prerequisites](/installation/prerequisites).

:::

Follow these steps to install Rubra:

1. Clone the Rubra GitHub repository by executing the following command in your terminal:
    ```shell
    git clone https://github.com/acorn-io/rubra.git
    ```

2. Navigate into the `rubra` directory:
    ```shell
    cd rubra
    ```

3. (Optional) Define the models you want Rubra to access by modifying [`llm-config.yaml`](https://github.com/acorn-io/rubra/blob/main/llm-config.yaml). Refer to [LLM Configuration instructions](/installation/llm-config) for more details. 
Additionally, you can add or remove LLMs in the Rubra UI after installation.

4. Pull the necessary images and start Rubra:
    ```shell
    docker-compose pull  && docker-compose up -d
    ```

After completing these steps, Rubra should be successfully installed and running on your local machine. 

Access the Rubra UI by visiting [http://localhost:8501](http://localhost:8501/) in your browser.

Develop with Rubra backend by setting the OpenAI base URL to Rubra backend's URL. By default, Rubra backend runs on [http://localhost:8000](http://localhost:8000/).

```
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8000/", api_key="abc")
```