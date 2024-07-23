import openai
openai.api_key = "sk-"
openai.base_url = "http://localhost:1234/v1/"

model = "gpt-4o"


def run_chat(user_query, system_prompt = "", functions=[], msgs = []):
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