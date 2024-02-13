# Standard Library
import os

import openai

# Third Party
from openai import OpenAI

openai.api_key = "..."

rubra_backend_host = os.getenv("RUBRA_BACKEND_HOST", "localhost")
RUBRA_BACKEND_URL = f"http://{rubra_backend_host}:8000"
rubra_client = OpenAI(base_url=RUBRA_BACKEND_URL, api_key="abc")

def get_all_assistants():
    all_assistants = []
    after = None
    while True:
        response = rubra_client.beta.assistants.list(limit=100, after=after)
        assistants = response.data
        all_assistants.extend(assistants)
        if len(assistants) < 100:
            break
        else:
            after = assistants[-1]["id"]

    return all_assistants

def get_configured_models():
    configured_models = rubra_client.models.list().data
    print(configured_models)
    return [("Model: " + model.id, "model_" + model.id) for model in configured_models]


def get_assistants():
    assistants = get_all_assistants()
    return [
        ("Assistant: " + assistant.name, "assistant_" + assistant.id)
        for assistant in assistants
    ]


def get_entity_options():
    return get_configured_models() + get_assistants()
