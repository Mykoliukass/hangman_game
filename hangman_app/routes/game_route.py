from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    session,
    redirect,
    url_for,
)
from flask_login import login_required, current_user
from bson import ObjectId
from configurations import configurations
from hangman_app import game_db
from hangman_app.game_logic.hangman_logic import HangmanGame
from hangman_app.logging_data.logging_module import (
    get_game_report_logger,
    get_error_reporting_logger,
)


game_report_logger = get_game_report_logger()
error_reporting_logger = get_error_reporting_logger()

game_route = Blueprint("game_route", __name__)


@game_route.route("/NewGame", methods=["GET", "POST"])
@login_required
def newgame():
    try:
        if request.method == "GET":
            if "hangman_game" not in session:
                # this whole mess creates a new game and adds it to the database. This is not made via hangman_logic, just to make hangman_logic to be a bit more universal.
                user_id = current_user.id
                hangman_game_instance = HangmanGame(user_id=user_id)
                collection = game_db.get_collection(
                    collection_name=configurations.GAME_COLLECTION_NAME
                )
                hangman_game_instance.random_word = game_db.get_random_word(
                    word_collection_name=configurations.WORD_COLLECTION_NAME
                )
                document = hangman_game_instance.create_game()
                result = collection.insert_one(document)
                hangman_game_instance.game_id = result.inserted_id
                game_report_logger.info("User %s started a new game", current_user.id)
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
                dictionary_after_guess = hangman_game_instance.make_a_guess(
                    chosen_letter
                )
                game_db.update_one_document(
                    collection_name=configurations.GAME_COLLECTION_NAME,
                    query={"_id": ObjectId(hangman_game_instance.game_id)},
                    update=dictionary_after_guess,
                )
                session["hangman_game"] = hangman_game_instance.to_json()

                if hangman_game_instance.is_game_over():
                    if hangman_game_instance.is_last_chance_needed():
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
                            today_games=game_db.get_games_played_today_or_to_date(
                                user_id=current_user.id,
                                game_collection_name=configurations.GAME_COLLECTION_NAME,
                                today=True,
                            ),
                        )
                        del session["hangman_game"]
                        return response

            whole_word_guess = request.form.get("whole_word")
            if whole_word_guess:
                document_after_guess = hangman_game_instance.guess_a_whole_word(
                    whole_word_guess
                )
                game_db.update_one_document(
                    collection_name=configurations.GAME_COLLECTION_NAME,
                    query={"_id": ObjectId(hangman_game_instance.game_id)},
                    update=document_after_guess,
                )
                session["hangman_game"] = hangman_game_instance.to_json()

                if hangman_game_instance.is_game_over():
                    response = render_template(
                        "GameOver.html",
                        user=current_user,
                        game=hangman_game_instance.to_json(),
                        today_games=game_db.get_games_played_today_or_to_date(
                            user_id=current_user.id,
                            game_collection_name=configurations.GAME_COLLECTION_NAME,
                            today=True,
                        ),
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

    except Exception as e:
        error_reporting_logger.error("An error occurred: %s", str(e), exc_info=True)

        return render_template("500.html"), 500
