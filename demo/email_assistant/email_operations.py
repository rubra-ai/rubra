'''
https://developers.google.com/gmail/api/quickstart/python
'''

import os.path
import base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]
# SCOPES = ["https://www.googleapis.com/auth/gmail.compose", "https://www.googleapis.com/auth/gmail.readonly"]

def auth():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def decode_base64(data):
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def gmail_send_message():
  """Create and insert a draft email.
   Print the returned draft's message and id.
   Returns: Draft object, including draft id and message meta data.

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  try:
    # create gmail api client
    service = build("gmail", "v1", credentials=auth())

    message = EmailMessage()

    message.set_content("This is automated draft mail")

    message["To"] = ["yingbei@acorn.io", "tybalex@gmail.com"]
    message["From"] = "tybalex@gmail.com"
    message["Subject"] = "Automated draft"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


def mark_as_read( email_id):
    service = build("gmail", "v1", credentials=auth())
    service.users().messages().modify(userId='me', id=email_id, body={'removeLabelIds': ['UNREAD']}).execute()
  


def read_message(email_id):
    service = build("gmail", "v1", credentials=auth())
    msg = service.users().messages().get(userId='me', id=email_id).execute()   

            # Extract the parts
    email_data = msg
    headers = email_data['payload']['headers']
    header_dict = {header['name']: header['value'] for header in headers}

    # Print the extracted information
    title = header_dict.get('Subject', 'No Subject')
    sender = header_dict.get('From', 'No Sender')
    receiver = header_dict.get('To', 'No Receiver')
    date = header_dict.get("Date", "No Date Received")
    
    content_text = ""
    try:
        if "parts" not in email_data['payload']:
            parts = []
        else:
            parts = email_data['payload']['parts']
        decoded_parts = {}

        for part in parts:
            mime_type = part['mimeType']
            encoded_data = part['body']['data']
            decoded_content = decode_base64(encoded_data)
            decoded_parts[mime_type] = decoded_content

        # Extract necessary information
        content_text = decoded_parts.get('text/plain', 'No Plain Text Content')
    except Exception as e:
        print(e)
    
    return {
        "id" : email_id,
        "title": title,
        "sender": sender,
        "receiver": receiver,
        "date": date,
        "content_text": content_text
    }

     
def list_messages(n=5, date = None):
    try:
        # create gmail api client
        service = build("gmail", "v1", credentials=auth())
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["UNREAD"])
            .execute()
        )
        messages = results.get('messages',[])
        res = []
        if not messages:
            print('No new messages.')
        else:
            for i, message in enumerate(messages):
                if i >= n:
                    break
                res.append(message["id"])
        
        print(res)
        return res
                
                                
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
#   gmail_send_message()
    res = list_messages()
    print(res)