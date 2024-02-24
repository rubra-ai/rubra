FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y wget

# Copy the specific files
COPY text_embedding_service.py .
COPY api_server.py .

# create a separate path for the onnx model
RUN mkdir onnx
RUN wget https://huggingface.co/rubra-ai/all-MiniLM-L6-v2-optimum.onnx/resolve/main/all-MiniLM-L6-v2-optimum-optimized-quantized.onnx -O ./onnx/all-MiniLM-L6-v2-optimum.onnx
# COPY ./ ./onnx
# Expose the default port for FastAPI
EXPOSE 8020

# Health check for the container
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8020/ping || exit 1

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8020"]
