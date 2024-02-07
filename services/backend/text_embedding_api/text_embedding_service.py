# Standard Library
import os
from typing import List

# Third Party
from sentence_transformers import SentenceTransformer

default_model = "sentence-transformers/all-MiniLM-L6-v2"
model_name = os.getenv("MODEL_NAME", default_model)
model = SentenceTransformer(model_name)

def embed_multiple(texts: List[str]) -> List[List[float]]:
    return model.encode(texts).tolist()