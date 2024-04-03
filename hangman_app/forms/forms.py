from flask_wtf import FlaskForm
from wtforms import (
    SubmitField,
    BooleanField,
    StringField,
    PasswordField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo
from hangman_app.models import User


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirmed_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", "Passwords must match.")],
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "This username is already taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                "This email address is already taken. Please choose a different one."
            )


class SignInForm(FlaskForm):
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField("Remmember me")
    submit = SubmitField("Sign in")
