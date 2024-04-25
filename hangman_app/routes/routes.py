from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    jsonify,
    session,
    redirect,
    url_for,
)
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
    if request.method == "GET":
        if "hangman_game" not in session:
            user_id = current_user.id
            hangman_game_instance = HangmanGame(user_id=user_id)
            hangman_game_instance.create_game()
            game_json = hangman_game_instance.to_json()
            session["hangman_game"] = game_json
        else:
            game_json = session.get("hangman_game")
            if game_json is None:
                flash("No game state found in session.", "error")
                return redirect(url_for("routes.home"))

            hangman_game_instance = HangmanGame.from_json(game_json)

        chosen_letter = None

    elif request.method == "POST":
        game_json = session.get("hangman_game")

        if game_json is None:
            flash("Game state could not be retrieved from session.", "error")
            return redirect(url_for("routes.home"))

        hangman_game_instance = HangmanGame.from_json(game_json)

        chosen_letter = request.form.get("letter")
        if chosen_letter:
            hangman_game_instance.make_a_guess(chosen_letter)
            session["hangman_game"] = hangman_game_instance.to_json()

            if hangman_game_instance.is_game_over():
                if (
                    hangman_game_instance.health_points == 0
                    or hangman_game_instance.guess_count == 0
                ):
                    return render_template(
                        "LastChance.html",
                        user=current_user,
                        game=hangman_game_instance.to_json(),
                    )
                else:
                    response = render_template(
                        "GameOver.html",
                        user=current_user,
                        game=hangman_game_instance.to_json(),
                        today_games=hangman_game_instance.get_games_played_today(),
                    )
                    del session["hangman_game"]
                    return response

        whole_word_guess = request.form.get("whole_word")
        if whole_word_guess:
            hangman_game_instance.guess_a_whole_word(whole_word_guess)
            session["hangman_game"] = hangman_game_instance.to_json()

            if hangman_game_instance.is_game_over():
                response = render_template(
                    "GameOver.html",
                    user=current_user,
                    game=hangman_game_instance.to_json(),
                    today_games=hangman_game_instance.get_games_played_today(),
                )
                del session["hangman_game"]
                return response

    if (
        request.method == "GET"
        and "hangman_game" in session
        and hangman_game_instance.is_game_over()
    ):
        del session["hangman_game"]

    return render_template(
        "NewGame.html",
        game=hangman_game_instance.get_game_document(),
        chosen_letter=chosen_letter,
        user=current_user,
    )
