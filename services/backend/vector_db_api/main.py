# Standard Library
import logging
from typing import List, Optional

# Third Party
# Local application imports
from core.tools.knowledge.vector_db.milvus.operations import (
    Query,
    add_texts,
    delete_docs,
    drop_collection,
    get_similar_match,
    load_collection,
)
from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

model = {}
top_re_rank = 5
top_k_match = 10
app = FastAPI()


@app.on_event("startup")
async def app_startup():
    pass


@app.post("/add_texts")
async def add_texts_embeddings(
    collection_name: str,
    texts: List[str],
    metadatas: Optional[List[dict]] = None,
):
    """_summary_

    Args:
        texts (List[str]): _description_
        connlection_name (str): this should reflect user's random id + the assistant_id they created.
    """
    pks = add_texts(collection_name, texts, metadatas)


@app.delete("/delete_docs")
async def delete_docs_api(collection_name: str, expr: str):
    delete_docs(collection_name, expr)


@app.post("/similarity_match")
def text_similarity_match(query: Query):
    logging.info(f"=========Query: {query}=========")
    res = get_similar_match(query, biencoder_match_method="milvus", rerank=query.rerank)
    logging.info(f"================\nSimilarity match response:\n {res}")
    return {"response": res}


@app.get("/ping")
def ping():
    return {"response": "Pong!"}
