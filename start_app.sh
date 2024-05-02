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
sleep 10

echo "Running Flask application..."
python run.py

docker stop $CONTAINER_NAME
echo "MongoDB container stopped."
