FROM python:3.10.7-slim

# Set the working directory in the container to /app
WORKDIR /app

# First, add only the requirements file (to leverage Docker cache)
ADD requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN spacy download en_core_web_sm
RUN playwright install
RUN playwright install-deps


# Add the current directory contents into the container at /app
# This is done after installing dependencies to leverage Docker's cache
COPY . /app
COPY --from=core ./ /app/core
WORKDIR /app

# Set environment variables
ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

# Run app.py when the container launches
CMD ["celery", "-A", "core.tasks.tasks", "worker", "--loglevel=info"]
