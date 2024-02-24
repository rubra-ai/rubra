# Standard Library
import logging
from pathlib import Path
from typing import Any, Dict, Iterator, List

# Third Party
import torch
import torch.nn.functional as F
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configuration
model_id = "sentence-transformers/all-MiniLM-L6-v2"
optimized_model_id = "all-MiniLM-L6-v2-optimum.onnx"
# using optimum optimized and quantized model from: https://huggingface.co/philschmid/all-MiniLM-L6-v2-optimum-embeddings
onnx_path = Path("./onnx")


def batch_iterable(iterable: List[str], batch_size: int) -> Iterator[List[str]]:
    """
    Yields batches of the iterable with a given size.
    """
    length = len(iterable)
    for idx in range(0, length, batch_size):
        yield iterable[idx : min(idx + batch_size, length)]


# load vanilla transformers and generate config files for the model
model = ORTModelForFeatureExtraction.from_pretrained(model_id, from_transformers=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)

model.save_pretrained(onnx_path)
tokenizer.save_pretrained(onnx_path)


# copied from the model card for inference
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[
        0
    ]  # First element of model_output contains all token embeddings
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
        input_mask_expanded.sum(1), min=1e-9
    )


class PreTrainedPipeline:
    def __init__(self, path="."):
        # load the optimized model
        self.model = ORTModelForFeatureExtraction.from_pretrained(
            path, file_name=f"./{optimized_model_id}"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(path)

    def __call__(self, data: Any) -> List[List[Dict[str, float]]]:
        """
        Args:
            data (:obj:):
                includes the input data and the parameters for the inference.
        Return:
            A :obj:`list`:. The list contains the embeddings of the inference inputs
        """
        inputs = data.get("inputs", data)

        # tokenize the input
        encoded_inputs = self.tokenizer(
            inputs, padding=True, truncation=True, return_tensors="pt"
        )
        # run the model
        outputs = self.model(**encoded_inputs)
        # Perform pooling
        sentence_embeddings = mean_pooling(outputs, encoded_inputs["attention_mask"])
        # Normalize embeddings
        sentence_embeddings = F.normalize(sentence_embeddings, p=2, dim=1)
        # postprocess the prediction
        return sentence_embeddings.tolist()


my_handler = PreTrainedPipeline(path=onnx_path)


def embed_multiple(texts: List[str], batch_size: int = 8) -> List[List[float]]:
    """
    Encodes texts into embeddings, processing in batches.
    """

    all_embeddings = []
    for i, batch in enumerate(batch_iterable(texts, batch_size), start=1):
        logging.info(f"Encoding batch {i}/{(len(texts) - 1) // batch_size + 1}")
        try:
            batch_embeddings = my_handler({"inputs": batch})
            all_embeddings.extend(batch_embeddings)
        except Exception as e:
            logging.error(f"Error encoding batch {i}: {e}")
            continue
    return all_embeddings


# Example usage
# texts = ["This is a sentence", "Here is another one", "..."]  # Add your texts here
# embeddings = embed_multiple(texts, batch_size=64)  # Adjust batch_size based on your system's capability
