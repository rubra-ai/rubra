# backend_models.py
from beanie import Document
from pydantic import (
    AnyUrl,
    BaseModel,
    Extra,
    Field,
    PositiveFloat,
    confloat,
    conint,
    constr,
)
from typing import Any, Dict, List, Optional, Union
from .models import (
    AssistantFileObject,
    AssistantToolsFunction,
    CreateAssistantRequest,
    FineTuningJob,
    ImagesResponse,
    LastError,
    ListAssistantFilesResponse,
    ListFilesResponse,
    ListFineTuneEventsResponse,
    Object7,
    Object14,
    Purpose1,
    Status,
    Object20,
    Object21,
    Object22,
    Object23,
    Object24,
    Object25,
    Object27,
    Object28,
    RequiredAction,
    Role7,
    Role8,
    Type16,
    Status2,
    Status3,
    LastError1,
    MessageContentTextObject,
    MessageContentImageFileObject,
    RunStepDetailsMessageCreationObject, 
    RunStepDetailsToolCallsObject,
    AssistantToolsCode,
    AssistantToolsRetrieval,
    AssistantToolsFunction,
    AssistantToolsBrowser
)

class AssistantObject(Document):
    assistant_id: str = Field(
        ..., description="The identifier, which can be referenced in API endpoints.", alias="id"
    )
    object: Object20 = Field(
        ..., description="The object type, which is always `assistant`."
    )
    created_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the assistant was created.",
    )
    name: constr(max_length=256) = Field(
        ...,
        description="The name of the assistant. The maximum length is 256 characters.\n",
    )
    description: constr(max_length=512) = Field(
        ...,
        description="The description of the assistant. The maximum length is 512 characters.\n",
    )
    model: str = Field(
        ...,
        description="ID of the model to use. You can use the [List models](/docs/api-reference/models/list) API to see all of your available models, or see our [Model overview](/docs/models/overview) for descriptions of them.\n",
    )
    instructions: constr(max_length=32768) = Field(
        ...,
        description="The system instructions that the assistant uses. The maximum length is 32768 characters.\n",
    )
    tools: List[
        Union[AssistantToolsCode, AssistantToolsRetrieval, AssistantToolsFunction, AssistantToolsBrowser]
    ] = Field(
        ...,
        description="A list of tool enabled on the assistant. There can be a maximum of 128 tools per assistant. Tools can be of types `code_interpreter`, `retrieval`, or `function`.\n",
        max_items=128,
    )
    file_ids: List[str] = Field(
        ...,
        description="A list of [file](/docs/api-reference/files) IDs attached to this assistant. There can be a maximum of 20 files attached to the assistant. Files are ordered by their creation date in ascending order.\n",
        max_items=20,
    )
    metadata: Dict[str, Any] = Field(
        ...,
        description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.\n",
    )

    class Settings:
        name = "assistants"

class ListAssistantsResponse(BaseModel):
    object: str = Field(..., example="list")
    data: List[AssistantObject]
    first_id: str = Field(..., example="asst_hLBK7PXBv5Lr2NQT7KLY0ag1")
    last_id: str = Field(..., example="asst_QLoItBbqwyAJEzlTy4y9kOMM")
    has_more: bool = Field(..., example=False)

class ThreadObject(Document):
    thread_id: str = Field(
        ..., description="The identifier, which can be referenced in API endpoints.", alias="id"
    )
    object: Object23 = Field(
        ..., description="The object type, which is always `thread`."
    )
    created_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the thread was created.",
    )
    metadata: Dict[str, Any] = Field(
        ...,
        description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maximum of 512 characters long."
    )

    class Settings:
        name = "threads"

class MessageObject(Document):
    message_id: str = Field(
        ..., description="The identifier, which can be referenced in API endpoints.", alias="id"
    )
    object: Object25 = Field(
        ..., description="The object type, which is always `thread.message`."
    )
    created_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the message was created.",
    )
    thread_id: str = Field(
        ...,
        description="The [thread](/docs/api-reference/threads) ID that this message belongs to.",
    )
    role: Role7 = Field(
        ...,
        description="The entity that produced the message. One of `user` or `assistant`.",
    )
    content: List[
        Union[MessageContentImageFileObject, MessageContentTextObject]
    ] = Field(
        ..., description="The content of the message in array of text and/or images."
    )
    assistant_id: str = Field(
        ...,
        description="If applicable, the ID of the [assistant](/docs/api-reference/assistants) that authored this message.",
    )
    run_id: str = Field(
        ...,
        description="If applicable, the ID of the [run](/docs/api-reference/runs) associated with the authoring of this message.",
    )
    file_ids: List[str] = Field(
        ...,
        description="A list of [file](/docs/api-reference/files) IDs that the assistant should use. Useful for tools like retrieval and code_interpreter that can access files. A maximum of 10 files can be attached to a message.",
        max_items=10,
    )
    metadata: Dict[str, Any] = Field(
        ...,
        description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.\n",
    )

    class Settings:
        name = "messages"

