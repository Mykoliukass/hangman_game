from typing import Optional
from pymongo.errors import PyMongoError
from hangman_app import game_db
from datetime import datetime
from bson import ObjectId
from hangman_app.logging.logging_decorator import log_decorator


class HangmanGame:
    GUESSES = 10
    HP = 6

    @classmethod
    def get_game_collection_name(cls):
        return "hangman_games"

    @classmethod
    def get_word_collection_name(cls):
        return "hangman_game_words"

    def __init__(
        self,
        user_id,
        guesses=GUESSES,
        health_points=HP,
    ):
        self.game_collection_name = self.get_game_collection_name()
        self.word_collection_name = self.get_word_collection_name()
        self.user_id = user_id
        self.random_word = None
        self.guessed_letters = []
        self.game_id = None
        self.guess_count = guesses
        self.health_points = health_points
        self.game_status = "Playing"
        self.game_date = self.get_date()

    @log_decorator
    def create_game(self) -> Optional[str]:
        collection = game_db.get_collection(collection_name=self.game_collection_name)
        self.random_word = game_db.get_random_word(
            word_collection_name=self.word_collection_name
        )
        document = self.get_game_document()
        result = collection.insert_one(document)
        self.game_id = result.inserted_id
        return str(result.inserted_id)

    @log_decorator
    def get_date(self) -> str:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")
        return formatted_date

    @log_decorator
    def get_game_document(self) -> dict:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")
        game_doc = {
            "user_id": self.user_id,
            "guesses": self.guess_count,
            "hp": self.health_points,
            "word": self.random_word,
            "guessed_letters": self.guessed_letters,
            "game_status": self.game_status,
            "game_date": formatted_date,
        }
        return {
            "user_id": self.user_id,
            "guesses": self.guess_count,
            "hp": self.health_points,
            "word": self.random_word,
            "guessed_letters": self.guessed_letters,
            "game_status": self.game_status,
            "game_date": formatted_date,
        }

    @log_decorator
    def to_json(self) -> dict:
        return {
            "user_id": self.user_id,
            "random_word": self.random_word,
            "guessed_letters": self.guessed_letters,
            "guesses": self.guess_count,
            "game_id": str(self.game_id),
            "health_points": self.health_points,
            "game_status": self.game_status,
            "game_date": self.game_date,
        }

    @log_decorator
    @classmethod
    def from_json(cls, jsonified_game: dict) -> "HangmanGame":
        hangman_instance = cls(
            user_id=jsonified_game["user_id"],
            guesses=jsonified_game["guesses"],
            health_points=jsonified_game["health_points"],
        )
        hangman_instance.random_word = jsonified_game["random_word"]
        hangman_instance.guessed_letters = jsonified_game["guessed_letters"]
        hangman_instance.game_id = jsonified_game["game_id"]
        hangman_instance.game_status = jsonified_game["game_status"]
        hangman_instance.game_date = jsonified_game["game_date"]
        return hangman_instance

    @log_decorator
    def mask_word(self, word, guessed_letters) -> Optional[str]:
        masked_word = "".join(
            [letter if letter in guessed_letters else "_" for letter in word]
        )
        return masked_word

    @log_decorator
    def update_game_status(self) -> str:
        masked_word = self.mask_word(self.random_word, self.guessed_letters)
        if masked_word == self.random_word:
            self.game_status = "Won"
        elif self.health_points == 0 or self.guess_count == 0:
            self.game_status = "Lost"
        else:
            self.game_status = self.game_status

    @log_decorator
    def make_a_guess(self, guessed_letter) -> None:
        self.guessed_letters.append(guessed_letter)
        self.guess_count -= 1
        if guessed_letter not in self.random_word:
            self.health_points -= 1
        self.update_game_status()
        update_dict = {
            "guessed_letters": self.guessed_letters,
            "guesses": self.guess_count,
            "hp": self.health_points,
            "game_status": self.game_status,
        }
        game_db.update_one_document(
            collection_name=self.game_collection_name,
            query={"_id": ObjectId(self.game_id)},
            update=update_dict,
        )

    @log_decorator
    def guess_a_whole_word(self, word) -> None:
        if word.upper() == self.random_word:
            self.game_status = "Won after the last chance"
            update_dict = {
                "guessed_letters": self.guessed_letters,
                "guesses": self.guess_count,
                "hp": self.health_points,
                "game_status": self.game_status,
            }
            game_db.update_one_document(
                collection_name=self.game_collection_name,
                query={"_id": self.game_id},
                update=update_dict,
            )
        else:
            self.game_status = "Lost"
            update_dict = {
                "guessed_letters": self.guessed_letters,
                "guesses": self.guess_count,
                "hp": self.health_points,
                "game_status": self.game_status,
            }
            game_db.update_one_document(
                collection_name=self.game_collection_name,
                query={"_id": self.game_id},
                update=update_dict,
            )

    @log_decorator
    def is_game_over(self) -> bool:
        return self.game_status in ["Won", "Lost", "Won after the last chance"]
