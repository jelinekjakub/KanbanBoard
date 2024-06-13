from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.models import User


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Heslo", validators=[DataRequired()])


class RegisterForm(FlaskForm):
    username = StringField(
        "Jméno", validators=[DataRequired(), Length(min=3, max=40)]
    )
    email = EmailField(
        "Email", validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        "Heslo", validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        "Heslo znovu",
        validators=[
            DataRequired(),
        ],
    )

    def validate(self, extra_validators=None):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user_w_email = User.query.filter_by(email=self.email.data).first()
        if user_w_email:
            self.email.errors.append("Tento email je již zaregistrován. ")
            return False
        user_w_username = User.query.filter_by(username=self.username.data).first()
        if user_w_username:
            self.username.errors.append("Toto uživatelské jméno je již zaregistrované. ")
            return False
        if self.password.data != self.confirm.data:
            self.password.errors.append("Hesla se musí shodovat. ")
            return False
        return True
