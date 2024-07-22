
from email_tools import run_agent, main_functions

msgs = []
user_query = "Process my last 5 emails, get the label for each of them, then change the emails with a `daily` label to `read` status."

run_agent(user_query, main_functions)

    
        