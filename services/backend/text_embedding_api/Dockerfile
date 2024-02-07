FROM rancher/opni-python-base:3.8-torch

# Set the working directory in the container
WORKDIR /app

# Copy the requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the specific files
COPY text_embedding_service.py .
COPY api_server.py .

# Expose the default port for FastAPI
EXPOSE 8020

# Health check for the container
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8020/ping || exit 1

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8020"]