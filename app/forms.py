from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, FileField
from wtforms.validators import DataRequired
import sqlalchemy as sa
from app import db

ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png']

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class EquipmentForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    territory = StringField("Корпус")
    office = StringField('Кабинет')
    description = TextAreaField('Описание')
    image = FileField('Изображение', validators=[FileAllowed(ALLOWED_IMAGE_EXTENSIONS, 'Только изображения (jpg, jpeg, png)!')])
    submit = SubmitField('Добавить')


