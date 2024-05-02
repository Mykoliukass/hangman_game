from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from configurations import configurations
from .models.mongo_functions import MongoCRUD

db = SQLAlchemy()
DB_NAME = configurations.FLASK_DB_NAME
game_db = MongoCRUD(
    host=configurations.MONGO_HOST,
    port=configurations.MONGO_PORT,
    database_name=configurations.DATABASE_NAME,
)


def create_app():
    app = Flask(__name__, static_folder="static")

    app.config["SECRET_KEY"] = configurations.FLASK_SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = configurations.SQLALCHEMY_DATABASE_URI
    app.jinja_env.globals["enumerate"] = enumerate

    db.init_app(app)

    @app.errorhandler(400)
    def handle_400_error(error):
        return render_template("400.html"), 400

    @app.errorhandler(404)
    def handle_404_error(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def handle_500_error(error):
        return render_template("500.html"), 500

    from .routes.routes import main_routes
    from .routes.auth import auth
    from .routes.game_route import game_route

    app.register_blueprint(main_routes, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(game_route, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models.models_sql import User

        return db.session.query(User).get(int(user_id))

    with app.app_context():
        db.create_all()

    return app


def create_database(app):
    if not path.exists(
        "website/" + configurations.SQLALCHEMY_DATABASE_URI.split("/")[-1]
    ):
        with app.app_context():
            db.create_all()
        print("Database created successfully")
