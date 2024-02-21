FROM python:3.8-slim-buster

# Create a separate directory for dependencies
WORKDIR /app/requirements

# Copy requirements.txt into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy the FastAPI app script into the container
COPY ./main.py ./main.py
COPY --from=core ./ /app/core


# Expose the default port for FastAPI
EXPOSE 8010

ENV HOST=host.docker.internal

# Run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8010"]
