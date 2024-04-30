# Check if MongoDB container is already running
if [ "$(docker ps -q -f name=hangman_games-mongo)" ]; then
    echo "MongoDB container is already running."
else
    # Start MongoDB Docker container if not already running
    docker start hangman_games-mongo
    echo "MongoDB container started."
fi

# Wait for a few seconds to ensure MongoDB is running
sleep 5

# Run the tests
echo "Running tests..."
python -m unittest discover -s tests -p "test_*.py"

# Check the exit status of the tests
if [ $? -eq 0 ]; then
    echo "Tests completed successfully."
else
    echo "Tests failed."
fi

# Stop MongoDB server
echo "Stopping MongoDB server..."
# Update the command below to stop your MongoDB server
docker stop hangman_games-mongo
echo "MongoDB container stopped."
echo "Done."
