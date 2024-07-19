from email_operations import mark_as_read, list_messages, read_message

functions = [
    {
            "type": "function",
            "function": {
                "name": "get_today_date",
                "description": "get today's date and time",
                "parameters": {
                    "type": "object",
                    "properties": {
                        # "directory": {
                        #     "type": "string",
                        #     "description": "the directory to list files from"
                        # }
                    },
                    "required": [
                        # "directory"
                    ]
                }
            }
        },
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
                        # "directory"
                    ]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "mark_email_as_read",
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
                "name": "read_email",
                "description": "read an email and get the content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "email_id": {
                            "type": "string",
                            "description": "the id of the email to read content."
                        }
                    },
                    "required": [
                        "email_id"
                    ]
                }
            }
        },
]

def get_date():
    return "2024-07-18"




tool_call_mapping = {
    "get_today_date": get_date,
    "list_unread_emails": list_messages,
    "mark_email_as_read": mark_as_read,
    "read_email": read_message
}