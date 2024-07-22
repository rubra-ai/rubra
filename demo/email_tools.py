from email_operations import mark_as_read, list_messages, read_message
from run_chat_completion import run_chat
import json

default_system_prompt = "You are a helpful assistant."

def run_agent(user_query, functions, system_prompt=default_system_prompt):
    print(f"User query: {user_query}")
    res, msgs = run_chat(user_query=user_query, functions=functions, system_prompt=system_prompt)
    while res.message.tool_calls:
        tool_calls = []
        func_output =[]
        for tool_call in res.message.tool_calls:
            
            func_name,func_args = tool_call.function.name, tool_call.function.arguments
            print(f"\n=====calling function : {func_name}, with args: {func_args}")
            tool_calls.append( {
                                "id": tool_call.id,
                                "function": {"name": func_name,
                                            "arguments": func_args},
                                "type": "function",
                            })
            func_args = json.loads(func_args)
            func_to_run = tool_call_mapping[func_name]
            observation = func_to_run(**func_args)
            # print(f"Observation: {observation}")
            func_output.append([tool_call.id, func_name, str(observation)])
        msgs.append({"role": "assistant",  "tool_calls": tool_calls})
        for id,func_name, o in func_output:
            msgs.append({
                        "role": "tool",
                        "name": func_name,
                        "content": o,
                        "tool_call_id": id
                })
        res, msgs = run_chat(user_query=user_query,functions=functions, msgs=msgs)
    final_res = res.message.content
    return final_res


main_functions = [
        {
            "type": "function",
            "function": {
                "name": "list_unread_emails",
                "description": "List all unread emails in the mailbox",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "n": {
                            "type": "integer",
                            "description": "the number of emails to return, default = 5"
                        },
                        "date": {
                            "type": "string",
                            "description": "list unread email for a specific date, in yyyy-mm-dd format, default is None. Useful when user want emails for a certain day"
                        },
                        
                    },
                    "required": [

                    ]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "change_email_to_read",
                "description": "change the status of an email to `read`",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "the id of the unread email to be marked as read."
                        }
                    },
                    "required": [
                        "email_id"
                    ]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "label_email",
                "description": "read an email and label it with one of the three label: work, daily, important",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "the id of the email to process."
                        }
                    },
                    "required": [
                        "email_id"
                    ]
                }
            }
        },
]


def label_message(email_id) -> str:
    """This is a rule based example to label emails. It's also possible to use LLM's help to do so.

    Args:
        email_id (_type_): _description_
    Return:
        one of the three label: [work, daily, important]
    """
    msg_detail = read_message(email_id)
    print(msg_detail["title"])
    print(msg_detail["date"])
    print(msg_detail["sender"])
    print(msg_detail["receiver"])
    
    # Now do some rule based stuff or use LLM or some model to label the email
    label = "daily"
    if "@acorn.io" in msg_detail["sender"]:
        label = "work"
    # some arbitrary keyword rule based stuff
    elif "REMINDER" in msg_detail["title"] or "important" in msg_detail["content_text"]: 
        label = "important"
        
    print(label)
    return f"Label: {label}"
    

tool_call_mapping = {
    "list_unread_emails": list_messages,
    "change_email_to_read": mark_as_read,
    "label_email": label_message,
}




