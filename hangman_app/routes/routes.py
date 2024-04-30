from collections import defaultdict
from datetime import datetime
from flask import Blueprint, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from hangman_app import game_db
from hangman_app.game_logic.hangman_logic import HangmanGame
from hangman_app.logging.logging_module import get_error_reporting_logger
from hangman_app.models.models_sql import User


main_routes = Blueprint("main_routes", __name__)
error_reporting_logger = get_error_reporting_logger()


@main_routes.route("/", methods=["GET"])
@login_required
def home():
    return render_template("home.html", user=current_user)


@main_routes.route("/History", methods=["GET"])
@login_required
def history():
    game_history = game_db.get_games_played_today_or_to_date(
        user_id=current_user.id,
        game_collection_name=HangmanGame.get_game_collection_name(),
    )
    return render_template("history.html", user=current_user, game_history=game_history)


@main_routes.route("/Top10", methods=["GET"])
@login_required
def get_top_10():
    try:
        # Retrieve winning games
        win_games = game_db.find_documents(
            collection_name=HangmanGame.get_game_collection_name(),
            query={"game_status": {"$in": ["Won", "Won after the last chance"]}},
        )

        wins_count = defaultdict(int)
        most_recent_win = defaultdict(lambda: None)

        # Process each game
        for game in win_games:
            user_id = game.get("user_id")
            wins_count[user_id] += 1

            # Update the most recent win date
            win_date = game.get("game_date")
            if win_date:
                # Convert date to datetime object for comparison
                win_date_obj = datetime.strptime(win_date, "%Y-%m-%d")
                if (
                    most_recent_win[user_id] is None
                    or win_date_obj > most_recent_win[user_id]
                ):
                    most_recent_win[user_id] = win_date_obj

        # Create a list of tuples (user_id, wins count, and most recent win date)
        win_list = [
            (user_id, wins, most_recent_win[user_id])
            for user_id, wins in wins_count.items()
        ]
        # Sort by wins count and most recent win date
        top_10_winners = sorted(win_list, key=lambda x: (x[1], x[2]), reverse=True)[:10]

        top10_players = []
        for user_id, wins, _ in top_10_winners:
            # Look up user in the database
            user = User.query.filter_by(id=user_id).first()
            if user:
                # Add user data to the list
                top10_players.append(
                    {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "wins": wins,
                    }
                )

        # Render the template with the top 10 players
        return render_template(
            "Top10.html", top10_players=top10_players, user=current_user
        )

    except Exception as e:
        # Log and handle any errors
        error_reporting_logger.error(
            "Error fetching top 10 players: %s", str(e), exc_info=True
        )
        flash("An error occurred while retrieving the top 10 players.", "error")
        return redirect(url_for("main_routes.home"))
