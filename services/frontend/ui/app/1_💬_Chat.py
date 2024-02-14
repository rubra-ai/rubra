# Standard Library
import asyncio
import logging
import time

# Third Party
import streamlit as st
import websockets
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
    Choice,
    ChoiceDelta,
    ChoiceDeltaFunctionCall,
    ChoiceDeltaToolCall,
    ChoiceDeltaToolCallFunction,
)
from rubra_ui_config import RUBRA_BACKEND_URL, get_entity_options, rubra_client
from rubra_ui_utils import remove_streamlit_elements

st.set_page_config(page_title="Rubra Chat", page_icon="🐿", layout="wide")
remove_streamlit_elements()
st.markdown(f"<h1 style='color: #E53935;'>Rubra Chat</h1>", unsafe_allow_html=True)

logging.basicConfig(level=logging.INFO)


# Initialize session state variables if not already set
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "selected_entity" not in st.session_state:
    st.session_state.selected_entity = None
if "entity_options" not in st.session_state:
    st.session_state.entity_options = get_entity_options()
if "messages" not in st.session_state:
    st.session_state.messages = []

default_index = 0
welcome_assistant_label = "Assistant: Welcome Assistant"

def escape_colons_for_display(text):
    """
    Escapes colons in the text to prevent Streamlit's markdown renderer
    from interpreting them as emoji shortcodes.
    """
    return text.replace(":", "\\:")

# Search for the "Welcome Assistant" in the entity options and set it as the default if found
for i, (label, _) in enumerate(st.session_state.entity_options):
    if label == welcome_assistant_label:
        default_index = i
        break

# If the chat has not started, we can set the default to "Welcome Assistant"
if not st.session_state.chat_started:
    selected_entity = st.selectbox(
        "Select a Model or an Assistant",
        st.session_state.entity_options,
        index=default_index,  # use the default_index here
        disabled=st.session_state.chat_started,
        format_func=lambda x: x[0],
    )
else:
    # If the chat has started, use the previously selected entity
    selected_entity = st.selectbox(
        "Select a Model or an Assistant",
        st.session_state.entity_options,
        index=default_index,  # use the default_index here
        disabled=st.session_state.chat_started,
        format_func=lambda x: x[0],
    )

# Set the session state only if a selection is made
if selected_entity:
    st.session_state.selected_entity = selected_entity[1]


def run_websocket(channel, message_placeholder, thread_id, run_id):
    async def connect():
        logging.info("Running websocket on channel: /ws/%s/%s", thread_id, run_id)
        uri = f"{RUBRA_BACKEND_URL.replace('http', 'ws')}/ws/{thread_id}/{run_id}"

        async with websockets.connect(uri) as websocket:
            conversation = ""
            function_call = ""
            while True:
                # Check if the websocket is closed
                if websocket.closed:
                    logging.info("WebSocket connection closed.")
                    break

                try:
                    message = await websocket.recv()
                    if message == "CLOSE_CONNECTION":
                        logging.info("Closing connection")
                        break  # Exit the loop to close the connection

                    chunk: ChatCompletionChunk = eval(message)
                    content = chunk.choices[0].delta.content
                    if (
                        chunk.choices[0].delta.tool_calls
                        or chunk.choices[0].delta.function_call
                    ):  # check function call
                        if (
                            chunk.choices[0].delta.tool_calls
                            and chunk.choices[0].delta.tool_calls[0].function.name
                        ):  # openai
                            function_call += (
                                chunk.choices[0].delta.tool_calls[0].function.name
                            )
                        elif chunk.choices[0].delta.function_call:  # custom model
                            function_call += content
                    else:  # check content
                        if content:
                            escape_colons_for_display(content)
                            conversation += content
                            message_placeholder.markdown(conversation + "▌")

                    if function_call:
                        if "FileKnowledge" in function_call:
                            message_placeholder.status(
                                ":open_file_folder: Using knowledge from Assistant's files"
                            )
                            function_call = ""
                        elif "GoogleSearchTool" in function_call:
                            message_placeholder.status(
                                ":globe_with_meridians: Browsing the web for you"
                            )
                            function_call = ""
                except websockets.exceptions.ConnectionClosed as e:
                    logging.info("WebSocket connection closed unexpectedly: %s", e)
                    break
                except Exception as e:
                    logging.error("Error processing message: %s", e)

            # Once the loop is broken, finalize the conversation display
            message_placeholder.markdown(conversation)
            st.session_state.messages.append(
                {"role": "assistant", "content": conversation}
            )

    asyncio.new_event_loop().run_until_complete(connect())

# Handle new chat input
prompt = st.chat_input("Message Rubra...")

# Add a Clear Chat button
if st.button("Clear Chat"):
    st.session_state.chat_started = False
    st.session_state.selected_entity = None
    st.session_state.messages = []
    if "assistant_id" in st.session_state:
        del st.session_state["assistant_id"]
    if "thread_id" in st.session_state:
        del st.session_state["thread_id"]
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        escaped_content = escape_colons_for_display(message["content"])
        st.markdown(escaped_content)

# Update the chat_started state as soon as there is a prompt
if prompt:
    st.session_state.chat_started = True
    escaped_prompt = escape_colons_for_display(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(escaped_prompt)

    # Determine the type of the selected entity and process accordingly
    if st.session_state.selected_entity.startswith("model_"):
        # Process chat with model
        model_id = st.session_state.selected_entity.split("model_")[1]
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            logging.info(
                "Start Time: %s", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            )
            logging.info("running with model id " + model_id)
            for response in rubra_client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.content or ""
                message_placeholder.markdown(escape_colons_for_display(full_response) + "▌")
            message_placeholder.markdown(escape_colons_for_display(full_response))
            logging.info(
                "End Time: %s", time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
            )
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
    elif st.session_state.selected_entity.startswith("assistant_"):
        logging.info("Chatting with an assistant")
        # Process chat with assistant
        assistant_id = st.session_state.selected_entity.split("assistant_")[1]
        st.session_state["assistant_id"] = assistant_id

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            # Check if a thread already exists
            if "thread_id" in st.session_state:
                logging.info(
                    "adding message to existing thread %s",
                    st.session_state["thread_id"],
                )
                # Add the new message to the existing thread
                rubra_client.beta.threads.messages.create(
                    st.session_state["thread_id"],
                    role="user",
                    content=prompt,
                )
            else:
                # Create a new thread if it doesn't exist
                message_thread = rubra_client.beta.threads.create(
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    metadata={"created_in_ui": "true"},
                )
                st.session_state["thread_id"] = message_thread.id
                logging.info(message_thread)

            thread_run = rubra_client.beta.threads.runs.create(
                thread_id=st.session_state["thread_id"],
                assistant_id=st.session_state["assistant_id"],
            )
            logging.info(thread_run)

            message_placeholder.markdown(full_response + "▌")
            run_websocket(
                st.session_state["thread_id"],
                message_placeholder,
                st.session_state["thread_id"],
                thread_run.id,
            )
    st.rerun()
