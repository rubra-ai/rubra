# Text Embedding API

This project provides a FastAPI server for generating text embeddings using a pre-trained model.

## Getting Started

To build and run the Docker container:

```bash
docker build -t text-embedding-api .
docker run -p 8020:8020 text-embedding-api
```

The API server will be available at `http://localhost:8020`.

## Endpoints

- `GET /ping`: Health check endpoint.
- `POST /embed_multiple`: Accepts a list of texts and returns their embeddings.

## Environment Variables

- `MODEL_NAME`: Set the environment variable to change the Sentence Transformer model
  - default is [`sentence-transformers/all-MiniLM-L6-v2`](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)