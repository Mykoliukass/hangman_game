# Check if MongoDB container is already running
if [ "$(docker ps -q -f name=hangman_games-mongo)" ]; then
    echo "MongoDB container is already running."
else
    # Start MongoDB Docker container if not already running
    docker start hangman_games-mongo
    echo "MongoDB container started."
fi

# Wait for MongoDB to start (if needed)
echo "Waiting for MongoDB to start..."
sleep 5

# Run Flask application
python run.py

# Stop MongoDB container after Flask application finishes
docker stop hangman_games-mongo
echo "MongoDB container stopped."