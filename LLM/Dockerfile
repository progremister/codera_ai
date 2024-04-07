# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends pciutils curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl https://ollama.ai/install.sh | sh

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir requests crewai langchain langchain-openai crewai[tools]

# Define environment variables for Ollama
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_ORIGINS=*

# Start the Ollama server in the background
RUN ollama serve &

# Run model.py when the container launches
CMD ["python", "./model.py"]