class ListMessagesResponse(BaseModel):
    object: str = Field(..., example="list")
    data: List[MessageObject]
    first_id: str = Field(..., example="msg_hLBK7PXBv5Lr2NQT7KLY0ag1")
    last_id: str = Field(..., example="msg_QLoItBbqwyAJEzlTy4y9kOMM")
    has_more: bool = Field(..., example=False)

class RunObject(Document):
    run_id: str = Field(
        ..., description="The identifier, which can be referenced in API endpoints.", alias="id"
    )
    object: Object22 = Field(
        ..., description="The object type, which is always `thread.run`."
    )
    created_at: int = Field(
        ..., description="The Unix timestamp (in seconds) for when the run was created."
    )
    thread_id: str = Field(
        ...,
        description="The ID of the [thread](/docs/api-reference/threads) that was executed on as a part of this run.",
    )
    assistant_id: str = Field(
        ...,
        description="The ID of the [assistant](/docs/api-reference/assistants) used for execution of this run.",
    )
    status: Status2 = Field(
        ...,
        description="The status of the run, which can be either `queued`, `in_progress`, `requires_action`, `cancelling`, `cancelled`, `failed`, `completed`, or `expired`.",
    )
    required_action: RequiredAction = Field(
        None,
        description="Details on the action required to continue the run. Will be `null` if no action is required.",
    )
    last_error: LastError = Field(
        None,
        description="The last error associated with this run. Will be `null` if there are no errors.",
    )
    expires_at: int = Field(
        None, description="The Unix timestamp (in seconds) for when the run will expire."
    )
    started_at: int = Field(
        None, description="The Unix timestamp (in seconds) for when the run was started."
    )
    cancelled_at: int = Field(
        None,
        description="The Unix timestamp (in seconds) for when the run was cancelled.",
    )
    failed_at: int = Field(
        None, description="The Unix timestamp (in seconds) for when the run failed."
    )
    completed_at: int = Field(
        None,
        description="The Unix timestamp (in seconds) for when the run was completed.",
    )
    model: str = Field(
        ...,
        description="The model that the [assistant](/docs/api-reference/assistants) used for this run.",
    )
    instructions: str = Field(
        ...,
        description="The instructions that the [assistant](/docs/api-reference/assistants) used for this run.",
    )
    tools: List[
        Union[AssistantToolsCode, AssistantToolsRetrieval, AssistantToolsFunction, AssistantToolsBrowser]
    ] = Field(
        ...,
        description="The list of tools that the [assistant](/docs/api-reference/assistants) used for this run.",
        max_items=20,
    )
    file_ids: List[str] = Field(
        ...,
        description="The list of [File](/docs/api-reference/files) IDs the [assistant](/docs/api-reference/assistants) used for this run.",
    )
    metadata: Dict[str, Any] = Field(
        ...,
        description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.\n",
    )

    class Settings:
        name = "runs"



class OpenAIFile(Document):
    file_id: str = Field(
        ...,
        description="The file identifier, which can be referenced in the API endpoints.", alias="id"
    )
    bytes: int = Field(..., description="The size of the file, in bytes.")
    created_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the file was created.",
    )
    filename: str = Field(..., description="The name of the file.")
    object: Object14 = Field(
        ..., description="The object type, which is always `file`."
    )
    purpose: Purpose1 = Field(
        ...,
        description="The intended purpose of the file. Supported values are `fine-tune`, `fine-tune-results`, `assistants`, and `assistants_output`.",
    )
    status: Status = Field(
        ...,
        description="Deprecated. The current status of the file, which can be either `uploaded`, `processed`, or `error`.",
    )
    status_details: Optional[str] = Field(
        None,
        description="Deprecated. For details on why a fine-tuning training file failed validation, see the `error` field on `fine_tuning.job`.",
    )
    
    class Settings:
        name = "files"

