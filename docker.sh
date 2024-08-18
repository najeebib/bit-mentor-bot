#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <docker_hub_username>"
    exit 1
fi

DOCKER_HUB_USERNAME="$1"

IMAGE_NAME="telegram-bot"
TAG="latest"
VERSION_TAG="v1.0.0"
CONTAINER_NAME="telegram-bot-container"

ENV_FILE_PATH="$(cd "$(dirname "$0")" && pwd)/.env_dev"

if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    ENV_FILE_PATH=$(cygpath -w "$ENV_FILE_PATH")
fi

if [ ! -f "$ENV_FILE_PATH" ]; then
    echo "Environment file '$ENV_FILE_PATH' not found."
    exit 1
fi

echo "Using environment file at: '$ENV_FILE_PATH'"

echo "Building Docker image..."
docker build -t $IMAGE_NAME:$TAG .

if [ $? -eq 0 ]; then
    echo "Docker image built successfully."

    docker tag $IMAGE_NAME:$TAG $DOCKER_HUB_USERNAME/$IMAGE_NAME:$VERSION_TAG

    echo "Pushing Docker image to Docker Hub..."
    docker push $DOCKER_HUB_USERNAME/$IMAGE_NAME:$VERSION_TAG

    if [ $? -eq 0 ]; then
        echo "Docker image pushed to Docker Hub successfully."

        echo "Running Docker container with Docker Compose..."
        docker-compose up -d

        if [ $? -eq 0 ]; then
            echo "Docker container is running."
        else
            echo "Failed to start Docker container."
        fi
    else
        echo "Failed to push Docker image to Docker Hub."
    fi
else
    echo "Docker image build failed."
fi
