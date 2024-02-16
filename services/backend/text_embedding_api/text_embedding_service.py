# Standard Library
import os
import logging
from typing import List, Iterator

# Third Party
from sentence_transformers import SentenceTransformer

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
default_model = "sentence-transformers/all-MiniLM-L6-v2"
model_name = os.getenv("MODEL_NAME", default_model)

# Load model
model = SentenceTransformer(model_name)

def batch_iterable(iterable: List[str], batch_size: int) -> Iterator[List[str]]:
    """
    Yields batches of the iterable with a given size.
    """
    length = len(iterable)
    for idx in range(0, length, batch_size):
        yield iterable[idx:min(idx + batch_size, length)]

def embed_multiple(texts: List[str], batch_size: int = 8) -> List[List[float]]:
    """
    Encodes texts into embeddings, processing in batches.
    """
    all_embeddings = []
    for i, batch in enumerate(batch_iterable(texts, batch_size), start=1):
        logging.info(f'Encoding batch {i}/{(len(texts) - 1) // batch_size + 1}')
        try:
            batch_embeddings = model.encode(batch).tolist()
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            logging.error(f'Error encoding batch {i}: {e}')
            continue
    return all_embeddings

# Example usage
# texts = ["This is a sentence", "Here is another one", "..."]  # Add your texts here
# embeddings = embed_multiple(texts, batch_size=64)  # Adjust batch_size based on your system's capability
