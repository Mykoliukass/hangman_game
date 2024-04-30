from datetime import datetime
import logging
import random
from typing import List, Dict, Optional, Union
from pymongo import MongoClient
from pymongo.errors import (
    PyMongoError,
    ConnectionFailure,
    ConfigurationError,
    CollectionInvalid,
)

from hangman_app.logging.logging_module import get_database_error_logger


database_error_logger = get_database_error_logger()


class MongoCRUD:
    def __init__(self, host: str, port: int, database_name: str) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        try:
            self.client = MongoClient(self.host, self.port)
            self.database = self.client[self.database_name]
        except (ConnectionFailure, ConfigurationError) as e:
            database_error_logger.error(
                "Failed to connect to database: %s", str(e), exc_info=True
            )
            raise

    def get_collection(self, collection_name: str):
        try:
            logging.debug("Getting collection: %s", collection_name)
            collection = self.database[collection_name]
            logging.debug("Retrieved collection: %s", collection)
            return collection
        except (CollectionInvalid, PyMongoError) as e:
            database_error_logger.error(
                "Failed to get collection '%s': %s",
                collection_name,
                str(e),
                exc_info=True,
            )
            return None

    def find_documents(
        self, collection_name: str, query: Optional[Dict] = None
    ) -> Union[List[Dict], None]:
        try:
            collection = self.get_collection(collection_name)
            if query is None:
                documents = collection.find({}, {"_id": 0})
            else:
                documents = collection.find(query, {"_id": 0})
            return list(documents)
        except PyMongoError as e:
            database_error_logger.error(
                "Failed to find documents in '%s': %s",
                collection_name,
                str(e),
                exc_info=True,
            )
            return None

    def insert_one_document(
        self, collection_name: str, document: Dict
    ) -> Optional[str]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as e:
            database_error_logger.error(
                "Failed to insert one document in '%s': %s",
                collection_name,
                str(e),
                exc_info=True,
            )
            return None

    def insert_many_documents(
        self, collection_name: str, documents: List[Dict]
    ) -> Union[str, None]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_many(documents)
            return str(result.inserted_ids)
        except PyMongoError as e:
            database_error_logger.error(
                "Failed to insert many documents in '%s': %s",
                collection_name,
                str(e),
                exc_info=True,
            )
            return None

    def update_one_document(
        self, collection_name: str, query: Dict, update: Dict
    ) -> Union[int, None]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.update_one(query, {"$set": update})
            return result.modified_count
        except PyMongoError as e:
            database_error_logger.error(
                "Failed to update one document in '%s': %s",
                collection_name,
                str(e),
                exc_info=True,
            )
            return None

    def generate_and_insert_words(self, collection_name: str, word_count: int):
        try:
            with open("extra_files/english_words.txt", "r", encoding="utf-8") as file:
                english_words = [line.strip() for line in file]
            words = set()

            while len(words) < word_count:
                word = random.choice(english_words).upper()
                if len(word) < 6 or len(word) > 13:
                    continue
                words.add(word)

            documents = [{"word": word} for word in words]

            self.insert_many_documents(collection_name, documents)
        except PyMongoError as e:
            database_error_logger.error(
                "Failed to generate and insert words in '%s': %s",
                collection_name,
                str(e),
                exc_info=True,
            )

    def get_random_word(self, word_collection_name):
        try:
            word_collection = self.get_collection(word_collection_name)
            random_document_cursor = word_collection.aggregate(
                [{"$sample": {"size": 1}}]
            )
            random_document = next(random_document_cursor)
            random_word = random_document["word"]
            return random_word
        except PyMongoError as e:
            database_error_logger.error(
                "Failed to get random word from '%s': %s",
                word_collection_name,
                str(e),
                exc_info=True,
            )
            return None

    def get_games_played_today_or_to_date(
        self, game_collection_name, user_id, today=False
    ) -> Union[list, None]:
        try:
            if not today:
                game_collection = self.get_collection(game_collection_name)
                query = {"user_id": user_id}
                games_history = self.find_documents(game_collection_name, query)
                return games_history
            elif today:
                today_date = datetime.now().strftime("%Y-%m-%d")
                game_collection = self.get_collection(game_collection_name)
                query = {"user_id": user_id, "game_date": today_date}
                games_history = self.find_documents(game_collection_name, query)
                return games_history
        except PyMongoError as e:
            database_error_logger.error(
                "Failed to retrieve games history in '%s': %s",
                game_collection_name,
                str(e),
                exc_info=True,
            )
            return None
