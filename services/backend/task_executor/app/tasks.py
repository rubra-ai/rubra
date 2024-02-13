# tasks.py
# Standard Library
import json
import os
import sys
from functools import partial

# Get the current working directory
current_directory = os.getcwd()

# Add the current directory to sys.path
sys.path.append(current_directory)

# Standard Library
import io
import logging
import uuid
from datetime import datetime

# Third Party
import redis
from celery import Celery, shared_task, signals
from openai import OpenAI
from pymongo import MongoClient

# Local
from app.backend_models import (
    AssistantObject,
    FilesStorageObject,
    MessageObject,
    RunStepObject,
)
from app.local_model import RubraLocalAgent
from app.models import Role7, Status2, Type8, Type824

litellm_host = os.getenv("LITELLM_HOST", "localhost")
redis_host = os.getenv("REDIS_HOST", "localhost")
mongodb_host = os.getenv("MONGODB_HOST", "localhost")

redis_client = redis.Redis(host=redis_host, port=6379, db=0)
app = Celery("tasks", broker=f"redis://{redis_host}:6379/0")
app.config_from_object("app.celery_config")
app.autodiscover_tasks(["app"])  # Explicitly discover tasks in 'app' package

# MongoDB Configuration
MONGODB_URL = f"mongodb://{mongodb_host}:27017"
DATABASE_NAME = "rubra_db"

# Global MongoDB client
mongo_client = None


@signals.worker_process_init.connect
def setup_mongo_connection(*args, **kwargs):
    global mongo_client
    mongo_client = MongoClient(f"mongodb://{mongodb_host}:27017")


def create_assistant_message(
    thread_id, assistant_id, run_id, content_text, role=Role7.assistant.value
):
    db = mongo_client[DATABASE_NAME]

    # Generate a unique ID for the message
    message_id = f"msg_{uuid.uuid4().hex[:6]}"

    # Create the message object
    message = {
        "id": message_id,
        "object": "thread.message",
        "created_at": int(datetime.now().timestamp()),
        "thread_id": thread_id,
        "role": role,
        "content": [
            {"type": "text", "text": {"value": content_text, "annotations": []}}
        ],
        "file_ids": [],
        "assistant_id": assistant_id,
        "run_id": run_id,
        "metadata": {},
    }

    # Insert the message into MongoDB
    db.messages.insert_one(message)


def rubra_local_agent_chat_completion(
    chat_agent: RubraLocalAgent,
    redis_channel,
    chat_messages: list,
    sys_instruction: str,
    thread_id: str,
    assistant_id: str,
    run_id: str,
):
    response = chat_agent.chat(
        msgs=chat_messages, sys_instruction=sys_instruction, stream=True
    )

    msg = ""
    if (
        len(chat_agent.tools) == 0
    ):  # if no tool, stream the response and return msg directly
        for r in response:
            if r.choices and r.choices[0].delta and r.choices[0].delta.content:
                msg += r.choices[0].delta.content

            redis_client.publish(redis_channel, str(r))
        return msg

    msg_state = "start"  # possible states: start, chat, function
    for r in response:
        if r.choices and r.choices[0].delta and r.choices[0].delta.content:
            msg += r.choices[0].delta.content
            logging.debug(f" msg : {msg}  msg_state: {msg_state}")
            if msg_state == "function":
                r.choices[0].delta.function_call = {"type": "function"}

            if '"function":' in msg or '"content": "' in msg:
                if msg_state == "start":
                    if '"content": "' in msg:
                        msg_state = "chat"
                        r.choices[0].delta.content = msg.split('"content": "')[1]
                    else:
                        msg_state = "function"
                        r.choices[0].delta.content = msg
                        r.choices[0].delta.function_call = {"type": "function"}
                elif msg_state == "chat":
                    if r.choices[0].delta.content.endswith('"'):
                        try:
                            json.loads(msg + "}")
                            r.choices[0].delta.content = r.choices[
                                0
                            ].delta.content.split('"')[0]
                        except:
                            pass
                    if r.choices[0].delta.content.endswith("}"):
                        try:
                            json.loads(msg)
                            r.choices[0].delta.content = r.choices[
                                0
                            ].delta.content.split("}")[0]
                        except:
                            pass

        if msg_state != "start":
            redis_client.publish(redis_channel, str(r))

    is_function_call, parsed_msg = chat_agent.validate_function_call(msg)
    ## TODO: create run_step object.

    if is_function_call:
        logging.info("=====function call========")
        function_call_content = parsed_msg
        chat_messages.append(
            {"role": Role7.assistant.value, "content": function_call_content}
        )
        create_assistant_message(
            thread_id, assistant_id, run_id, content_text=function_call_content
        )

        function_response = chat_agent.get_function_response(
            function_call_json=json.loads(parsed_msg)
        )

        parsed_msg = function_response

        last_chunk = r
        last_chunk.choices[0].delta.function_call = None
        last_chunk.choices[0].delta.content = parsed_msg
        redis_client.publish(redis_channel, str(last_chunk))
        last_chunk.choices[0].delta.content = ""
        redis_client.publish(redis_channel, str(last_chunk))
        print(f"message: {parsed_msg}")

    return parsed_msg


