# pylint: disable=import-error
from mongo_functions import MongoCRUD

HOST = "localhost"
PORT = 27017
DATABASE_NAME = "Hangman_games"
# These should be parametrized and made global for sh and other scripts
WORD_COLLECTION = "hangman_game_words"
GAME_COLLECTION = "hangman_games"

game_db = MongoCRUD(host=HOST, port=PORT, database_name=DATABASE_NAME)

game_db.generate_and_insert_words(collection_name=WORD_COLLECTION, word_count=20)
