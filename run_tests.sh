#!/bin/bash

eval $(python extract_config.py)

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "MongoDB container is already running."
else
    if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
        docker start $CONTAINER_NAME
        echo "MongoDB container started."
    else
        docker run -d --name $CONTAINER_NAME -p 27017:27017 $IMAGE_NAME
        echo "New MongoDB container created and started."
    fi
fi

echo "Waiting for MongoDB to start..."
sleep 5

echo "Running tests..."
python -m unittest discover -s tests -p "test_*.py"

if [ $? -eq 0 ]; then
    echo "Tests completed successfully."
else
    echo "Tests failed."
fi

echo "Stopping MongoDB container..."
docker stop $CONTAINER_NAME
echo "MongoDB container stopped."

echo "Done."
