if [ "$(docker ps -q -f name=hangman_games-mongo)" ]; then
    echo "MongoDB container is already running."
else
    # Start MongoDB Docker container
    docker run -d -p 27017:27017 --name hangman_games-mongo mongo:latest
    echo "MongoDB container started."
fi

# Wait for MongoDB to start
echo "Waiting for MongoDB to start..."
sleep 5

# Run Flask application
python run.py

# Stop MongoDB container after Flask application finishes
docker stop hangman_games-mongo
echo "MongoDB container stopped."