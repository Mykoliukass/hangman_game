from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Game
from . import db

routes = Blueprint("routes", __name__)


@routes.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("home.html", user=current_user)
