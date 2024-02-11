# Standard Library
import logging
import os
import time

# Third Party
import requests
import streamlit as st
from litellm import check_valid_key
from rubra_ui_utils import remove_streamlit_elements

# Constants and Configuration
RUBRA_BACKEND_HOST = os.getenv("RUBRA_BACKEND_HOST", "localhost")
LITELLM_HOST = os.getenv("LITELLM_HOST", "localhost")
RUBRA_BACKEND_URL = f"http://{RUBRA_BACKEND_HOST}:8000"
LITELLM_URL = f"http://{LITELLM_HOST}:8002"
MODEL_INFO_URL = f"{RUBRA_BACKEND_URL}/models/info"
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}

logging.basicConfig(level=logging.INFO)

# Model Providers Data
model_providers = {
    # "Azure": {
    #     "api_base_required": True,
    #     "api_key_required": True,
    #     "custom_llm_provider": "azure",
    #     "models": [
    #         "gpt-4",
    #         "gpt-4-0314",
    #         "gpt-4-0613",
    #         "gpt-4-32k",
    #         "gpt-4-32k-0314",
    #         "gpt-4-32k-0613",
    #         "gpt-3.5-turbo",
    #         "gpt-3.5-turbo-0301",
    #         "gpt-3.5-turbo-0613",
    #         "gpt-3.5-turbo-16k",
    #         "gpt-3.5-turbo-16k-0613",
    #     ],
    # },
    "OpenAI": {
        "api_base_required": False,
        "api_key_required": True,
        "custom_llm_provider": "openai",
        "models": [
            "gpt-4-0125-preview",
            "gpt-4-1106-preview",
            "gpt-4",
            "gpt-4-32k",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
        ],
    },
    "Anthropic": {
        "api_key_required": True,
        "models": ["claude-2.1"],
    },
    "Local": {
        "api_base": "http://host.docker.internal:1234/v1",
        "api_key_required": False,
        "custom_llm_provider": "openai",
        "models": ["custom"],
    },
}


# API Helper Functions
def get_model_info():
    response = requests.get(MODEL_INFO_URL)
    if response.status_code == 200:
        return response.json().get("data", [])
    return []


def add_new_model(model, api_key, selected_provider, api_base=None):
    # Retrieve custom_llm_provider value
    custom_llm_provider = model_providers[selected_provider].get(
        "custom_llm_provider", None
    )

    # Initialize litellm_params with mandatory keys
    litellm_params = {
        "model": model,
        "api_key": api_key,
    }

    # Conditionally add custom_llm_provider if it's not None
    if custom_llm_provider is not None:
        litellm_params["custom_llm_provider"] = custom_llm_provider

    if api_base:
        litellm_params["api_base"] = api_base

    data = {
        "model_name": model,
        "litellm_params": litellm_params,
        "model_info": {
            "id": model,
            "created": int(time.time()),
        },
    }
    response = requests.post(
        f"{RUBRA_BACKEND_URL}/models/new", json=data, headers=HEADERS
    )
    return response


def delete_model(model_id):
    data = {"id": model_id}
    response = requests.post(
        f"{RUBRA_BACKEND_URL}/models/delete", json=data, headers=HEADERS
    )
    return response


def get_api_key_status():
    response = requests.get(f"{RUBRA_BACKEND_URL}/get_api_key_status")
    if response.status_code == 200:
        active_keys = {}
        for key in response.json().items():
            if key[1]:
                active_keys[key[0]] = key[1]
        return active_keys
    else:
        st.error("Failed to retrieve API key status.")
        return {}


def handle_update_api_key(api_key_name, new_api_key):
    # Prepare the data for the API request
    data = {api_key_name: True if new_api_key else False}

    # Send the update request to the backend
    response = requests.post(
        f"{RUBRA_BACKEND_URL}/set_api_keys", json=data, headers=HEADERS
    )
    if response.status_code == 200:
        logging.info(f"{api_key_name} updated successfully in redis")
    else:
        st.error(
            f"Failed to update {api_key_name}. Status code: {response.status_code}"
        )


