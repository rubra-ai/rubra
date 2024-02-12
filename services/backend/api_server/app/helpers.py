# Standard Library
import uuid


def generate_assistant_id():
    # Generate a unique ID and convert it to a string
    unique_id = uuid.uuid4()
    # Attach the prefix 'asst_' to the ID
    assistant_id = f"asst_{unique_id.hex[:6]}"
    return assistant_id


def generate_thread_id():
    # Generate a unique ID and convert it to a string
    thread_id = f"thread_{uuid.uuid4().hex[:6]}"
    return thread_id


def generate_message_id():
    # Generate a unique ID and convert it to a string
    msg_id = f"msg_{uuid.uuid4().hex[:6]}"
    return msg_id


def generate_run_id():
    # Generate a unique ID and convert it to a string
    run_id = f"run_{uuid.uuid4().hex[:6]}"
    return run_id
