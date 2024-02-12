# Standard Library
import json
import os

# Third Party
import requests

VECTOR_DB_HOST = os.getenv("VECTOR_DB_HOST", "localhost")
VECTOR_DB_MATCH_URL = f"http://{VECTOR_DB_HOST}:8010/similarity_match"


class FileKnowledgeTool:
    name = "FileKnowledge"
    description = "Useful for search knowledge or information from user's file"
    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "the completed question to search",
            },
        },
        "required": ["query"],
    }

    async def _arun(self, query: str, assistant_id):
        return await file_knowledge_search_api(query, assistant_id)

    def _run(self, query: str, assistant_id):
        return file_knowledge_search_api(query, assistant_id)


def file_knowledge_search_api(query: str, assistant_id: str):
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = json.dumps(
        {
            "text": query,
            "collection_name": assistant_id,
            "topk": 10,
            "rerank": False,
            "topr": 5,
        }
    )

    response = requests.post(VECTOR_DB_MATCH_URL, headers=headers, data=data)
    res = response.json()["response"]
    txt = ""
    for r in res:
        txt += r["text"] + "\n\n"
    return txt
