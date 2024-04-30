import unittest
from hangman_app.game_logic.hangman_logic import HangmanGame


class TestHangmanGame(unittest.TestCase):
    def setUp(self):
        self.user_id = 1
        self.game = HangmanGame(user_id=self.user_id)
        self.game.random_word = "PYTHON"
        self.game.game_id = "61f1a3b4c5d6e7f8a9b0cdef"

    def test_mask_word(self):
        # Test with 0 guessed letters
        masked_word = self.game.mask_word("PYTHON", [])
        self.assertEqual(masked_word, "______")

        # Test with some guessed letters
        guessed_letters = ["P", "Y", "T"]
        masked_word = self.game.mask_word("PYTHON", guessed_letters)
        self.assertEqual(masked_word, "PYT___")

        # Testing with all correct letters
        guessed_letters = list("PYTHON")
        masked_word = self.game.mask_word("PYTHON", guessed_letters)
        self.assertEqual(masked_word, "PYTHON")

    def test_make_a_guess(self):
        # Guessing a correct letter
        self.game.make_a_guess("P")
        self.assertIn("P", self.game.guessed_letters)
        self.assertEqual(self.game.guess_count, HangmanGame.GUESSES - 1)
        self.assertEqual(self.game.health_points, HangmanGame.HP)

        # Testing handling incorrect letter guess
        self.game.make_a_guess("Z")
        self.assertIn("Z", self.game.guessed_letters)
        self.assertEqual(self.game.guess_count, HangmanGame.GUESSES - 2)
        self.assertEqual(self.game.health_points, HangmanGame.HP - 1)

        # Testing game status change
        self.game.make_a_guess("Y")
        self.game.make_a_guess("T")
        self.game.make_a_guess("H")
        self.game.make_a_guess("O")
        self.game.make_a_guess("N")
        self.assertEqual(self.game.game_status, "Won")


if __name__ == "__main__":
    unittest.main()