class ListFilesResponse(BaseModel):
    data: List[OpenAIFile]
    object: Object7

class FilesStorageObject(Document):
    file_id: str = Field(
        ...,
        description="The file identifier, which can be referenced in the API endpoints.", alias="id"
    )
    content: bytes = Field(..., description="The file content")
    content_type: str = Field(..., description="The file content type")
    
    class Settings:
        name = "files_storage"


class AssistantFileObject(Document):
    file_id: str = Field(
        ..., description="The identifier, which can be referenced in API endpoints." , alias="id"
    )
    object: Object28 = Field(
        ..., description="The object type, which is always `assistant.file`."
    )
    created_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the assistant file was created.",
    )
    assistant_id: str = Field(
        ..., description="The assistant ID that the file is attached to."
    )
    
    class Settings:
        name = "assistant_files"


class ListAssistantFilesResponse(BaseModel):
    object: str = Field(..., example="list")
    data: List[AssistantFileObject]
    first_id: str = Field(..., example="file-hLBK7PXBv5Lr2NQT7KLY0ag1")
    last_id: str = Field(..., example="file-QLoItBbqwyAJEzlTy4y9kOMM")
    has_more: bool = Field(..., example=False)
    

class RunStepObject(Document):
    run_step_id: str = Field(
        ...,
        description="The identifier of the run step, which can be referenced in API endpoints.", alias="id"
    )
    object: Object27 = Field(
        ..., description="The object type, which is always `thread.run.step``."
    )
    created_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the run step was created.",
    )
    assistant_id: str = Field(
        ...,
        description="The ID of the [assistant](/docs/api-reference/assistants) associated with the run step.",
    )
    thread_id: str = Field(
        ...,
        description="The ID of the [thread](/docs/api-reference/threads) that was run.",
    )
    run_id: str = Field(
        ...,
        description="The ID of the [run](/docs/api-reference/runs) that this run step is a part of.",
    )
    type: Type16 = Field(
        ...,
        description="The type of run step, which can be either `message_creation` or `tool_calls`.",
    )
    status: Status3 = Field(
        ...,
        description="The status of the run step, which can be either `in_progress`, `cancelled`, `failed`, `completed`, or `expired`.",
    )
    step_details: Union[
        RunStepDetailsMessageCreationObject, RunStepDetailsToolCallsObject
    ] = Field(..., description="The details of the run step.")
    last_error: LastError1 = Field(
        ...,
        description="The last error associated with this run step. Will be `null` if there are no errors.",
    )
    expired_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the run step expired. A step is considered expired if the parent run is expired.",
    )
    cancelled_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the run step was cancelled.",
    )
    failed_at: int = Field(
        ..., description="The Unix timestamp (in seconds) for when the run step failed."
    )
    completed_at: int = Field(
        ...,
        description="The Unix timestamp (in seconds) for when the run step completed.",
    )
    metadata: Dict[str, Any] = Field(
        ...,
        description="Set of 16 key-value pairs that can be attached to an object. This can be useful for storing additional information about the object in a structured format. Keys can be a maximum of 64 characters long and values can be a maxium of 512 characters long.\n",
    )
    class Settings:
        name = "run_steps"


class ListRunStepsResponse(BaseModel):
    object: str = Field(..., example="list")
    data: List[RunStepObject]
    first_id: str = Field(..., example="step_hLBK7PXBv5Lr2NQT7KLY0ag1")
    last_id: str = Field(..., example="step_QLoItBbqwyAJEzlTy4y9kOMM")
    has_more: bool = Field(..., example=False)
    
    
class ListRunsResponse(BaseModel):
    object: str = Field(..., example="list")
    data: List[RunObject]
    first_id: str = Field(..., example="run_hLBK7PXBv5Lr2NQT7KLY0ag1")
    last_id: str = Field(..., example="run_QLoItBbqwyAJEzlTy4y9kOMM")
    has_more: bool = Field(..., example=False)
    

class FileUpload(BaseModel):
    purpose: str

class ApiKeysUpdateModel(BaseModel):
    OPENAI_API_KEY: Optional[bool] = None
    ANTHROPIC_API_KEY: Optional[bool] = None