def form_openai_tools(tools, assistant_id: str):
    # Local
    from app.tools.file_knowledge_tool import FileKnowledgeTool
    from app.tools.web_browse_tool.web_browse_tool import WebBrowseTool

    retrieval = FileKnowledgeTool()
    googlesearch = WebBrowseTool()
    res_tools = []
    available_function = {}
    for t in tools:
        if t["type"] == Type8.retrieval.value:
            retrieval_tool = {
                "type": "function",
                "function": {
                    "name": retrieval.name,
                    "description": retrieval.description,
                    "parameters": retrieval.parameters,
                },
            }
            res_tools.append(retrieval_tool)
            retrieval_func = partial(retrieval._run, assistant_id=assistant_id)
            available_function[retrieval.name] = retrieval_func
        elif t["type"] == Type824.retrieval.value:
            gs_tool = {
                "type": "function",
                "function": {
                    "name": googlesearch.name,
                    "description": googlesearch.description,
                    "parameters": googlesearch.parameters,
                },
            }
            res_tools.append(gs_tool)
            available_function[googlesearch.name] = googlesearch._run
        else:
            res_tools.append(t)
    return res_tools, available_function


@shared_task
def execute_chat_completion(assistant_id, thread_id, redis_channel, run_id):
    try:
        oai_client = OpenAI(
            base_url=f"http://{litellm_host}:8002/v1/",
            api_key="abc",  # point to litellm server
        )
        db = mongo_client[DATABASE_NAME]

        # Fetch assistant and thread messages synchronously
        assistant = db.assistants.find_one({"id": assistant_id})
        thread_messages = list(db.messages.find({"thread_id": thread_id}))

        if not assistant or not thread_messages:
            raise ValueError("Assistant or Thread Messages not found")

        # Update the run status to in_progress and set the started_at timestamp
        started_at = int(datetime.now().timestamp())
        db.runs.update_one(
            {"id": run_id},
            {"$set": {"status": Status2.in_progress.value, "started_at": started_at}},
        )

        print("Calling model:", assistant["model"])

        if assistant["model"].startswith("claude-") or assistant["model"].startswith(
            "gpt-"
        ):
            # Prepare the chat messages for OpenAI
            chat_messages = [{"role": "system", "content": assistant["instructions"]}]
            for msg in thread_messages:
                content_text = (
                    msg["content"][0]["text"]["value"]
                    if msg["content"]
                    and isinstance(msg["content"], list)
                    and "text" in msg["content"][0]
                    else ""
                )
                chat_messages.append({"role": msg["role"], "content": content_text})

            print("Chat Messages:", chat_messages)

            # Call OpenAI for chat completion
            oai_tools, available_function = form_openai_tools(
                assistant["tools"], assistant_id=assistant_id
            )
            print("oai_tools", oai_tools)
            # filter out code interpreter and browser for now
            oai_tools = [
                tool for tool in oai_tools if tool["type"] != "code_interpreter"
            ]

            if oai_tools:
                response = oai_client.chat.completions.create(
                    model=assistant["model"],
                    messages=chat_messages,
                    tools=oai_tools,
                    tool_choice="auto",
                    temperature=0.1,
                    top_p=0.95,
                    stream=True,
                )
            else:
                response = oai_client.chat.completions.create(
                    model=assistant["model"],
                    messages=chat_messages,
                    temperature=0.1,
                    top_p=0.95,
                    stream=True,
                )

            # Iterate over the response chunks and construct the assistant's response
            assistant_response = ""
            function_call_list_dict = []
            for i, chunk in enumerate(response):
                if chunk.choices and chunk.choices[0].delta:
                    if chunk.choices[
                        0
                    ].delta.tool_calls:  # openai can do multi-tool-call
                        print(chunk.choices[0].delta)
                        for tc in chunk.choices[0].delta.tool_calls:
                            if tc.function.name:  # the first chunk
                                function_call_list_dict.append(
                                    {
                                        "name": tc.function.name,
                                        "id": tc.id,
                                        "argument": tc.function.arguments or "",
                                    }
                                )

                            else:
                                function_call_list_dict[-1][
                                    "argument"
                                ] += tc.function.arguments
                    elif chunk.choices[0].delta.content:
                        assistant_message = chunk.choices[0].delta.content
                        assistant_response += assistant_message
                redis_client.publish(redis_channel, str(chunk))

            while function_call_list_dict:
                print(f"called function : {function_call_list_dict}")
                print(f"num of functions: {len(function_call_list_dict)}")

                function_call_msg = {
                    "content": "",
                    "role": "assistant",
                    "tool_calls": [],
                }
                for j, fc in enumerate(function_call_list_dict):
                    this_fc = {
                        "index": 0,
                        "id": fc["id"],
                        "function": {"arguments": fc["argument"], "name": fc["name"]},
                        "type": "function",
                    }
                    function_call_msg["tool_calls"].append(this_fc)
                print(function_call_msg)
                chat_messages.append(function_call_msg)
                for ftc in function_call_list_dict:
                    if ftc["name"] not in available_function:
                        # TODO: in this case, add a runstep object. And the user is responsible to submit the tool output
                        pass
                    else:
                        function_args = json.loads(ftc["argument"])
                        function_response = available_function[ftc["name"]](
                            **function_args
                        )
                        function_response_content = json.dumps(function_response)

                        chat_messages.append(
                            {
                                "tool_call_id": ftc["id"],
                                "role": "tool",
                                "name": ftc["name"],
                                "content": function_response_content,
                            }
                        )

                response = oai_client.chat.completions.create(
                    model=assistant["model"],
                    messages=chat_messages,
                    tools=oai_tools,
                    tool_choice="auto",
                    temperature=0.1,
                    top_p=0.95,
                    stream=True,
                )
                # Iterate over the response chunks and construct the assistant's response
                assistant_response = ""
                function_call_list_dict = []
                for i, chunk in enumerate(response):
                    if chunk.choices and chunk.choices[0].delta:
                        if chunk.choices[
                            0
                        ].delta.tool_calls:  # openai can do multi-tool-call
                            print(chunk.choices[0].delta.tool_calls)
                            for i, tc in enumerate(chunk.choices[0].delta.tool_calls):
                                if tc.function.name:  # the first chunk
                                    function_call_list_dict.append(
                                        {
                                            "name": tc.function.name,
                                            "id": tc.id,
                                            "argument": tc.function.arguments or "",
                                        }
                                    )

                                else:
                                    function_call_list_dict[-1][
                                        "argument"
                                    ] += tc.function.arguments
                        elif chunk.choices[0].delta.content:
                            assistant_message = chunk.choices[0].delta.content
                            assistant_response += assistant_message
                        # redis_client.publish(redis_channel, str(assistant_message))
                    redis_client.publish(redis_channel, str(chunk))

        else:  # assume local model
            chat_messages = []
            for msg in thread_messages:
                content_text = (
                    msg["content"][0]["text"]["value"]
                    if msg["content"]
                    and isinstance(msg["content"], list)
                    and "text" in msg["content"][0]
                    else ""
                )
                chat_messages.append({"role": msg["role"], "content": content_text})

            chat_agent = RubraLocalAgent(
                assistant_id=assistant_id, tools=assistant["tools"]
            )
            sys_instruction = assistant["instructions"]
            assistant_response = rubra_local_agent_chat_completion(
                chat_agent,
                redis_channel,
                chat_messages,
                sys_instruction,
                thread_id,
                assistant_id,
                run_id,
            )

        # Check if there's a valid response to add as an assistant message
        if assistant_response.strip():
            # Create a new message from the assistant
            create_assistant_message(
                thread_id, assistant_id, run_id, assistant_response
            )
            print("Assistant message created:", assistant_response)

        # Update the run status to completed and set the completed_at timestamp after successful completion
        completed_at = int(datetime.now().timestamp())
        db.runs.update_one(
            {"id": run_id},
            {"$set": {"status": Status2.completed.value, "completed_at": completed_at}},
        )
        redis_client.publish(
            f"task_status_{thread_id}",
            json.dumps(
                {"thread_id": thread_id, "run_id": run_id, "status": "completed"}
            ),
        )

    except Exception as e:
        print(f"Error in execute_chat_completion: {str(e)}")
        # Update the run status to failed and set the failed_at timestamp in case of an exception
        failed_at = int(datetime.now().timestamp())
        db.runs.update_one(
            {"id": run_id},
            {"$set": {"status": Status2.failed.value, "failed_at": failed_at}},
        )
        redis_client.publish(
            f"task_status_{thread_id}",
            json.dumps({"thread_id": thread_id, "run_id": run_id, "status": "failed"}),
        )

        raise


