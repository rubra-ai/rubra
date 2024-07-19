import openai
openai.api_key = "123"
openai.base_url = "http://localhost:1234/v1/"

model = "gpt4o"

from email_tools  import functions, tool_call_mapping
import json

msgs = []
system_prompt = "You are a helpful assistant."
user_query = "look at my new emails today one by one. For each of them, if the content looks not important, such as commercials or utility bill, mark it as read."

def run_chat(user_query, msgs = []):
    if not msgs or len(msgs) == 0:
        msgs = [{"role": "system", "content":system_prompt} ,{"role": "user", "content": user_query}]
    else:
        msgs.append({"role": "user", "content": user_query})
    try:
        completion = openai.chat.completions.create(
            model=model,
            temperature=0.1,
            messages=msgs,
            tools=functions,
            tool_choice="auto",
            stream=False,
        )
        res = completion.choices[0]
        return res, msgs
    except Exception as e:
        print(f"Error : {e}")

res, msgs = run_chat(user_query=user_query)
while res.message.tool_calls:
    tool_calls = []
    func_output =[]
    for tool_call in res.message.tool_calls:
        
        func_name,func_args = tool_call.function.name, tool_call.function.arguments
        print(f"\n=====calling function : {func_name}, with args: {func_args}")
        func_args = json.loads(func_args)
        tool_calls.append( {
                            "id": tool_call.id,
                            "function": {"name": func_name,
                                        "arguments": func_args},
                            "type": "function",
                        })
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
    res, msgs = run_chat(user_query=user_query, msgs=msgs)
final_res = res.message.content
print(final_res)
    
        