# Standard Library
import logging
import time
from typing import List
import asyncio

# Third Party
from fastapi import FastAPI
from text_embedding_service import embed_multiple

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.get("/ping")
def ping():
    return {"response": "Pong!"}

@app.post("/embed_multiple")
async def api_embed_multiple(texts: List[str]):
    """
    Embeds multiple texts using the `embed_multiple` function.

    Args:
        texts (List[str]): A list of texts to be embedded.

    Returns:
        dict: A dictionary containing the embeddings of the texts.
    """
    try:
        t0 = time.time()
        embeddings = await asyncio.to_thread(embed_multiple, texts)
        logging.debug(f"Embedding time: {time.time() - t0}")
        return {"embeddings": embeddings}
    except Exception as e:
        logging.error(f"An error occurred during embedding: {e}")
        return {"error": str(e)}, 500