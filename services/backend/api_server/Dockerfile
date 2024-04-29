FROM python:3.10.7-slim

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app
COPY --from=core ./ /app/core

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install gcc g++ -y
RUN pip install --no-cache-dir -r requirements.txt
RUN spacy download en_core_web_sm
RUN playwright install
RUN playwright install-deps

# Make port 80 available to the world outside this container
EXPOSE 8000

ENV HOST=host.docker.internal

# Run app.py when the container launches
CMD ["uvicorn", "app.backend:app", "--host", "0.0.0.0", "--port", "8000"]
