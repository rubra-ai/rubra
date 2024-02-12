# Standard Library
import json
import os
from typing import List

# Third Party
import requests
from langchain.embeddings.base import Embeddings

HOST = os.getenv("EMBEDDING_HOST", "localhost")
EMBEDDING_URL = f"http://{HOST}:8020/embed_multiple"


def embed_text(texts: List[str]) -> List[List[float]]:
    """Embed a list of texts using a remote service.

    Args:
        texts (List[str]): List of texts to be embedded.

    Returns:
        List[List[float]]: List of embedded texts.
    """
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    data = json.dumps(texts)

    response = requests.post(EMBEDDING_URL, headers=headers, data=data)
    response = response.json()

    return response["embeddings"]


class CustomEmbeddings(Embeddings):
    """Custom embeddings class that uses a remote service for embedding."""

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents.

        Args:
            texts (List[str]): List of documents to be embedded.

        Returns:
            List[List[float]]: List of embedded documents.
        """
        return embed_text(texts)

    def embed_query(self, text: str) -> List[float]:
        """Embed a single query.

        Args:
            text (str): Query to be embedded.

        Returns:
            List[float]: Embedded query.
        """
        return embed_text([text])[0]
