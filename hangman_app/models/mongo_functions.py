from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import (
    PyMongoError,
    ConnectionFailure,
    ConfigurationError,
    CollectionInvalid,
    ExecutionTimeout,
    OperationFailure,
    ServerSelectionTimeoutError,
)
from typing import List, Dict, Optional, Union
from faker import Faker
import random
from datetime import datetime
from hangman_app.logging.logging_decorator import log_decorator


class MongoCRUD:
    def __init__(self, host: str, port: int, database_name: str) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        self.client = MongoClient(self.host, self.port)
        self.database = self.client[self.database_name]

    @log_decorator
    def get_collection(self, collection_name: str):
        return self.database[collection_name]

    @log_decorator
    def find_documents(
        self, collection_name: str, query: Optional[Dict] = None
    ) -> Union[List[Dict], None]:
        collection = self.get_collection(collection_name)
        if query is None:
            documents = collection.find({}, {"_id": 0})
        else:
            documents = collection.find(query, {"_id": 0})
        return list(documents)

    @log_decorator
    def insert_one_document(
        self, collection_name: str, document: Dict
    ) -> Optional[str]:
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return str(result.inserted_id)

    @log_decorator
    def insert_many_documents(
        self, collection_name: str, documents: List[Dict]
    ) -> Union[str, None]:
        collection = self.get_collection(collection_name)
        result = collection.insert_many(documents)
        return str(result.inserted_ids)

    @log_decorator
    def update_one_document(
        self, collection_name: str, query: Dict, update: Dict
    ) -> Union[int, None]:
        collection = self.get_collection(collection_name)
        result = collection.update_one(query, {"$set": update})
        return result.modified_count

    @log_decorator
    def generate_and_insert_words(self, collection_name: str, word_count: int):
        with open("extra_files/english_words.txt", "r") as file:
            english_words = [line.strip() for line in file]
        words = set()

        while len(words) < word_count:
            word = random.choice(english_words).upper()
            if len(word) < 6 or len(word) > 13:
                continue
            words.add(word)

        documents = [{"word": word} for word in words]

        self.insert_many_documents(collection_name, documents)

    @log_decorator
    def get_random_word(self, word_collection_name):
        word_collection = self.get_collection(word_collection_name)
        random_document_cursor = word_collection.aggregate([{"$sample": {"size": 1}}])
        random_document = next(random_document_cursor)
        random_word = random_document["word"]
        return random_word

    def get_games_played_today_or_to_date(
        self, game_collection_name, user_id, today=False
    ) -> list:
        if today == False:
            game_collection = self.get_collection(game_collection_name)
            query = {"user_id": user_id}
            games_history = self.find_documents(game_collection_name, query)
            return games_history
        elif today == True:
            today_date = datetime.now().strftime("%Y-%m-%d")
            game_collection = self.get_collection(game_collection_name)
            query = {"user_id": user_id, "game_date": today_date}
            games_history = self.find_documents(game_collection_name, query)
            return games_history
