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


@routes.route("/History", methods=["GET", "POST"])
@login_required
def history():
    game_history = game_db.get_games_played_total(
        game_collection_name=HangmanGame.get_game_collection_name(),
        user_id=current_user.id,
    )
    return render_template("history.html", user=current_user, game_history=game_history)


@routes.route("/NewGame", methods=["GET", "POST"])
@login_required
def newgame():
    global hangman_game_instance
    game_document = None

    if request.method == "GET":
        user_id = current_user.id
        hangman_game_instance = HangmanGame(user_id=user_id)
        print("New game instance created:", hangman_game_instance)
        game_document = hangman_game_instance.get_game_document()
        chosen_letter = None
    elif request.method == "POST":
        chosen_letter = request.form.get("letter")

        if chosen_letter:
            hangman_game_instance.make_a_guess(chosen_letter)
            game_document = hangman_game_instance.get_game_document()

            if hangman_game_instance.is_game_over():
                if (
                    hangman_game_instance.health_points == 0
                    or hangman_game_instance.guess_count == 0
                ):
                    return render_template(
                        "last_chance.html", user=current_user, game=game_document
                    )
                else:
                    return render_template(
                        "GameOver.html",
                        user=current_user,
                        game=game_document,
                        today_games=hangman_game_instance.get_games_played_today(),
                    )

        whole_word_guess = request.form.get("whole_word")
        if whole_word_guess:
            hangman_game_instance.guess_a_whole_word(whole_word_guess)

            if hangman_game_instance.is_game_over():
                game_document = hangman_game_instance.get_game_document()
                return render_template(
                    "GameOver.html",
                    user=current_user,
                    game=game_document,
                    today_games=hangman_game_instance.get_games_played_today(),
                )

    return render_template(
        "NewGame.html",
        game=game_document,
        chosen_letter=chosen_letter,
        user=current_user,
    )
