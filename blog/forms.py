from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, ValidationError, FileField
from .models import User


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя: ', validators=[validators.DataRequired()])
    password = PasswordField('Пароль: ', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')
    ])
    confirm = PasswordField('Повторите пароль: ')
    submit = SubmitField("Создать пользователя")

    # def validate_username(self, field):
    #     if User.query.filter_by(username=field.data).first():
    #         raise ValidationError('Username already in use.')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя: ', validators=[validators.DataRequired()])
    password = PasswordField('Пароль: ', validators=[validators.DataRequired()])
    submit = SubmitField("Войти")


