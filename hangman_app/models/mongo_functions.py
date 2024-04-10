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


class MongoCRUD:
    def __init__(self, host: str, port: int, database_name: str) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        self.client = MongoClient(self.host, self.port)
        self.database = self.client[self.database_name]

    def get_collection(self, collection_name: str):
        try:
            return self.database[collection_name]
        except PyMongoError as err:
            print(f"An error occurred: {err}")

    def find_documents(
        self, collection_name: str, query: Dict
    ) -> Union[List[Dict], None]:
        try:
            collection = self.get_collection(collection_name)
            documents = collection.find(query, {"_id": 0})
            return list(documents)
        except PyMongoError as err:
            print(f"An error occurred: {err}")

    def insert_one_document(
        self, collection_name: str, document: Dict
    ) -> Optional[str]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as err:
            print(f"An error occurred: {err}")

    def insert_many_documents(
        self, collection_name: str, documents: List[Dict]
    ) -> Union[str, None]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_many(documents)
            return str(result.inserted_ids)
        except PyMongoError as err:
            print(f"An error occurred: {err}")

    def update_one_document(
        self, collection_name: str, query: Dict, update: Dict
    ) -> Union[int, None]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.update_one(query, {"$set": update})
            return result.modified_count
        except PyMongoError as err:
            print(f"An error occurred: {err}")

    def update_many_documents(
        self, collection_name: str, query: Dict, update: Dict
    ) -> Union[int, None]:
        try:
            collection = self.get_collection(collection_name)
            result = collection.update_many(query, {"$set": update})
            return result.modified_count
        except PyMongoError as err:
            print(f"An error occurred: {err}")

    def generate_and_insert_words(self, collection_name: str, word_count: int):
        with open(
            "Z:\CodeAcademy\hangman_game\hangman_app\extra_files/english_words.txt", "r"
        ) as file:
            english_words = [line.strip() for line in file]

        words = set()

        while len(words) < word_count:
            word = random.choice(english_words)
            if len(word) < 6 or len(word) > 13:
                continue
            words.add(word)

        documents = [{"word": word} for word in words]

        self.insert_many_documents(collection_name, documents)

    def get_random_word(self, word_collection_name):
        try:
            word_collection = self.get_collection(word_collection_name)
            random_document_cursor = word_collection.aggregate(
                [{"$sample": {"size": 1}}]
            )
            random_document = next(
                random_document_cursor
            ) 
            random_word = random_document["word"]
            return random_word
        except PyMongoError as err:
            print(f"An error occurred while fetching random word: {err}")