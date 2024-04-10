from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from hangman_app import db, game_db
from bson import ObjectId
from hangman_app.game_logic.hangman_logic import HangmanGame

routes = Blueprint("routes", __name__)


@routes.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)


@routes.route("/NewGame", methods=["GET", "POST"])
@login_required
def newgame():
    global hangman_game_instance
    game_document = None  # Initialize game_document here

    if request.method == "GET":
        user_id = current_user.id
        hangman_game_instance = HangmanGame(user_id=user_id)
        game_document = {
            "user_id": hangman_game_instance.user_id,
            "word": hangman_game_instance.random_word,
            "guesses": hangman_game_instance.guess_count,
            "hp": hangman_game_instance.health_points,
            "guessed_letters": hangman_game_instance.guessed_letters,
            "game_status": hangman_game_instance.game_status,
        }
        chosen_letter = None
    elif request.method == "POST":
        chosen_letter = request.form.get("letter")

        if chosen_letter:
            hangman_game_instance.make_a_guess(chosen_letter)

            # Update game_document with the new game state
            game_document = {
                "user_id": hangman_game_instance.user_id,
                "word": hangman_game_instance.random_word,
                "guesses": hangman_game_instance.guess_count,
                "hp": hangman_game_instance.health_points,
                "guessed_letters": hangman_game_instance.guessed_letters,
                "game_status": hangman_game_instance.game_status,
            }

            if hangman_game_instance.is_game_over():
                return render_template("GameOver.html", user=current_user)

    return render_template(
        "NewGame.html",
        game=game_document,
        chosen_letter=chosen_letter,
        user=current_user,
    )


# needs updating accordingly - when post and when get methods are called. Also update hangman_logic.py file that has HangmanGame class.abs