def handle_delete_api_key(api_key_name):
    # Prepare the data for the API request
    data = {api_key_name: False}  # An empty string signifies deletion

    # Send the delete request to the backend
    response = requests.post(
        f"{RUBRA_BACKEND_URL}/set_api_keys", json=data, headers=HEADERS
    )
    if response.status_code == 200:
        st.success(f"{api_key_name} deleted successfully.")
    else:
        st.error(
            f"Failed to delete {api_key_name}. Status code: {response.status_code}"
        )


def validate_and_update_api_key(provider, api_key, api_key_status):
    model_to_check = "gpt-3.5-turbo" if provider == "OpenAI" else "claude-2.1"
    valid_key = check_valid_key(model=model_to_check, api_key=api_key)

    if valid_key:
        st.success(f"{provider} API Key is valid...")
        env_var_name = "OPENAI_API_KEY" if provider == "OpenAI" else "ANTHROPIC_API_KEY"
        # Check if the key is already set
        if not api_key_status.get(env_var_name):
            # Key is not set, so call handle_update_api_key
            handle_update_api_key(env_var_name, api_key)

        # Update the key in the backend without calling handle_update_api_key
        update_data = {"environment_variables": {env_var_name: api_key}}
        response = requests.post(
            f"{RUBRA_BACKEND_URL}/config/update", json=update_data, headers=HEADERS
        )
        if response.status_code == 200:
            st.success(f"{provider} API Key updated successfully.", icon="✅")
        else:
            st.error(
                f"Failed to update {provider} API Key. Status code: {response.status_code}"
            )
    else:
        st.error("Invalid API Key.")


# UI Helper Functions
def format_cost(cost):
    return "${:,.6f}".format(cost) if cost is not None else "N/A"


def format_max_tokens(tokens):
    return "{:,}".format(tokens) if tokens is not None else "N/A"


# Streamlit UI Code
def setup_streamlit_ui():
    st.set_page_config(page_title="Rubra Settings", page_icon="🐿", layout="wide")
    remove_streamlit_elements()
    render_model_info_section()
    render_api_key_management_section()
    render_add_new_model_section()
    # render_remove_model_section()


def render_model_info_section():
    st.markdown(
        f"<h1 style='color: #E53935;'>Rubra Settings</h1>", unsafe_allow_html=True
    )
    model_info_list = get_model_info()
    st.markdown("##### Configured Models")
    for model_info in model_info_list:
        model_name = model_info.get("model_name", "Unknown Model")
        model_details = model_info.get("model_info", {})
        model_litellm_params = model_info.get("litellm_params", {})
        model_id = model_info.get("model_info", {}).get("id", "Unknown ID")

        with st.expander(f"{model_name}", expanded=False):
            st.caption(f"Model ID: {model_litellm_params['model']}")
            if model_litellm_params.get("api_base"):
                st.caption(f"LLM Base API: {model_litellm_params['api_base']}")
            if model_details.get("max_tokens"):
                st.caption(
                    f"Max Tokens: {format_max_tokens(model_details.get('max_tokens'))}"
                )
            if model_details.get("input_cost_per_token"):
                st.caption(
                    f"Input Cost per Token: {format_cost(model_details.get('input_cost_per_token'))}"
                )
            if model_details.get("output_cost_per_token"):
                st.caption(
                    f"Output Cost per Token: {format_cost(model_details.get('output_cost_per_token'))}"
                )
            # Add a button for each model to remove it
            if model_id != "Unknown ID":
                if st.button("Remove", key=f"remove_{model_id}", type="primary"):
                    response = delete_model(model_id)
                    if response.status_code == 200:
                        st.success(f"Model {model_name} successfully removed.")
                    else:
                        st.error(
                            f"Failed to remove model {model_name}. Status code: {response.status_code}"
                        )


