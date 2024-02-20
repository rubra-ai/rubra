# Standard Library
import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

# Third Party
import aioredis
import requests
from beanie import init_beanie
from celery import Celery
from fastapi import FastAPI, Form, HTTPException, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.websockets import WebSocketState
from motor.motor_asyncio import AsyncIOMotorClient
from openai import OpenAI
from pydantic import BaseModel
from pymongo import ASCENDING, DESCENDING
from starlette.websockets import WebSocketDisconnect

from .backend_models import (
    ApiKeysUpdateModel,
    AssistantFileObject,
    AssistantObject,
    CreateAssistantRequest,
    FilesStorageObject,
    FileUpload,
    ListAssistantFilesResponse,
    ListAssistantsResponse,
    ListFilesResponse,
    ListMessagesResponse,
    ListRunStepsResponse,
    MessageObject,
    OpenAIFile,
    RunObject,
    RunStepObject,
    ThreadObject,
)

from .helpers import (
    generate_assistant_id,
    generate_message_id,
    generate_run_id,
    generate_thread_id,
)
from .models import (
    AssistantToolsBrowser,
    AssistantToolsRetrieval,
    CreateAssistantFileRequest,
    CreateChatCompletionRequest,
    CreateChatCompletionResponse,
    CreateFileRequest,
    CreateMessageRequest,
    CreateRunRequest,
    CreateThreadRequest,
    DeleteAssistantFileResponse,
    DeleteAssistantResponse,
    DeleteFileResponse,
    DeleteThreadResponse,
    ListModelsResponse,
    MessageContentImageFileObject,
    MessageContentTextObject,
    Model,
    ModifyAssistantRequest,
    ModifyMessageRequest,
    ModifyRunRequest,
    ModifyThreadRequest,
    Object,
    Object7,
    Object8,
    Object14,
    Object20,
    Object21,
    Object22,
    Object23,
    Object24,
    Object25,
    Object28,
    Object29,
    Order1,
    Order3,
    Order5,
    Order7,
    Order9,
    Order11,
    Purpose,
    Purpose1,
    Role7,
    Role8,
    Status,
    Status2,
    SubmitToolOutputsRunRequest,
    Text,
    Type6,
    Type8,
    Type13,
    Type824,
)

litellm_host = os.getenv("LITELLM_HOST", "localhost")
redis_host = os.getenv("REDIS_HOST", "localhost")
mongodb_host = os.getenv("MONGODB_HOST", "localhost")

app = FastAPI()

origins = [
    "http://localhost:3000",  # Add the frontend host here
    "http://localhost",
    "https://docs.rubra.ai",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# MongoDB Configurationget
MONGODB_URL = f"mongodb://{mongodb_host}:27017"
DATABASE_NAME = "rubra_db"
LITELLM_URL = f"http://{litellm_host}:8002"
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}

# Initialize MongoDB client
mongo_client = AsyncIOMotorClient(MONGODB_URL)
database = mongo_client[DATABASE_NAME]

celery_app = Celery(broker=f"redis://{redis_host}:6379/0")

logging.basicConfig(level=logging.INFO)


def get_database():
    return database


@app.on_event("startup")
async def on_startup():
    await init_beanie(
        database=get_database(),
        document_models=[
            AssistantObject,
            ThreadObject,
            MessageObject,
            RunObject,
            OpenAIFile,
            FilesStorageObject,
            AssistantFileObject,
        ],
    )

    available_models = [r.id for r in litellm_list_model().data]
    if not available_models:
        logging.warning("No models configured.")
        return

    # TODO: model names should be configurable instead of hard-coded
    welcome_asst_instruction = "You are a welcoming assistant that greets users to Rubra - an LLM tool that makes it easy to create AI assistants."
    tool_use_instruction = "You have access to a web browser tool, so let the user know that you can browse the web to answer queries."

    tool_enabled_model_pool = ["custom", "gpt-4-1106-preview"]
    welcome_asst_model = "custom"  # default to custom model
    if welcome_asst_model not in available_models:
        if "gpt-4-1106-preview" in available_models:
            welcome_asst_model = "gpt-4-1106-preview"
        else:
            welcome_asst_model = available_models[0]

    if welcome_asst_model in tool_enabled_model_pool:
        welcome_asst_instruction += tool_use_instruction

    # Create the Welcome Assistant if it doesn't exist
    existing_assistant = await AssistantObject.find_one({"id": "asst_welcome"})
    if not existing_assistant:
        logging.info("Creating Welcome Assistant")
        assistant = AssistantObject(
            assistant_id="asst_welcome",
            object=Object20.assistant.value,
            created_at=int(datetime.now().timestamp()),
            name="Welcome Assistant",
            description="Welcome Assistant",
            model=welcome_asst_model,
            instructions=welcome_asst_instruction,
            tools=[{"type": Type824.retrieval.value}]
            if welcome_asst_model in tool_enabled_model_pool
            else [],  # browser
            file_ids=[],
            metadata={},
        )
        await assistant.insert()


