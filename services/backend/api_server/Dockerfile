FROM python:3.10-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements_backend.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

ENV HOST=host.docker.internal

# Run app.py when the container launches
CMD ["uvicorn", "app.backend:app", "--host", "0.0.0.0", "--port", "8000"]