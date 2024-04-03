import os
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, logout_user, login_user, login_required
from datetime import datetime
import secrets
from hangman_app import db
from hangman_app.forms import SignUpForm, SignInForm, LoginForm
from hangman_app.models import User
from flask_bcrypt import bcrypt
from hangman_app import app


# @app.route("/register", methods=["GET", "POST"])
# def signup():
#     db.create_all()
#     if current_user.is_authenticated:
#         return redirect(url_for("index"))
#     form = SignUpForm()
#     if form.validate_on_submit():
#         encrypted_password = bcrypt.generate_password_hash(
#             form.slaptazodis.data
#         ).decode("utf-8")
#         user = User(
#             username=form.username.data,
#             email=form.email.data,
#             password=encrypted_password,
#         )
#         db.session.add(user)
#         db.session.commit()
#         flash("Sėkmingai prisiregistravote! Galite prisijungti", "success")
#         return redirect(url_for("index"))
#     return render_template("register.html", title="Register", form=form)


# @app.route("/signin", methods=["GET", "POST"])
# def signin():
#     if current_user.is_authenticated:
#         return redirect(url_for("index"))
#     form = SignInForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and bcrypt.check_password_hash(user.password, form.password.data):
#             login_user(user, remember=form.remember.data)
#             next_page = request.args.get("next")
#             return redirect(next_page) if next_page else redirect(url_for("index"))
#         else:
#             flash(
#                 "Prisijungti nepavyko. Patikrinkite el. paštą ir slaptažodį", "danger"
#             )
#     return render_template("login.html", title="Signin", form=form)


# @app.route("/logout")
# def logout():
#     logout_user()
#     return redirect(url_for("index"))


# @app.route("/irasai")
# @login_required
# def records():
#     db.create_all()
#     page = request.args.get("page", 1, type=int)
#     visi_irasai = (
#         Irasas.query.filter_by(vartotojas_id=current_user.id)
#         .order_by(Irasas.data.desc())
#         .paginate(page=page, per_page=5)
#     )
#     return render_template("irasai.html", visi_irasai=visi_irasai, datetime=datetime)


# @app.route("/naujas_irasas", methods=["GET", "POST"])
# def new_record():
#     db.create_all()
#     forma = IrasasForm()
#     if forma.validate_on_submit():
#         naujas_irasas = Irasas(
#             pajamos=forma.pajamos.data,
#             suma=forma.suma.data,
#             vartotojas_id=current_user.id,
#         )
#         db.session.add(naujas_irasas)
#         db.session.commit()
#         flash(f"Įrašas sukurtas", "success")
#         return redirect(url_for("records"))
#     return render_template("prideti_irasa.html", form=forma)


# @app.route("/delete/<int:id>")
# def delete(id):
#     irasas = Irasas.query.get(id)
#     db.session.delete(irasas)
#     db.session.commit()
#     return redirect(url_for("records"))


# @app.route("/update/<int:id>", methods=["GET", "POST"])
# def update(id):
#     forma = IrasasForm()
#     irasas = Irasas.query.get(id)
#     if forma.validate_on_submit():
#         irasas.pajamos = forma.pajamos.data
#         irasas.suma = forma.suma.data
#         db.session.commit()
#         return redirect(url_for("records"))
#     return render_template("update.html", form=forma, irasas=irasas)


# @app.route("/balansas")
# def balance():
#     try:
#         visi_irasai = Irasas.query.filter_by(vartotojas_id=current_user.id)
#     except:
#         visi_irasai = []
#     balansas = 0
#     for irasas in visi_irasai:
#         if irasas.pajamos:
#             balansas += irasas.suma
#         else:
#             balansas -= irasas.suma
#     return render_template("balansas.html", balansas=balansas)


# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, "static/profilio_nuotraukos", picture_fn)

#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)

#     return picture_fn


# @app.route("/paskyra", methods=["GET", "POST"])
# @login_required
# def paskyra():
#     form = PaskyrosAtnaujinimoForma()
#     if form.validate_on_submit():
#         if form.nuotrauka.data:
#             nuotrauka = save_picture(form.nuotrauka.data)
#             current_user.nuotrauka = nuotrauka
#         current_user.vardas = form.vardas.data
#         current_user.el_pastas = form.el_pastas.data
#         db.session.commit()
#         flash("Tavo paskyra atnaujinta!", "success")
#         return redirect(url_for("paskyra"))
#     elif request.method == "GET":
#         form.vardas.data = current_user.vardas
#         form.el_pastas.data = current_user.el_pastas
#     nuotrauka = url_for(
#         "static", filename="profilio_nuotraukos/" + current_user.nuotrauka
#     )
#     return render_template(
#         "paskyra.html", title="Account", form=form, nuotrauka=nuotrauka
#     )


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/reset_password", methods=["GET", "POST"])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for("home"))
#     form = UzklausosAtnaujinimoForma()
#     if form.validate_on_submit():
#         user = Vartotojas.query.filter_by(el_pastas=form.el_pastas.data).first()
#         send_reset_email(user)
#         flash(
#             "Jums išsiųstas el. laiškas su slaptažodžio atnaujinimo instrukcijomis.",
#             "info",
#         )
#         return redirect(url_for("prisijungti"))
#     return render_template("reset_request.html", title="Reset Password", form=form)


# @app.route("/reset_password/<token>", methods=["GET", "POST"])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for("home"))
#     user = Vartotojas.verify_reset_token(token)
#     if user is None:
#         flash("Užklausa netinkama arba pasibaigusio galiojimo", "warning")
#         return redirect(url_for("reset_request"))
#     form = SlaptazodzioAtnaujinimoForma()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.slaptazodis.data).decode(
#             "utf-8"
#         )
#         user.slaptazodis = hashed_password
#         db.session.commit()
#         flash("Tavo slaptažodis buvo atnaujintas! Gali prisijungti", "success")
#         return redirect(url_for("prisijungti"))
#     return render_template("reset_token.html", title="Reset Password", form=form)


# @app.errorhandler(404)
# def klaida_404(klaida):
#     return render_template("404.html"), 404


# @app.errorhandler(403)
# def klaida_403(klaida):
#     return render_template("403.html"), 403


# @app.errorhandler(500)
# def klaida_500(klaida):
#     return render_template("500.html"), 500
