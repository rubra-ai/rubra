# Use an official Python runtime as a parent image
FROM python:3.10-slim as builder

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Use a second stage to create a smaller final image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the built dependencies from the builder stage
COPY --from=builder /usr/local /usr/local

# Copy the necessary application files and .streamlit configuration
COPY ./app/*Chat.py /app/
COPY ./app/pages /app/pages
COPY ./app/rubra_ui_utils.py /app/
COPY ./app/rubra_ui_config.py /app/
COPY ./.streamlit/config.toml /root/.streamlit/config.toml

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Run streamlit when the container launches
CMD ["streamlit", "run", "1_💬_Chat.py", "--server.port=8501", "--server.address=0.0.0.0"]
