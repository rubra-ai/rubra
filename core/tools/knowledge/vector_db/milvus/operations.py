# Standard Library
import os
from typing import List, Optional

# Third Party
from pydantic import BaseModel

# Local application imports
from .custom_embeddigs import CustomEmbeddings
from .query_milvus import Milvus

MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")

model = {}
top_re_rank = 5
top_k_match = 10


class Query(BaseModel):
    text: str
    collection_name: str
    topk: int = top_k_match
    rerank: bool = False
    topr: int = top_re_rank


def drop_collection(collection_name: str):
    load_collection(collection_name).drop_collection()


def load_collection(collection_name: str) -> Milvus:
    return Milvus(
        embedding_function=CustomEmbeddings(),
        collection_name=collection_name,
        connection_args={
            "host": MILVUS_HOST,
            "port": "19530",
            "user": "username",
            "password": "password",
        },
        index_params={
            "metric_type": "IP",
            "index_type": "FLAT",
            "params": {"nlist": 16384},
        },
        search_params={"metric_type": "IP", "params": {"nprobe": 32}},
    )


def add_texts(
    collection_name: str,
    texts: List[str],
    metadatas: Optional[List[dict]] = None,
):
    c = load_collection(collection_name)
    pks = c.add_texts(texts=texts, metadatas=metadatas)
    print(pks)
    return pks


def delete_docs(collection_name: str, expr: str):
    c = load_collection(collection_name)
    c.delete_entities(expr=expr)


def get_top_k_biencoder_match_milvus(query: Query):
    c = load_collection(query.collection_name)

    docs = c.similarity_search(query.text, k=query.topk)
    res = []
    for i, d in enumerate(docs):
        thisd = {"id": i, "metadata": d.metadata, "text": d.page_content}
        res.append(thisd)
    return res


def get_similar_match(query, biencoder_match_method: str, rerank: bool = False):
    query_biencoder_matches = get_top_k_biencoder_match_milvus(query)
    return query_biencoder_matches[: query.topr]