@app.task
def execute_asst_file_create(file_id: str, assistant_id: str):
    # Standard Library
    import json

    # Third Party
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from chardet import detect

    # Local
    from app.vector_db.milvus.main import add_texts

    try:
        db = mongo_client[DATABASE_NAME]
        collection_name = assistant_id
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        parsed_text = ""

        file_object = db.files_storage.find_one({"id": file_id})
        logging.info(f"processing file id : {file_id}")

        if file_object["content_type"] == "application/pdf":
            # Third Party
            from PyPDF2 import PdfReader

            reader = PdfReader(io.BytesIO(file_object["content"]))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"

            parsed_text = text

        elif file_object["content_type"] == "application/json":
            res = json.loads(file_object["content"])
            parsed_text = res
        else:  ## try to read plain text
            try:
                parsed_text = file_object["content"].decode('utf-8')
            except UnicodeDecodeError:
                try:
                    # Attempt to detect encoding and decode
                    encoding = detect(file_object["content"])['encoding']
                    parsed_text = file_object["content"].decode(encoding)
                except Exception as e:
                    logging.error(f"Decoding error with detected encoding: {e}")
                    parsed_text = ""

        if parsed_text != "":
            # Split docs and add to milvus vector DB
            texts = text_splitter.split_text(parsed_text)
            metadatas = [{"file_id": file_id} for t in texts]
            pks = add_texts(collection_name, texts=texts, metadatas=metadatas)

        logging.info(f"file {file_id} processing completed")
    except Exception as e:
        print(f"Error in execute_asst_file_create: {str(e)}")
