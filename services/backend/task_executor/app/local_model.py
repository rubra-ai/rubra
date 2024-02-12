# Standard Library
import json
import logging
import os
import random

# Third Party
import spacy
from openai import OpenAI

# Local
from app.models import Role7, Type8, Type824
from app.tools.file_knowledge_tool import FileKnowledgeTool
from app.tools.get_date_tool import get_date
from app.tools.web_browse_tool.web_browse_tool import (
    WebBrowseTool,
    create_google_search_url,
    parse_url,
)

ner = spacy.load("en_core_web_sm")

pattern = r">(.*?)</"


FUNCTION_CALL_FORMAT = """{"function": "function_name", "args": {"arg_1": "value_1", "args_2": "value_2" ...}}"""
CHAT_FORMAT = '{"choice": "Chat", "content": "your response"}'
TOOL_OUTPUT_ROLE = Role7.tool_output.value
QUERY_FORMAT = '{"query": "refined question"}'

litellm_host = os.getenv("LITELLM_HOST", "localhost")


oai_client = OpenAI(
    base_url=f"http://{litellm_host}:8002/v1/",
    # base_url="http://localhost:1234/v1/",
    api_key="abc",
)
model_name = "custom"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def ner_date_detection(query: str) -> bool:
    """Detect if the query contains a date entity"""
    # Process the text
    doc = ner(query)

    # Search for entities in the text
    for ent in doc.ents:
        if ent.label_ == "DATE":
            return True

    return False


def query_enhancement_relative_date(query: str) -> str:
    PROMPT = f"""
today's date is : {get_date()}
Given the QUESTION, generate a new query that can be used to google search.
Find out the indent of the QUESTION, if it's looking for information with relative date, improve it with fixed date, for example:
EXAMPLE1: "who won the US election yesterday" -> "US election result {get_date(day_delta=-1)}"
EXAMPLE2: "tomorrow's weather in SF" -> "weather in SF on {get_date(day_delta=1)}"

Your response should be in the following json format:
{QUERY_FORMAT}

QUESTION: {query}
"""
    messages = [{"role": "user", "content": PROMPT}]
    response = oai_client.chat.completions.create(
        model="openai/custom", messages=messages, stream=False
    )
    res = response.choices[0].message.content
    try:
        res = json.loads(res)["query"]
    except Exception as e:
        logging.error(
            "LLM response is not in valid json format, using the original query."
        )
        res = query
    return res


def query_enhancement_no_date(query: str) -> str:
    PROMPT = f"""
Today's date is : {get_date()}
Given the QUESTION, generate a new query that can be used to google search.
Find out the intent of the QUESTION, if it is looking for latest information, then add date properly for example:
EXAMPLE1: "who won the Taiwan election" -> "Taiwan election result {get_date(year_only=True)}"
EXAMPLE2: "the result of IOWA vote" -> "the result of IOWA vote {get_date(year_only=True)}"

Your response should be in the following json format:
{QUERY_FORMAT}

QUESTION: {query}
"""
    messages = [{"role": "user", "content": PROMPT}]
    response = oai_client.chat.completions.create(
        model="openai/custom", messages=messages, stream=False
    )
    res = response.choices[0].message.content
    try:
        res = json.loads(res)["query"]
    except Exception as e:
        logging.error(
            "LLM response is not in valid json format, using the original query."
        )
        res = query
    return res


def simple_summarize(query: str, context: str) -> str:
    if len(context.strip()) == 0:
        return "Sorry, I can't find any relevant information."
    PROMPT = f"""
Do NOT infer or assume anything, generate an answer to the QUESTION only based on the search results you got, include as much information as possible.
If the search results is irrelevant, politely express that you can't help.
--------------------
SEARCH RESULTS:
{context}
--------------------
QUESTION: {query}
"""
    messages = [{"role": "user", "content": PROMPT}]
    response = oai_client.chat.completions.create(
        model="openai/custom", temperature=0.1, messages=messages, stream=False
    )
    return response.choices[0].message.content