def render_add_new_model_section():
    st.markdown("---")
    st.markdown(
        "##### Add a New Model",
        help="For all remote models, an API key is required. Set the API key in the API Key Management section.",
    )

    # Retrieve API key status and configured models
    api_key_status = get_api_key_status()
    model_info_list = get_model_info()
    configured_models = [
        model_info.get("model_name", "") for model_info in model_info_list
    ]

    # Update model_providers list based on conditions
    selectable_providers = []
    if api_key_status.get("OPENAI_API_KEY"):
        selectable_providers.append("OpenAI")
    if api_key_status.get("ANTHROPIC_API_KEY"):
        selectable_providers.append("Anthropic")
    if "custom" not in configured_models:
        selectable_providers.append("Local")

    selected_provider = st.selectbox(
        "Select a Model Provider", [""] + selectable_providers
    )

    all_fields_filled = True  # Flag to check if all required fields are filled

    if selected_provider:
        models = model_providers[selected_provider]["models"]
        api_key_required = model_providers[selected_provider].get(
            "api_key_required", False
        )
        api_base_required = model_providers[selected_provider].get(
            "api_base_required", False
        )
        selected_model = st.selectbox("Select a Model", models)
        # Set api_key based on the selected provider
        if api_key_required:
            if selected_provider == "Anthropic":
                api_key = "os.environ/ANTHROPIC_API_KEY"
            elif selected_provider == "OpenAI":
                api_key = "os.environ/OPENAI_API_KEY"
        else:
            api_key = None
        api_base = st.text_input("API Base") if api_base_required else None
        submit_button = st.button("Add Model")

        # Check if all required fields are filled
        if api_key_required and not api_key:
            all_fields_filled = False
        if api_base_required and not api_base:
            all_fields_filled = False
        if not all([selected_model, selected_provider]):
            all_fields_filled = False

        if submit_button:
            if all_fields_filled:
                response = add_new_model(
                    selected_model,
                    api_key,
                    selected_provider,
                    api_base,
                )

                if response.status_code == 200:
                    st.success("Model successfully added.")
                else:
                    st.error(
                        f"Failed to add model. Status code: {response.status_code}"
                    )
            else:
                st.warning("Please fill out all required fields before submitting.")


def render_remove_model_section():
    st.markdown("---")
    st.markdown("##### Remove a Model")
    model_id_to_remove = st.text_input("Model to Remove")
    remove_button = st.button("Remove Model")

    if remove_button:
        if model_id_to_remove:
            response = delete_model(model_id_to_remove)
            if response.status_code == 200:
                st.success("Model successfully removed.")
            else:
                response_json = response.json()
                if "detail" in response_json:
                    st.error(f"Failed to remove model. {response_json['detail']}")
                else:
                    st.error(
                        f"Failed to remove model. Status code: {response.status_code}"
                    )
        else:
            st.warning("Please enter a model ID to remove.")


def render_api_key_management_section():
    st.markdown("---")
    st.markdown("##### API Key Management")
    with st.expander("Add, remove, update API keys here", expanded=False):
        # Retrieve and display the status of API keys
        api_key_status = get_api_key_status()

        # Initialize the provider options
        provider_options = [""]

        # Check if OpenAI API key is set and if not, add it to the options
        if (
            "OPENAI_API_KEY" not in api_key_status
            or not api_key_status["OPENAI_API_KEY"]
        ):
            provider_options.append("OpenAI")

        # Check if Anthropic API key is set and if not, add it to the options
        if (
            "ANTHROPIC_API_KEY" not in api_key_status
            or not api_key_status["ANTHROPIC_API_KEY"]
        ):
            provider_options.append("Anthropic")

        if api_key_status:
            st.markdown("###### Active API Keys:")
            for key, is_set in api_key_status.items():
                if is_set and is_set == True:
                    with st.form(f"{key}_form", clear_on_submit=True):
                        st.markdown(
                            f"<span style='color:green'>**{key}**</span>",
                            unsafe_allow_html=True,
                        )
                        new_api_key = st.text_input(f"New Key Value", type="password")
                        update_button = st.form_submit_button("Update")
                        delete_button = st.form_submit_button("Delete", type="primary")

                        if update_button:
                            handle_update_api_key(key, new_api_key)
                        elif delete_button:
                            handle_delete_api_key(key)

        if len(provider_options) > 1:
            st.markdown("###### Add New API Key:")
            provider = st.selectbox("Select a Provider", provider_options)
            api_key = st.text_input("API Key", type="password")

            if provider and api_key:
                validate_and_update_api_key(provider, api_key, api_key_status)


if __name__ == "__main__":
    setup_streamlit_ui()
