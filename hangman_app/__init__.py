from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from .models.mongo_functions import MongoCRUD

db = SQLAlchemy()
DB_NAME = "database.db"

HOST = "localhost"
PORT = 27017
DATABASE_NAME = "Hangman_games"
# These should be parametrized and made global for sh and other scripts


game_db = MongoCRUD(host=HOST, port=PORT, database_name=DATABASE_NAME)


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config["SECRET_KEY"] = "hjshjhdjah kjshkjdhjs"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.jinja_env.globals["enumerate"] = enumerate

    db.init_app(app)

    from .routes.routes import main_routes
    from .routes.auth import auth
    from .routes.game_route import game_route

    app.register_blueprint(main_routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(game_route, url_prefix="/")
    from .models.models_sql import User

    with app.app_context():
        db.create_all()

    # from . import game_db

    # WORD_COLLECTION = "hangman_game_words"
    # game_db.generate_and_insert_words(collection_name=WORD_COLLECTION, word_count=2000)  # uncomment only if you want to add new words
    # game_db.create_game(
    #     game_collection_name="hangman_games",
    #     word_collection_name="hangman_game_words",
    #     user_id="1545",
    # )  <- it was just to try

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
