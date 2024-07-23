## Rubra model demo

This demo will walk you through an example that how you can connect rubra tool-call model to your gmail mailbox, and let the ai assistant helps you take care of your emails.

*In this demo, the assistant is granted privileges only to read your emails and change the status of an email from unread to read.*

### Prerequisites:
- Python 3.10.7 or greater, with the pip package management tool
- A Google Cloud project.
- Your Google account with Gmail enabled.

### Get Started

**1.Start a Rubra Model server:**
Use either [tools.cpp](https://github.com/rubra-ai/tools.cpp?tab=readme-ov-file#toolscpp-quickstart) or [vLLM](https://github.com/rubra-ai/vllm?tab=readme-ov-file#rubra-vllm-quickstart) to serve a Rubra model.

**2.Enable Gmail API and setup authentication:**
A few things to config to allow the AI assistant to connect to your gmail emails thru Gmail API: 
- In the Google Cloud console, [enable the Gmail API](https://console.cloud.google.com/flows/enableapi?apiid=gmail.googleapis.com).
- [Configure the OAuth consent screen](https://developers.google.com/gmail/api/quickstart/python#configure_the_oauth_consent_screen): For User type select Internal, if you can't then simply select external.
- [Authorize credentials for a desktop application](https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application): Don't forget to download `credentials.json` to the `demo` dir or where you'd like to run the code.

Reference: https://developers.google.com/gmail/api/quickstart/python#set_up_your_environment

**3.Pip install and Run the python script:**
```python
pip install -r requirements.txt
```
and then:
```python
python main_email_assistant.py
```

The user prompt in this script:
```
Process my last 5 emails. get the label for all of them, then change the emails with a `daily` label to `read` status.
```
If everything goes well, the AI assistant will look at the latest 5 emails and mark some of them as `read`.

### What's next?
In the demo, the assistant is granted privileges only to: 
- list and read emails
- change the status of emails from `unread` to `read`.

You can definitely enhance its capabilities by introducing more tools/functions, such as moving emails to different folders/inboxes, drafting and sending emails, etc.