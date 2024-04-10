from hangman_app import db, game_db
from typing import Optional
from pymongo.errors import PyMongoError


class HangmanGame:
    GUESSES = 10
    HP = 6

    def __init__(
        self,
        user_id,
        game_collection_name="hangman_games",
        word_collection_name="hangman_game_words",
        guesses=GUESSES,
        health_points=HP,
    ):
        self.game_collection_name = game_collection_name
        self.word_collection_name = word_collection_name
        self.user_id = user_id
        self.random_word = None
        self.guessed_letters = []
        self.game_id = None
        self.guess_count = guesses
        self.health_points = health_points
        self.game_status = "Playing"
        self.create_game(guesses, health_points)

    def create_game(self, guesses, health_points) -> Optional[str]:
        try:
            collection = game_db.get_collection(
                collection_name=self.game_collection_name
            )
            self.random_word = game_db.get_random_word(
                word_collection_name=self.word_collection_name
            )
            document = {
                "user_id": self.user_id,
                "guesses": guesses,
                "hp": health_points,
                "word": self.random_word,
                "guessed_letters": self.guessed_letters,
            }
            result = collection.insert_one(document)
            self.game_id = result.inserted_id
            return str(result.inserted_id)
        except PyMongoError as err:
            print(f"An error occurred: {err}")

    def mask_word(self, word, guessed_letters) -> Optional[str]:
        masked_word = "".join(
            [letter if letter in guessed_letters else "_" for letter in word]
        )
        return masked_word

    def update_game_status(self) -> str:
        masked_word = self.mask_word(self.random_word, self.guessed_letters)
        if masked_word == self.random_word:
            self.game_status = "Won"
        elif self.health_points == 0 or self.guess_count == 0:
            self.game_status = "Lost"
        else:
            self.game_status = self.game_status

    def make_a_guess(self, guessed_letter) -> None:
        try:
            self.guessed_letters.append(guessed_letter)
            self.guess_count -= 1
            if guessed_letter not in self.random_word:
                self.health_points -= 1
            self.update_game_status()
            print(self.guessed_letters)
            # Construct the update dictionary with updated fields
            update_dict = {
                "guessed_letters": self.guessed_letters,
                "guesses": self.guess_count,
                "hp": self.health_points,
                "game_status": self.game_status,
            }

            # Perform the update operation
            game_db.update_one_document(
                collection_name=self.game_collection_name,
                query={"_id": self.game_id},
                update=update_dict,
            )
        except Exception as e:
            print(f"An error occurred: {e}")

    def is_game_over(self) -> bool:
        return self.game_status in ["Won", "Lost"]


# we can add a new game to the database here
# add updating functions here as well

# if new_game > db.create_game(game_collection_name, word_collection_name, user_id)
