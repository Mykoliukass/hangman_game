CONTAINER_NAME = "hangman_games-mongo"
IMAGE_NAME = "mongo:latest"
MONGO_HOST = "localhost"
MONGO_PORT = 27017
DATABASE_NAME = "Hangman_games"
GAME_COLLECTION_NAME = "hangman_games"
WORD_COLLECTION_NAME = "hangman_game_words"

MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/{DATABASE_NAME}"


FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_SECRET_KEY = "hjshjhdjah kjshkjdhjs"
FLASK_DB_NAME = "user_database.db"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{FLASK_DB_NAME}"
