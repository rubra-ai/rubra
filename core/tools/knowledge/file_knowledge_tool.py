import os
import json
import requests

VECTOR_DB_HOST = os.getenv("VECTOR_DB_HOST", "localhost")
VECTOR_DB_MATCH_URL = f"http://{VECTOR_DB_HOST}:8010/similarity_match"

class FileKnowledgeTool:
    name = "FileKnowledge"
    description = "Useful for searching knowledge or information from user's files"
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

    def __init__(self):
        self.headers = {"accept": "application/json", "Content-Type": "application/json"}

    async def _arun(self, query: str, assistant_id):
        return await self._run(query, assistant_id)

    def _run(self, query: str, assistant_id):
        return self._file_knowledge_search_api(query, assistant_id)

    def _file_knowledge_search_api(self, query: str, assistant_id: str):
        data = json.dumps(
            {
                "text": query,
                "collection_name": assistant_id,
                "topk": 10,
                "rerank": False,
                "topr": 5,
            }
        )

        response = requests.post(VECTOR_DB_MATCH_URL, headers=self.headers, data=data)
        res = response.json()["response"]
        txt = ""
        for r in res:
            txt += r["text"] + "\n\n"
        return txt
