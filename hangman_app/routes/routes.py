from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from hangman_app import db, game_db
from bson import ObjectId
from hangman_app.game_logic.hangman_logic import HangmanGame
from collections import defaultdict
from hangman_app.models.models_sql import User

main_routes = Blueprint("main_routes", __name__)


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
    win_games = game_db.find_documents(
        collection_name=HangmanGame.get_game_collection_name(),
        query={"game_status": {"$in": ["Won", "Won after the last chance"]}},
    )

    wins_count = defaultdict(int)
    most_recent_win = defaultdict(lambda: None)

    for game in win_games:
        user_id = game["user_id"]
        wins_count[user_id] += 1

        # win date for each user
        win_date = game.get("date", None)
        if win_date:
            if most_recent_win[user_id] is None or win_date > most_recent_win[user_id]:
                most_recent_win[user_id] = win_date

    # list of user_id, wins count, and most recent win date tuples
    win_list = [
        (user_id, wins, most_recent_win[user_id])
        for user_id, wins in wins_count.items()
    ]

    # sorting by win count and by last win date
    top_10_winners = sorted(win_list, key=lambda x: (x[1], x[2]), reverse=True)[:10]

    top10_players = []
    for user_id, wins, _ in top_10_winners:
        user = User.query.filter_by(id=user_id).first()
        if user:
            top10_players.append(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "wins": wins,
                }
            )

    return render_template("Top10.html", top10_players=top10_players, user=current_user)