QA_FORMAT_FALSE = "Not enough information"


def simple_qa(query: str, context: str) -> str:
    PROMPT = f"""
Do NOT infer or assume anything, only answer the QUESTION based on the search results.
When the search results do not directly provide enough information for answering the qestion, response with txt format: {QA_FORMAT_FALSE}
Otherwise, simply response with you answer that only focus on answer the question, and do not infer or assume anything.
--------------------
SEARCH RESULTS:
{context}
--------------------
QUESTION: {query}
"""
    messages = [{"role": "user", "content": PROMPT}]
    response = oai_client.chat.completions.create(
        model="openai/custom",
        temperature=0.1,
        messages=messages,
        stream=False,
        response_format="web",
    )
    return response.choices[0].message.content


def simple_judge(query: str, answer: str) -> str:
    PROMPT = f"""
Given the QUESTION and the ANSWER, determine if the ANSWER is sufficient to the QUESTION.
if the ANSWER does answer the QUESTION completely, response with word "Yes".
Otherwise, if the answer indicates that there's not enough information to fully answer the question, response with word "No".

QUESTION: {query}? ANSWER: {answer}
"""
    messages = [{"role": "user", "content": PROMPT}]
    response = oai_client.chat.completions.create(
        model="openai/custom", temperature=0.0, messages=messages, stream=False
    )
    return response.choices[0].message.content


def multi_step_summarize(query: str, context: str) -> str:
    # Third Party
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=300)

    page_res_list = []
    for i, c in enumerate(context):
        ctx = parse_url(c["url"], query)
        logging.info(f"=========visited url:========== {c['url']}")
        if len(ctx) == 0:
            continue
        texts = text_splitter.split_text(ctx)

        useful_chunk = 0
        for i, t in enumerate(texts):
            if i >= 10:  # arbitrary limit
                break
            chunk_qa = simple_qa(query=query, context=t)
            logging.debug(f"CHUNK {i} : {chunk_qa}")
            if not chunk_qa.startswith(QA_FORMAT_FALSE):
                page_res_list.append(chunk_qa)
                useful_chunk += 1

        if useful_chunk > 0:
            page_qa = simple_summarize(query=query, context="".join(page_res_list))
            logging.info(f"======PAGE_QA:======\n {page_qa}")
            is_sufficient = simple_judge(query=query, answer=page_qa)
            logging.info(f"======IS_SUFFICIENT:======\n {is_sufficient}")
            if is_sufficient.strip() == "Yes":
                return page_qa
    return page_qa


