from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField
from wtforms.validators import DataRequired
import sqlalchemy as sa
from app import db

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    # password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EquipmentForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    territory = StringField("Корпус")
    office = StringField('Кабинет')
    description = TextAreaField('Описание')
    submit = SubmitField('Добавить')