from typing import Optional
from hangman_app.logging_data.logging_module import get_game_logic_error_logger
from datetime import datetime
from configurations import configurations

game_logic_error_logger = get_game_logic_error_logger()


class HangmanGame:
    GUESSES = 10
    HP = 6

    def __init__(
        self,
        user_id,
        guesses=GUESSES,
        health_points=HP,
    ):
        self.game_collection_name = configurations.GAME_COLLECTION_NAME
        self.word_collection_name = configurations.WORD_COLLECTION_NAME
        self.user_id = user_id
        self.random_word = None
        self.guessed_letters = []
        self.game_id = None
        self.guess_count = guesses
        self.health_points = health_points
        self.game_status = "Playing"
        self.game_date = self.get_date()

    def create_game(self) -> Optional[str]:
        try:
            document = self.get_game_document()
            return document
        except Exception as e:
            game_logic_error_logger.error(
                "Failed to create game: %s", str(e), exc_info=True
            )
            return None

    def get_date(self) -> str:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")
        return formatted_date

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
        return game_doc

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

    @classmethod
    def from_json(cls, jsonified_game: dict) -> "HangmanGame":
        try:
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
        except KeyError as e:
            game_logic_error_logger.error(
                "Invalid JSON game data: %s", str(e), exc_info=True
            )
            return None

    def mask_word(self, word, guessed_letters) -> Optional[str]:
        try:
            masked_word = "".join(
                [letter if letter in guessed_letters else "_" for letter in word]
            )
            return masked_word
        except Exception as e:
            game_logic_error_logger.error(
                "Failed to mask word: %s", str(e), exc_info=True
            )
            return None

    def update_game_status(self) -> str:
        masked_word = self.mask_word(self.random_word, self.guessed_letters)
        if masked_word == self.random_word:
            self.game_status = "Won"
        elif self.health_points == 0 or self.guess_count == 0:
            self.game_status = "Lost"
        else:
            self.game_status = self.game_status
        return self.game_status

    def make_a_guess(self, guessed_letter) -> None:
        try:
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
            return update_dict
        except Exception as e:
            game_logic_error_logger.error(
                "Failed to make a guess: %s", str(e), exc_info=True
            )

    def guess_a_whole_word(self, word) -> None:
        try:
            if word.upper() == self.random_word:
                self.game_status = "Won after the last chance"
                update_dict = {
                    "guessed_letters": self.guessed_letters,
                    "guesses": self.guess_count,
                    "hp": self.health_points,
                    "game_status": self.game_status,
                }
                return update_dict
            else:
                self.game_status = "Lost"
                update_dict = {
                    "guessed_letters": self.guessed_letters,
                    "guesses": self.guess_count,
                    "hp": self.health_points,
                    "game_status": self.game_status,
                }
                return update_dict
        except Exception as e:
            game_logic_error_logger.error(
                "Failed to guess whole word: %s", str(e), exc_info=True
            )

    def is_game_over(self) -> bool:
        return self.game_status in ["Won", "Lost", "Won after the last chance"]

    def is_last_chance_needed(self) -> bool:
        if self.game_status != "Won" and (
            self.health_points == 0 or self.guess_count == 0
        ):
            return True
        else:
            return False