@app.get("/get_api_key_status", tags=["API Keys"])
async def get_api_key_status():
    try:
        redis = await aioredis.from_url(
            f"redis://{redis_host}:6379/0", encoding="utf-8", decode_responses=True
        )
        openai_key = await redis.get("OPENAI_API_KEY")
        anthropic_key = await redis.get("ANTHROPIC_API_KEY")

        # Convert the string values to booleans
        openai_key_status = openai_key.lower() == "true" if openai_key else False
        anthropic_key_status = (
            anthropic_key.lower() == "true" if anthropic_key else False
        )

        return {
            "OPENAI_API_KEY": openai_key_status,
            "ANTHROPIC_API_KEY": anthropic_key_status,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/set_api_keys", tags=["API Keys"])
async def set_api_key_status(api_keys: ApiKeysUpdateModel):
    try:
        redis = await aioredis.from_url(
            f"redis://{redis_host}:6379/0", encoding="utf-8", decode_responses=True
        )

        logging.info("Setting API keys")
        logging.info(api_keys)

        async with redis:
            if api_keys.OPENAI_API_KEY is not None:
                logging.info("Setting OPENAI_API_KEY" + str(api_keys.OPENAI_API_KEY))
                await redis.set("OPENAI_API_KEY", str(api_keys.OPENAI_API_KEY))
            if api_keys.ANTHROPIC_API_KEY is not None:
                await redis.set("ANTHROPIC_API_KEY", str(api_keys.ANTHROPIC_API_KEY))

        return {"message": "API key status updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assistants", response_model=AssistantObject, tags=["Assistants"])
async def create_assistant(body: CreateAssistantRequest) -> AssistantObject:
    """
    Create an assistant with a model and instructions.
    """
    # Generate a unique ID for the assistant
    assistant_id = generate_assistant_id()
    logging.info("assistant_id: %s", assistant_id)

    # Create an AssistantObject from the request data
    assistant = AssistantObject(
        assistant_id=assistant_id,
        object="assistant",
        created_at=int(datetime.now().timestamp()),
        name=body.name or "",
        description=body.description or "",
        model=body.model,
        instructions=body.instructions or "",
        tools=body.tools or [],
        file_ids=body.file_ids or [],
        metadata=body.metadata or {},
    )

    # Save the assistant to MongoDB
    await assistant.insert()

    for file_id in assistant.file_ids:
        await _create_assistant_file(assistant_id=assistant_id, file_id=file_id)

    return assistant


@app.get("/assistants", response_model=ListAssistantsResponse, tags=["Assistants"])
async def list_assistants(
    limit: Optional[int] = 20,
    order: Optional[Order1] = "desc",
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> ListAssistantsResponse:
    """
    Returns a list of assistants.
    """
    query = {}

    # Apply 'after' and 'before' filters
    if after:
        query["assistant_id"] = {"$gt": after}
    if before:
        query["assistant_id"] = {"$lt": before}

    # Define sorting order
    sort_order = DESCENDING if order == "desc" else ASCENDING

    # Prepare the query for assistants
    find_query = AssistantObject.find(query).sort([("assistant_id", sort_order)])

    # Retrieve assistants from MongoDB
    assistants = await find_query.to_list(limit)

    # Check if there are more results
    total_count = await find_query.count()
    has_more = len(assistants) < total_count

    # Prepare the response
    list_response = ListAssistantsResponse(
        object="list",
        data=assistants,
        first_id=assistants[0].assistant_id if assistants else "",
        last_id=assistants[-1].assistant_id if assistants else "",
        has_more=has_more,
    )

    return list_response


@app.get(
    "/assistants/{assistant_id}", response_model=AssistantObject, tags=["Assistants"]
)
async def get_assistant(assistant_id: str) -> AssistantObject:
    """
    Retrieves an assistant.
    """
    # Query the MongoDB database for the assistant using the 'id' field
    assistant = await AssistantObject.find_one({"id": assistant_id})

    # Check if the assistant data was found
    if not assistant:
        raise HTTPException(
            status_code=404, detail=f"Assistant with ID '{assistant_id}' not found"
        )

    return assistant


@app.post(
    "/assistants/{assistant_id}", response_model=AssistantObject, tags=["Assistants"]
)
async def modify_assistant(
    assistant_id: str, body: ModifyAssistantRequest
) -> AssistantObject:
    """
    Modifies an assistant.
    """
    # Query the MongoDB database for the assistant using the 'id' field
    existing_assistant = await AssistantObject.find_one({"id": assistant_id})

    # Check if the assistant exists
    if not existing_assistant:
        raise HTTPException(
            status_code=404, detail=f"Assistant with ID '{assistant_id}' not found"
        )

    # Update the assistant object with new data from the request
    existing_assistant.model = body.model if body.model else existing_assistant.model
    existing_assistant.instructions = body.instructions if body.instructions else existing_assistant.instructions
    existing_assistant.description = body.description if body.description else existing_assistant.description
    
    existing_assistant.metadata = body.metadata if body.metadata else existing_assistant.metadata
    existing_assistant.name = body.name if body.name else existing_assistant.name
    existing_assistant.tools = body.tools if body.tools else existing_assistant.tools

    # TODO: take care of assistant file creation and deletion.
    existing_assistant.file_ids = body.file_ids if body.file_ids else existing_assistant.file_ids

    # Save the updated assistant to MongoDB
    await existing_assistant.save()

    return existing_assistant


@app.delete(
    "/assistants/{assistant_id}",
    response_model=DeleteAssistantResponse,
    tags=["Assistants"],
)
async def delete_assistant(assistant_id: str) -> DeleteAssistantResponse:
    """
    Delete an assistant.
    """
    # Query the MongoDB database for the assistant using the 'id' field
    existing_assistant = await AssistantObject.find_one({"id": assistant_id})

    # Check if the assistant exists
    if not existing_assistant:
        raise HTTPException(
            status_code=404, detail=f"Assistant with ID '{assistant_id}' not found"
        )

    # Delete assistant files
    if existing_assistant.file_ids:
        # Local
        from app.vector_db.milvus.main import drop_collection
        
        for file_id in existing_assistant.file_ids:
            try:
                existing_assistant_file = await AssistantFileObject.find_one(
                    {"id": file_id, "assistant_id": assistant_id}
                )
                if existing_assistant_file:
                    await existing_assistant_file.delete()
                    logging.info(f"assistant file {file_id} for assistant {assistant_id} deleted")
                else:
                    logging.warning(
                        f"assistant file {file_id} for assistant {assistant_id} not found"
                    )
            except Exception as e:
                logging.error(f"Error in deleting assistant file {file_id}: {e}")
        
        try:
            drop_collection(assistant_id)
        except Exception as e:
            logging.error(f"Error in dropping asst {assistant_id}'s file vector db collection: {e}")

    # Delete the assistant from MongoDB
    await existing_assistant.delete()

    # Return response indicating successful deletion
    return DeleteAssistantResponse(
        id=assistant_id, deleted=True, object=Object21.assistant_deleted
    )


@app.post("/threads", response_model=ThreadObject, tags=["Assistants"])
async def create_thread(body: CreateThreadRequest = None) -> ThreadObject:
    """
    Create a thread.
    """
    # Generate a unique ID for the thread with the specified format
    thread_id = generate_thread_id()

    # Create MessageObjects from the provided messages
    messages = []
    if body and body.messages:
        for msg_request in body.messages:
            # Convert Role8 to Role7 if valid
            if msg_request.role.value in Role7.__members__:
                role = Role7(msg_request.role.value)
            else:
                raise HTTPException(
                    status_code=400, detail=f"Invalid role: {msg_request.role}"
                )

            # Create a MessageObject
            message_id = generate_message_id()
            message = MessageObject(
                message_id=message_id,
                object=Object25.thread_message,
                created_at=int(datetime.now().timestamp()),
                thread_id=thread_id,
                role=role,
                content=[
                    MessageContentTextObject(
                        type=Type13.text,
                        text=Text(value=msg_request.content, annotations=[]),
                    )
                ],  # TODO need to address MessageContentImageFileObject
                file_ids=msg_request.file_ids if msg_request.file_ids else [],
                metadata=msg_request.metadata if msg_request.metadata else {},
                assistant_id="",
                run_id="",
            )
            messages.append(message)

    # Create a ThreadObject
    thread = ThreadObject(
        thread_id=thread_id,
        object=Object23.thread,
        created_at=int(datetime.now().timestamp()),
        metadata=body.metadata if body and body.metadata else {},
    )

    await thread.insert()
    tasks = []
    for msg in messages:
        tasks.append(msg.insert())
    await asyncio.gather(*tasks)

    return thread


@app.get("/threads/{thread_id}", response_model=ThreadObject, tags=["Assistants"])
async def get_thread(thread_id: str) -> ThreadObject:
    """
    Retrieves a thread.
    """
    # Query the MongoDB database for the thread using the 'thread_id' field
    thread = await ThreadObject.find_one({"id": thread_id})

    # Check if the thread was found
    if not thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    return thread


@app.post("/threads/{thread_id}", response_model=ThreadObject, tags=["Assistants"])
async def modify_thread(thread_id: str, body: ModifyThreadRequest) -> ThreadObject:
    """
    Modifies a thread.
    """
    # Fetch the existing thread data from MongoDB
    existing_thread = await ThreadObject.find_one({"id": thread_id})

    # Check if the thread exists
    if not existing_thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    # Update the thread metadata by merging it with new data from the request
    if body.metadata is not None:
        existing_thread.metadata = existing_thread.metadata or {}
        existing_thread.metadata.update(body.metadata)

    # Save the updated thread back in MongoDB
    await existing_thread.save()

    return existing_thread


@app.delete(
    "/threads/{thread_id}", response_model=DeleteThreadResponse, tags=["Assistants"]
)
async def delete_thread(thread_id: str) -> DeleteThreadResponse:
    """
    Delete a thread.
    """
    # Check if the thread exists in MongoDB
    existing_thread = await ThreadObject.find_one({"id": thread_id})

    # If the thread does not exist, raise an HTTP 404 error
    if not existing_thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    # Delete the thread from MongoDB
    await existing_thread.delete()

    # Return response indicating successful deletion
    return DeleteThreadResponse(
        id=thread_id, deleted=True, object=Object24.thread_deleted
    )


@app.post(
    "/threads/{thread_id}/messages", response_model=MessageObject, tags=["Assistants"]
)
async def create_message(thread_id: str, body: CreateMessageRequest) -> MessageObject:
    """
    Create a message in a thread.
    """
    # Generate a unique ID for the message
    message_id = generate_message_id()

    # Ensure the thread exists
    thread = await ThreadObject.find_one({"id": thread_id})
    if not thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    # Convert the content string to a MessageContentTextObject
    content = MessageContentTextObject(
        type=Type13.text,  # Since we are dealing with only text content
        text=Text(value=body.content, annotations=[]),
    )

    # Create a MessageObject with the text content
    message = MessageObject(
        message_id=message_id,
        object=Object25.thread_message,  # Replace with the correct enum or object for 'thread.message'
        created_at=int(datetime.now().timestamp()),
        thread_id=thread_id,
        role=Role7(body.role.value),  # Convert Role8 to Role7 if required and valid
        content=[content],  # List containing the text content object
        assistant_id="",  # Populate if applicable
        run_id="",  # Populate if applicable
        file_ids=body.file_ids or [],
        metadata=body.metadata or {},
    )

    # Insert the message into MongoDB
    await message.insert()

    return message


@app.get(
    "/threads/{thread_id}/messages/{message_id}",
    response_model=MessageObject,
    tags=["Assistants"],
)
async def get_message(thread_id: str, message_id: str) -> MessageObject:
    """
    Retrieve a message from a thread.
    """
    # Check if the thread exists
    thread = await ThreadObject.find_one({"id": thread_id})
    if not thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    # Query the MongoDB database for the message using 'message_id' and 'thread_id'
    message = await MessageObject.find_one({"id": message_id, "thread_id": thread_id})

    # Check if the message was found
    if not message:
        raise HTTPException(
            status_code=404,
            detail=f"Message with ID '{message_id}' in thread '{thread_id}' not found",
        )

    return message


@app.post(
    "/threads/{thread_id}/messages/{message_id}",
    response_model=MessageObject,
    tags=["Assistants"],
)
async def modify_message(
    thread_id: str, message_id: str, body: ModifyMessageRequest
) -> MessageObject:
    """
    Modifies a message within a thread.
    """
    # Check if the thread exists
    thread = await ThreadObject.find_one({"id": thread_id})
    if not thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    # Query the MongoDB database for the message using 'message_id' and 'thread_id'
    message = await MessageObject.find_one({"id": message_id, "thread_id": thread_id})

    # Check if the message was found
    if not message:
        raise HTTPException(
            status_code=404,
            detail=f"Message with ID '{message_id}' in thread '{thread_id}' not found",
        )

    # Update the message metadata by merging it with new data from the request
    if body.metadata is not None:
        message.metadata = message.metadata or {}
        message.metadata.update(body.metadata)

    # Save the updated message back in MongoDB
    await message.save()

    return message


@app.get(
    "/threads/{thread_id}/messages",
    response_model=ListMessagesResponse,
    tags=["Assistants"],
)
async def list_messages(
    thread_id: str,
    limit: Optional[int] = 20,
    order: Optional[Order3] = "desc",
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> ListMessagesResponse:
    """
    Returns a list of messages for a given thread.
    """
    # Check if the thread exists
    thread = await ThreadObject.find_one({"id": thread_id})
    if not thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    # Define sorting order
    sort_order = DESCENDING if order == "desc" else ASCENDING

    # Prepare the query for messages
    query = {"thread_id": thread_id}
    if after:
        query["message_id"] = {"$gt": after}
    if before:
        query["message_id"] = {"$lt": before}

    # Retrieve messages from MongoDB
    find_query = MessageObject.find(query).sort([("created_at", sort_order)])
    messages = await find_query.to_list(limit)

    # Check if there are more results
    total_count = await find_query.count()
    has_more = len(messages) < total_count

    # Prepare the response
    list_response = ListMessagesResponse(
        object="list",
        data=messages,
        first_id=messages[0].message_id if messages else None,
        last_id=messages[-1].message_id if messages else None,
        has_more=has_more,
    )

    return list_response


async def redis_subscriber(channel, timeout=1):
    logging.info(f"Connecting to Redis and subscribing to channel: {channel}")
    redis = await aioredis.from_url(
        f"redis://{redis_host}:6379/0", encoding="utf-8", decode_responses=True
    )
    pubsub = redis.pubsub()
    await pubsub.subscribe(channel)

    while True:
        try:
            message = await asyncio.wait_for(
                pubsub.get_message(ignore_subscribe_messages=True), timeout=timeout
            )
            if message and message["type"] == "message":
                yield message["data"]
            else:
                yield None  # Yield None if no message is received
        except asyncio.TimeoutError:
            yield None  # Yield None on timeout

    logging.info(f"Unsubscribing from Redis channel: {channel}")
    await pubsub.unsubscribe(channel)
    await redis.close()


async def listen_for_task_status(
    task_status_channel, status_update_event, thread_id, run_id
):
    logging.info(f"Listening for task status on channel: {task_status_channel}")
    redis = None
    pubsub = None
    try:
        redis = await aioredis.from_url(
            f"redis://{redis_host}:6379/0", encoding="utf-8", decode_responses=True
        )
        pubsub = redis.pubsub()
        await pubsub.subscribe(task_status_channel)

        while True:
            message = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            if message:
                if message["type"] == "message":
                    task_status = json.loads(message["data"])
                    if (
                        task_status["thread_id"] == thread_id
                        and task_status["run_id"] == run_id
                    ):
                        logging.info(f"Received task status update: {task_status}")
                        status_update_event.set()
                        break
            await asyncio.sleep(0.1)  # Prevents the loop from being blocking
    except Exception as e:
        logging.error(f"Error in listen_for_task_status: {e}")
    finally:
        if pubsub:
            await pubsub.unsubscribe(task_status_channel)
            await pubsub.close()
        if redis:
            await redis.close()


@app.websocket("/ws/{thread_id}/{run_id}")
async def websocket_endpoint(websocket: WebSocket, thread_id: str, run_id: str):
    await websocket.accept()
    logging.info(f"WebSocket connection opened for thread {thread_id}, run {run_id}")
    status_update_event = asyncio.Event()
    channel = f"task_status_{thread_id}"
    asyncio.create_task(
        listen_for_task_status(channel, status_update_event, thread_id, run_id)
    )
    try:
        await send_messages_to_websocket(
            websocket, thread_id, run_id, status_update_event
        )
    except WebSocketDisconnect:
        logging.info(f"WebSocket disconnected on thread {thread_id}, run {run_id}")
    except Exception as e:
        logging.error(f"WebSocket error on thread {thread_id}, run {run_id}: {e}")
    finally:
        await websocket.close()
        logging.info(f"WebSocket for thread {thread_id}, run {run_id} closed")


async def send_messages_to_websocket(
    websocket: WebSocket, thread_id: str, run_id: str, status_update_event
):
    logging.info(f"Sending messages to WebSocket for thread {thread_id}, run {run_id}")
    while not status_update_event.is_set():
        async for message in redis_subscriber(thread_id):
            if message is None:  # Check if message is None and continue if it is
                if status_update_event.is_set():
                    logging.info("Status update event set, breaking loop")
                    break
                continue

            if websocket.client_state == WebSocketState.DISCONNECTED:
                logging.info("Client disconnected websocket")
                return  # Exit the function as the client is disconnected
            await websocket.send_text(message)

    logging.info("Closing connection as task is completed or failed")
    await websocket.send_text("CLOSE_CONNECTION")


@app.post("/threads/{thread_id}/runs", response_model=RunObject, tags=["Assistants"])
async def create_run(thread_id: str, body: CreateRunRequest) -> RunObject:
    """
    Create a run.
    """
    # Generate a unique ID for the run
    run_id = generate_run_id()

    # Ensure the thread exists
    thread = await ThreadObject.find_one({"id": thread_id})
    if not thread:
        raise HTTPException(
            status_code=404, detail=f"Thread with ID '{thread_id}' not found"
        )

    # Fetch the assistant details
    assistant = await AssistantObject.find_one({"id": body.assistant_id})
    if not assistant:
        raise HTTPException(
            status_code=404, detail=f"Assistant with ID '{body.assistant_id}' not found"
        )

    # Use tools and file_ids from the assistant, or default if not present
    tools = assistant.tools or []
    file_ids = assistant.file_ids or []

    # Create a RunObject with the provided data and default values
    run = RunObject(
        run_id=run_id,
        object=Object22.thread_run,
        created_at=int(datetime.now().timestamp()),
        thread_id=thread_id,
        assistant_id=body.assistant_id,
        status=Status2.queued,  # Default status to 'queued'
        required_action=None,
        last_error=None,
        expires_at=None,  # Set if applicable
        started_at=None,  # Set when the run starts
        cancelled_at=None,
        failed_at=None,
        completed_at=None,  # Set when the run completes
        model=body.model
        or assistant.model,  # Use the model from the request or assistant
        instructions=body.instructions or assistant.instructions,
        tools=tools,
        file_ids=file_ids,
        metadata=body.metadata or {},
    )

    logging.info(run)

    # Insert the run into MongoDB
    await run.insert()

    # Dispatch the task and set initial run status to 'queued'
    redis_channel = f"{thread_id}"
    celery_app.send_task(
        "app.tasks.execute_chat_completion",
        args=[body.assistant_id, thread_id, redis_channel, run_id],
    )

    await run.save()

    return run


@app.get(
    "/threads/{thread_id}/runs/{run_id}", response_model=RunObject, tags=["Assistants"]
)
async def get_run(thread_id: str, run_id: str) -> RunObject:
    """
    Retrieves a run associated with a given thread.
    """
    # Query the MongoDB database for the run using 'run_id' and 'thread_id'
    run = await RunObject.find_one({"id": run_id, "thread_id": thread_id})

    # Check if the run was found
    if not run:
        raise HTTPException(
            status_code=404,
            detail=f"Run with ID '{run_id}' in thread '{thread_id}' not found",
        )

    return run


@app.post(
    "/threads/{thread_id}/runs/{run_id}", response_model=RunObject, tags=["Assistants"]
)
async def modify_run(thread_id: str, run_id: str, body: ModifyRunRequest) -> RunObject:
    """
    Modifies a run.
    """
    # Query the MongoDB database for the run using 'run_id' and 'thread_id'
    existing_run = await RunObject.find_one({"id": run_id, "thread_id": thread_id})

    # Check if the run exists
    if not existing_run:
        raise HTTPException(
            status_code=404,
            detail=f"Run with ID '{run_id}' in thread '{thread_id}' not found",
        )

    # Update the run object with new metadata from the request
    if body.metadata is not None:
        existing_run.metadata = existing_run.metadata or {}
        existing_run.metadata.update(body.metadata)

    # Save the updated run to MongoDB
    await existing_run.save()

    return existing_run


def convert_to_model(obj):
    return Model(
        id=obj.id, created=obj.created, object=obj.object, owned_by=obj.owned_by
    )


def find_provider(obj):
    if obj["litellm_params"]:
        if "custom_llm_provider" in obj["litellm_params"]:
            return obj["litellm_params"]["custom_llm_provider"]
        else:
            logging.info(
                "Cannot find custom_llm_provider field. Trying to extract from model name"
            )
            return obj["litellm_params"]["model"].split("/")[0]
    logging.info(obj)
    return "rubra"


def convert_model_info_to_oai_model(obj, predefined_models):
    if obj["model_info"]:
        if "created" in obj["model_info"]:
            return Model(
                id=obj["model_name"],
                created=obj["model_info"]["created"],
                object="model",
                owned_by=find_provider(obj),
            )
        else:
            logging.info("Cannot find created field")
            logging.info(obj)
            return Model(
                id=obj["model_name"],
                created=0,
                object="model",
                owned_by=find_provider(obj),
            )
    else:
        # predefined model
        created_at = -1
        for m in predefined_models:
            if m.id == obj["model_name"]:
                created_at = m.created
                break
        return Model(
            id=obj["model_name"],
            created=created_at,
            object="model",
            owned_by=find_provider(obj),
        )


def litellm_list_model() -> ListModelsResponse:
    try:
        client = OpenAI(base_url=LITELLM_URL, api_key="abc")
        models_data = client.models.list().data
        models_data = sorted(models_data, key=lambda x: x.id)
        predefined_models = [convert_to_model(m) for m in models_data]

        models_data = requests.get(f"{LITELLM_URL}/model/info").json().get("data", [])
        models = [
            convert_model_info_to_oai_model(m, predefined_models) for m in models_data
        ]
        return ListModelsResponse(object=Object.list, data=models)

    except Exception as e:
        logging.error(str(e))
        return ListModelsResponse(object=Object.list, data=[])


@app.get("/models", response_model=ListModelsResponse, tags=["Models"])
def list_models() -> ListModelsResponse:
    return litellm_list_model()


@app.get("/models/info", tags=["Models"])
def get_models_info():
    model_info_url = f"{LITELLM_URL}/model/info"
    response = requests.get(model_info_url)
    if response.status_code == 200:
        return response.json()
    return []


class ModelInfo(BaseModel):
    id: str
    created: int


class AddModel(BaseModel):
    model_name: str
    litellm_params: Dict[
        str, Any
    ]  # Assuming litellm_params is a dictionary with unspecified structure
    model_info: ModelInfo


@app.post("/models/new", tags=["Models"])
def add_model(add_model: AddModel):
    data = add_model.dict()
    print(data)
    response = requests.post(f"{LITELLM_URL}/model/new", json=data, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []


class ModelID(BaseModel):
    id: str


@app.post("/models/delete", tags=["Models"])
def delete_model(model_id: ModelID):
    model_info_url = f"{LITELLM_URL}/model/delete"
    response = requests.post(model_info_url, json=model_id.dict(), headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []


class EnvironmentVariablesModel(BaseModel):
    environment_variables: Dict[str, str]


@app.post("/config/update", tags=["Models"])
def update_key(data: EnvironmentVariablesModel):
    model_info_url = f"{LITELLM_URL}/config/update"
    data = data.dict()
    response = requests.post(model_info_url, json=data, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    return []


### APIs for file upload
@app.get("/files", response_model=ListFilesResponse, tags=["Files"])
async def list_files(purpose: Optional[str] = None) -> ListFilesResponse:
    """
    Returns a list of files that belong to the user's organization.
    """
    if purpose == "":
        purpose = None
    if purpose is not None and purpose not in Purpose1.__members__:
        raise HTTPException(
            status_code=404,
            detail=f"the purpose of the file has to be one of {Purpose1.__members__}",
        )

    search_filter = {}
    if purpose:
        search_filter["purpose"] = purpose

    res_files = OpenAIFile.find(search_filter)
    data = []
    async for f in res_files:
        data.append(f)
    return ListFilesResponse(data=data, object=Object7.list)


@app.post("/files", response_model=OpenAIFile, tags=["Files"])
async def create_file(file: UploadFile, purpose: str = Form(...)) -> OpenAIFile:
    # async def create_file(body: CreateFileRequest) -> OpenAIFile:
    """
        Upload a file that can be used across various endpoints/features. The size of all the files uploaded by one organization can be up to 100 GB.

    The size of individual files for can be a maximum of 512MB. See the [Assistants Tools guide](/docs/assistants/tools) to learn more about the types of files supported. The Fine-tuning API only supports `.jsonl` files.

    Please [contact us](https://help.openai.com/) if you need to increase these storage limits.

    """

    # Standard Library
    from datetime import datetime

    if purpose not in Purpose1.__members__:
        raise HTTPException(
            status_code=404,
            detail=f"the purpose of the file has to be one of {Purpose1.__members__}",
        )

    # Convert to Unix timestamp
    create_time_unix = int(datetime.now().timestamp())
    file_id = f"file_{uuid.uuid4().hex[:6]}"

    # process file # TODO: size limit of a file?

    uploaded_file = OpenAIFile(
        file_id=file_id,
        bytes=file.size,
        created_at=create_time_unix,
        filename=file.filename,
        object=Object14.file,
        purpose=purpose,
        status=Status.uploaded,
    )
    await uploaded_file.insert()
    content = await file.read()

    file_content_object = FilesStorageObject(
        file_id=file_id, content=content, content_type=file.content_type
    )
    await file_content_object.insert()

    return uploaded_file


@app.delete("/files/{file_id}", response_model=DeleteFileResponse, tags=["Files"])
async def delete_file(file_id: str) -> DeleteFileResponse:
    """
    Delete a file.
    """

    existing_file = await OpenAIFile.find_one({"id": file_id})
    existing_file_object = await FilesStorageObject.find_one({"id": file_id})

    # If the file does not exist, raise an HTTP 404 error
    if not existing_file:
        raise HTTPException(
            status_code=404, detail=f"File with ID '{file_id}' not found"
        )

    # Delete the file from MongoDB
    await existing_file.delete()
    await existing_file_object.delete()

    # Return response indicating successful deletion
    return DeleteFileResponse(id=file_id, object=Object8.file, deleted=True)


@app.get("/files/{file_id}", response_model=OpenAIFile, tags=["Files"])
async def retrieve_file(file_id: str) -> OpenAIFile:
    """
    Returns information about a specific file.
    """
    existing_file = await OpenAIFile.find_one({"id": file_id})

    # If the file does not exist, raise an HTTP 404 error
    if not existing_file:
        raise HTTPException(
            status_code=404, detail=f"File with ID '{file_id}' not found"
        )
    return existing_file


@app.get("/files/{file_id}/content", response_model=str, tags=["Files"])
async def download_file(file_id: str) -> str:
    """
    Returns the contents of the specified file.
    """
    existing_file_object = await FilesStorageObject.find_one({"id": file_id})

    # If the file content does not exist, raise an HTTP 404 error
    if not existing_file_object:
        raise HTTPException(
            status_code=404, detail=f"File content with ID '{file_id}' not found"
        )

    encodings = ["utf-8", "ascii", "iso-8859-1", "windows-1252", "utf-16", "utf-32"]
    for encoding in encodings:
        try:
            decoded_content = existing_file_object.content.decode(encoding)
            return decoded_content
        except Exception as e:
            logging.error(f"Decoding content with {encoding} failed: {e}\n")

    raise HTTPException(
        status_code=404, detail=f"Fail to decode content for file: '{file_id}'."
    )


### assistant file


@app.get(
    "/assistants/{assistant_id}/files",
    response_model=ListAssistantFilesResponse,
    tags=["Assistants"],
)
async def list_assistant_files(
    assistant_id: str,
    limit: Optional[int] = 20,
    order: Optional[Order9] = "asce",
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> ListAssistantFilesResponse:
    """
    Returns a list of assistant files.
    """
    existing_assistant = await AssistantObject.find_one({"id": assistant_id})
    if not existing_assistant:
        raise HTTPException(
            status_code=404, detail=f"Assistant with ID '{assistant_id}' not found"
        )

    query = {"assistant_id": assistant_id}

    # Apply 'after' and 'before' filters
    if after:
        query["file_id"] = {"$gt": after}
    if before:
        query["file_id"] = {"$lt": before}

    # Define sorting order
    sort_order = DESCENDING if order == "desc" else ASCENDING

    # Prepare the query for assistant files
    find_query = AssistantFileObject.find(query).sort([("file_id", sort_order)])
    # Retrieve assistant_files from MongoDB
    assistant_files = await find_query.to_list(limit)

    # Check if there are more results
    total_count = await find_query.count()
    has_more = len(assistant_files) < total_count

    # Prepare the response
    list_response = ListAssistantFilesResponse(
        object="list",
        data=assistant_files,
        first_id=assistant_files[0].file_id if assistant_files else "",
        last_id=assistant_files[-1].file_id if assistant_files else "",
        has_more=has_more,
    )

    return list_response


@app.post(
    "/assistants/{assistant_id}/files",
    response_model=AssistantFileObject,
    tags=["Assistants"],
)
async def create_assistant_file(
    assistant_id: str, body: CreateAssistantFileRequest
) -> AssistantFileObject:
    """
    Create an assistant file by attaching a [File](/docs/api-reference/files) to an [assistant](/docs/api-reference/assistants).
    """
    return await _create_assistant_file(assistant_id=assistant_id, file_id=body.file_id)


async def _create_assistant_file(
    assistant_id: str, file_id: str
) -> AssistantFileObject:
    # Local
    from app.tasks import execute_asst_file_create

    # Check if the assistant exists
    existing_assistant = await AssistantObject.find_one({"id": assistant_id})
    if not existing_assistant:
        raise HTTPException(
            status_code=404, detail=f"Assistant with ID '{assistant_id}' not found"
        )

    existing_file = await OpenAIFile.find_one({"id": file_id})

    # If the file does not exist, raise an HTTP 404 error
    if not existing_file:
        raise HTTPException(
            status_code=404, detail=f"File with ID '{file_id}' not found"
        )
    if existing_file.purpose.value != Purpose1.assistants.value:
        raise HTTPException(
            status_code=404,
            detail=f"File with ID '{file_id}' was not uploaded for purpose 'assistants'.",
        )

    existing_assistant_file = await AssistantFileObject.find_one(
        {"id": file_id, "assistant_id": assistant_id}
    )
    if not existing_assistant_file:
        # Create and store the AssistantFileObject
        assistant_file = AssistantFileObject(
            file_id=file_id,
            object=Object28.assistant_file,
            created_at=int(datetime.now().timestamp()),
            assistant_id=assistant_id,
        )

        await assistant_file.insert()

        # celery task
        execute_asst_file_create.delay(file_id=file_id, assistant_id=assistant_id)

        # Update the assistant's file_ids list and store the updated assistant

        if file_id not in existing_assistant.file_ids:
            existing_assistant.file_ids.append(file_id)
        for d in existing_assistant.tools:
            if d.type.value == Type8.retrieval.value:
                break
        else:  # if no `retrieval` tool in tools yet, add it
            existing_assistant.tools.append(
                AssistantToolsRetrieval(type=Type8.retrieval)
            )

        await existing_assistant.save()
        return assistant_file

    else:
        raise HTTPException(
            status_code=404,
            detail=f"File {file_id} has already been attached to assistant {assistant_id}",
        )


@app.get(
    "/assistants/{assistant_id}/files/{file_id}",
    response_model=AssistantFileObject,
    tags=["Assistants"],
)
async def get_assistant_file(
    assistant_id: str, file_id: str = ...
) -> AssistantFileObject:
    """
    Retrieves an AssistantFile.
    """
    existing_assistant_file = await AssistantFileObject.find_one(
        {"id": file_id, "assistant_id": assistant_id}
    )
    if not existing_assistant_file:
        raise HTTPException(
            status_code=404,
            detail=f"Assistant_file with ID '{file_id}' of assistant {assistant_id} not found",
        )

    return existing_assistant_file


@app.delete(
    "/assistants/{assistant_id}/files/{file_id}",
    response_model=DeleteAssistantFileResponse,
    tags=["Assistants"],
)
async def delete_assistant_file(
    assistant_id: str, file_id: str = ...
) -> DeleteAssistantFileResponse:
    """
    Delete an assistant file.
    """
    return await _delete_assistant_file(assistant_id=assistant_id, file_id=file_id)


async def _delete_assistant_file(
    assistant_id: str, file_id: str
) -> DeleteAssistantFileResponse:
    # Local
    from app.vector_db.milvus.main import delete_docs

    existing_assistant = await AssistantObject.find_one({"id": assistant_id})
    if not existing_assistant:
        raise HTTPException(
            status_code=404, detail=f"Assistant with ID '{assistant_id}' not found"
        )

    existing_assistant_file = await AssistantFileObject.find_one(
        {"id": file_id, "assistant_id": assistant_id}
    )
    if not existing_assistant_file:
        raise HTTPException(
            status_code=404,
            detail=f"Assistant_file with ID '{file_id}' of assistant {assistant_id} not found",
        )

    await existing_assistant_file.delete()

    existing_assistant.file_ids = [
        x for x in existing_assistant.file_ids if x != file_id
    ]
    if len(existing_assistant.file_ids) == 0:
        existing_assistant.tools = [
            x for x in existing_assistant.tools if x.type.value != Type8.retrieval.value
        ]
    await existing_assistant.save()
    # await existing_assistant.update({"$set": {"file_ids": cleaned_file_ids}})

    expr = f"file_id == '{file_id}'"
    delete_docs(collection_name=assistant_id, expr=expr)

    # Return response indicating successful deletion
    return DeleteAssistantFileResponse(
        id=file_id,
        deleted=True,
        object=Object29.assistant_file_deleted,
    )


@app.get(
    "/threads/{thread_id}/runs/{run_id}/steps",
    response_model=ListRunStepsResponse,
    tags=["Assistants"],
)
async def list_run_steps(
    thread_id: str,
    run_id: str = ...,
    limit: Optional[int] = 20,
    order: Optional[Order7] = "desc",
    after: Optional[str] = None,
    before: Optional[str] = None,
) -> ListRunStepsResponse:
    """
    Returns a list of run steps belonging to a run.
    """
    existing_run = await RunObject.find_one({"run_id": run_id})
    if not existing_run:
        raise HTTPException(status_code=404, detail=f"Run with ID '{run_id}' not found")

    query = {"thread_id": thread_id, "run_id": run_id}

    # Apply 'after' and 'before' filters
    if after:
        query["run_step_id"] = {"$gt": after}
    if before:
        query["run_step_id"] = {"$lt": before}

    # Define sorting order
    sort_order = DESCENDING if order == "desc" else ASCENDING

    # Prepare the query
    find_query = RunStepObject.find(query).sort([("run_step_id", sort_order)])
    # Retrieve  from MongoDB
    run_steps = await find_query.to_list(limit)

    # Check if there are more results
    total_count = await find_query.count()
    has_more = len(run_steps) < total_count

    # Prepare the response
    list_response = ListRunStepsResponse(
        object="list",
        data=run_steps,
        first_id=run_steps[0].run_step_id if run_steps else "",
        last_id=run_steps[-1].run_step_id if run_steps else "",
        has_more=has_more,
    )

    return list_response


@app.get(
    "/threads/{thread_id}/runs/{run_id}/steps/{step_id}",
    response_model=RunStepObject,
    tags=["Assistants"],
)
async def get_run_step(
    thread_id: str, run_id: str = ..., step_id: str = ...
) -> RunStepObject:
    """
    Retrieves a run step.
    """
    existing_run_step = await RunStepObject.find_one(
        {"thread_id": thread_id, "run_id": run_id, "id": step_id}
    )
    if not existing_run_step:
        raise HTTPException(
            status_code=404,
            detail=f"Run_step with ID '{step_id}' of run {run_id} of thread {thread_id} not found",
        )

    return existing_run_step


@app.post(
    "/v1/chat/completions",
    tags=["chat/completions"],
)
@app.post(
    "/chat/completions",
    tags=["chat/completions"],
)
async def chat_completion(body: CreateChatCompletionRequest):
    client = OpenAI(base_url=LITELLM_URL, api_key="abc")
    chat_messages = [
        {"role": m.__root__.role.value, "content": m.__root__.content}
        for m in body.messages
    ]
    response_format = body.response_format
    if body.response_format and body.response_format.type:
        if body.response_format.type == Type6.json_object:
            response_format = {"type": "json_object"}
        elif body.response_format.type == Type6.text:
            response_format = {"type": "text"}

    if type(body.max_tokens) != int:
        max_tokens = 128000
    else:
        max_tokens = body.max_tokens

    print(body)
    response = client.chat.completions.create(
        model=body.model,
        messages=chat_messages,
        temperature=body.temperature,
        top_p=body.top_p,
        stream=body.stream,
        response_format=response_format,
        frequency_penalty=body.frequency_penalty,
        logit_bias=body.logit_bias,
        max_tokens=max_tokens,
        n=body.n,
        presence_penalty=body.presence_penalty,
        seed=body.seed,
        stop=body.stop,
        tool_choice=body.tool_choice,
        tools=body.tools,
        user=body.user,
        function_call=body.function_call,
        functions=body.functions,
    )

    if body.stream:
        return StreamingResponse(
            data_generator(response), media_type="text/event-stream"
        )
    else:
        return response


def data_generator(response):
    """
    Format data in Server-Sent Event (SSE) messages, which OpenAI Stream API consumes.
    https://github.com/florimondmanca/httpx-sse/blob/master/src/httpx_sse/_decoders.py
    """
    try:
        for chunk in response:
            try:
                yield f"data: {json.dumps(chunk.dict())}\n\n"
            except Exception as e:
                yield f"data: {str(e)}\n\n"

        # Streaming is done, yield the [DONE] chunk
        done_message = "[DONE]"
        yield f"data: {done_message}\n\n"
    except Exception as e:
        yield f"data: {str(e)}\n\n"
