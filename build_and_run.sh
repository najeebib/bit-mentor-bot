#!/bin/bash

IMAGE_NAME="telegram-bot"
TAG="latest"
CONTAINER_NAME="telegram-bot-container"

# Get the absolute path to the .env_dev file and convert it to Windows format if necessary
ENV_FILE_PATH="$(cd "$(dirname "$0")" && pwd)/.env_dev"

# Convert the path to Windows format if running in Git Bash or WSL on Windows
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ENV_FILE_PATH=$(cygpath -w "$ENV_FILE_PATH")
fi

# Check if the .env_dev file exists
if [ ! -f "$ENV_FILE_PATH" ]; then
    echo "Environment file '$ENV_FILE_PATH' not found."
    exit 1
fi

# Debugging: Check the resolved path
echo "Using environment file at: '$ENV_FILE_PATH'"

echo "Building Docker image..."
docker build -t $IMAGE_NAME:$TAG .

if [ $? -eq 0 ]; then
    echo "Docker image built successfully."

    echo "Running Docker container..."
    docker run -d --name $CONTAINER_NAME \
        --env-file "$ENV_FILE_PATH" \
        -v "$ENV_FILE_PATH":/app/.env_dev \
        $IMAGE_NAME:$TAG

    if [ $? -eq 0 ]; then
        echo "Docker container is running."
    else
        echo "Failed to start Docker container."
    fi
else
    echo "Docker image build failed."
fi