class RubraLocalAgent:
    def __init__(self, assistant_id, tools):
        self.assistant_id = assistant_id
        self.setup_tools(tools)

    def setup_tools(self, tools):
        self.available_tools = {}
        self.tools = []
        for t in tools:
            if t["type"] == Type8.retrieval.value:
                file_search_tool = FileKnowledgeTool()

                def post_processed_file_search(query: str):
                    context = file_search_tool._run(
                        query=query, assistant_id=self.assistant_id
                    )
                    summarized_ans = simple_summarize(query=query, context=context)
                    return summarized_ans

                self.tools.append(
                    {
                        "name": file_search_tool.name,
                        "description": file_search_tool.description,
                        "parameters": file_search_tool.parameters,
                    }
                )
                self.available_tools[file_search_tool.name] = post_processed_file_search
            elif t["type"] == Type824.retrieval.value:
                search_tool = WebBrowseTool()

                def post_processed_google_search(query: str):
                    date_detected = ner_date_detection(query)
                    if date_detected:
                        logging.info(
                            "Date detected in query, using relative date enhancement."
                        )
                        # new_query = query_enhancement_relative_date(query) # TODO: need improvement
                        new_query = query
                    else:
                        logging.info(
                            "No date detected in query, using no date enhancement."
                        )
                        new_query = query_enhancement_no_date(query)
                    logging.debug(f"enhanced search query : {new_query}")
                    context = search_tool._run(
                        new_query, web_browse=False, concat_text=False
                    )
                    # summarized_ans = simple_summarize(new_query, context=context)
                    summarized_ans = multi_step_summarize(query, context=context)

                    # Add search reference for web-browse/google-search
                    google_search_url = create_google_search_url(new_query)
                    word_pool1 = ["I did", "After", "With"]
                    word_pool2 = ["I found", "I have", "I got", "I discovered"]
                    search_res_prefix = f"{random.choice(word_pool1)} a [quick search]({google_search_url}), here's what {random.choice(word_pool2)}:\n\n"
                    final_ans = search_res_prefix + summarized_ans
                    return final_ans

                self.tools.append(
                    {
                        "name": search_tool.name,
                        "description": search_tool.description,
                        "parameters": search_tool.parameters,
                    }
                )
                self.available_tools[search_tool.name] = post_processed_google_search

    def validate_function_call(self, msg: str) -> (bool, str):
        try:
            funtion_call_json = json.loads(msg)
        except Exception as e:
            logging.warning("invalid json format")
            logging.warning(e)
            try:
                funtion_call_json = json.loads(
                    msg + "}"
                )  # sometimes the msg is not complete with a closing bracket
            except Exception as e:
                logging.error(e)
                return False, msg

        if "function" in funtion_call_json:
            return True, json.dumps(funtion_call_json)
        else:
            return False, funtion_call_json["content"]

    def chat(
        self,
        msgs: list,
        sys_instruction: str = "",
        stream: bool = True,
    ):
        messages = []

        if sys_instruction is None or sys_instruction == "":
            system_instruction = "You are a helpful assistant."
        else:
            system_instruction = sys_instruction

        if len(self.tools) > 0:
            response_format = {"type": "json_object"}
            system_instruction += f"""
You have access to the following tool:
```
{self.tools[0]}
```
To use a tool, response strictly with the following json format:
{FUNCTION_CALL_FORMAT}

To chat with user, response strictly with the following json format:
{CHAT_FORMAT}

You MUST only answer user's question based on the output from tools, include as much information as possible.
If there is no tools or no relevant information that matches user's request, you should response that you can't help.
"""
        else:
            response_format = None

        messages.append({"role": "system", "content": system_instruction})
        for msg in msgs:
            if (
                msg["role"] == "user"
                or msg["role"] == "assistant"
                or msg["role"] == "tool_output"
            ):
                messages.append(msg)

        response = oai_client.chat.completions.create(
            model="openai/custom",
            messages=messages,
            stream=stream,
            temperature=0.1,
            response_format=response_format,
        )

        return response

    def get_function_response(self, function_call_json):
        try:
            function_name = function_call_json["function"]
            function_to_call = self.available_tools[function_name]
            function_args = function_call_json["args"]
            logging.info(
                f"Calling function : {function_name} with args: {function_args}"
            )
            function_response = function_to_call(**function_args)
            return function_response
        except Exception as e:
            logging.error(e)
            return "Rubra Backend Error: Failed to process function."

    def conversation(
        self,
        msgs: list,
        sys_instruction: str = "",
        stream: bool = True,
    ):
        messages = msgs.copy()

        response = self.chat(msgs=msgs, sys_instruction=sys_instruction, stream=stream)

        msg = ""
        for r in response:
            if r.choices[0].delta.content != None:
                msg += r.choices[0].delta.content

        if len(self.tools) == 0:
            msgs.append({"role": "assistant", "content": msg})
            return response, msgs

        is_function_call, parsed_msg = self.validate_function_call(msg)
        print(parsed_msg)

        if is_function_call:
            print("=====function call========")
            msgs.append({"role": "assistant", "content": parsed_msg})

            function_response = self.get_function_response(
                function_call_json=json.loads(parsed_msg)
            )

            msg = function_response
            print(f"\n MESSAGE: {msg}\n")
            parsed_msg = msg

        msgs.append({"role": "assistant", "content": parsed_msg})
        messages = msgs
        return response, messages
