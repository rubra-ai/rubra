# Vector Search Service

This service provides a FastAPI application that interfaces with a vector database for text embedding and similarity search operations. It is designed to be flexible and allows for the potential integration of various vector databases in the future.

The service provides the following endpoints:

- `POST /add_texts`: Add texts to a specified Milvus collection
- `DELETE /delete_docs`: Delete documents from a specified Milvus collection based on an expression
- `POST /similarity_match`: Perform a similarity search and return the top-k similar documents
- `GET /ping`: Health check endpoint

