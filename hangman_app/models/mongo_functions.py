from typing import List, Dict, Optional
import random
from datetime import datetime
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from configurations import configurations


class MongoCRUD:
    def __init__(self, host: str, port: int, database_name: str) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        self.client = MongoClient(self.host, self.port)
        self.database: Database = self.client[self.database_name]
        self.generate_and_insert_words(
            configurations.WORD_COLLECTION_NAME,
            word_count=2000,
        )

    def generate_and_insert_words(self, collection_name: str, word_count: int) -> None:
        collection: Collection = self.database[collection_name]
        if collection.count_documents({}) > 0:
            print(f"The collection '{collection_name}' already has data.")
            return

        with open(
            "../extra_files/english_words.txt",
            "r",
            encoding="utf-8",
        ) as file:
            english_words = [line.strip() for line in file]

        words = set()
        while len(words) < word_count:
            word = random.choice(english_words).upper()
            if 6 <= len(word) <= 13:
                words.add(word)

        documents = [{"word": word} for word in words]

        self.insert_many_documents(collection_name, documents)
        print(
            f"Inserted {len(documents)} words into the collection '{collection_name}'."
        )

    def get_collection(self, collection_name: str) -> Collection:
        collection: Collection = self.database[collection_name]
        return collection

    def find_documents(
        self, collection_name: str, query: Optional[Dict] = None
    ) -> List[Dict]:
        collection = self.get_collection(collection_name)
        try:
            if query is None:
                documents = collection.find({}, {"_id": 0})
            else:
                documents = collection.find(query, {"_id": 0})
            return list(documents)
        except PyMongoError as e:
            raise Exception(f"Failed to find documents: {e}")

    def insert_one_document(self, collection_name: str, document: Dict) -> str:
        collection = self.get_collection(collection_name)
        try:
            result = collection.insert_one(document)
            return str(result.inserted_id)
        except PyMongoError as e:
            raise Exception(f"Failed to insert one document: {e}")

    def insert_many_documents(self, collection_name: str, documents: List[Dict]) -> str:
        collection = self.get_collection(collection_name)
        try:
            result = collection.insert_many(documents)
            return str(result.inserted_ids)
        except PyMongoError as e:
            raise Exception(f"Failed to insert many documents: {e}")

    def update_one_document(
        self, collection_name: str, query: Dict, update: Dict
    ) -> int:
        collection = self.get_collection(collection_name)
        try:
            result = collection.update_one(query, {"$set": update})
            return result.modified_count
        except PyMongoError as e:
            raise Exception(f"Failed to update document: {e}")

    def get_random_word(self, word_collection_name: str) -> str:
        word_collection = self.get_collection(word_collection_name)
        try:
            random_document_cursor = word_collection.aggregate(
                [{"$sample": {"size": 1}}]
            )
            random_document = next(random_document_cursor)
            random_word = random_document["word"]
            return random_word
        except PyMongoError as e:
            raise Exception(f"Failed to get random word: {e}")

    def get_games_played_today_or_to_date(
        self, game_collection_name: str, user_id: str, today: bool = False
    ) -> List[Dict]:
        try:
            game_collection = self.get_collection(game_collection_name)
            if today:
                today_date = datetime.now().strftime("%Y-%m-%d")
                query = {"user_id": user_id, "game_date": today_date}
            else:
                query = {"user_id": user_id}
            games_history = self.find_documents(game_collection_name, query)
            return games_history
        except PyMongoError as e:
            raise Exception(f"Failed to get games played history: {e}")
