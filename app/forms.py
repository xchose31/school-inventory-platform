from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, FileField, SelectField
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
    territory = SelectField(
        'Территория',
        choices=[('альфа', 'Альфа'), ('бета', 'Бета'), ('гамма', 'Гамма'), ('дельта 1', 'Дельта 1'),
                 ('дельта 2', 'Дельта 2'), ('дельта 3', 'Дельта 3'), ('дельта 4', 'Дельта 4'), ('дельта 5', 'Дельта 5'),
                 ('дельта 6', 'Дельта 6')]
    )
    office = SelectField(
        'Кабинет',
        choices=[('101', '101'), ('102', '102'), ('103', '103'), ('104', '104'), ('105', '105'), ('106', '106'),
                 ('107', '107'), ('108', '108')]
    )
    description = TextAreaField('Описание')
    image = FileField('Изображение',
                      validators=[FileAllowed(ALLOWED_IMAGE_EXTENSIONS, 'Только изображения (jpg, jpeg, png)!')])
    equipment_type = SelectField(
        'Тип оборудования',
        choices=[('', 'Выберите...'), ('учебное', 'Учебное'), ('техническое', 'Техническое')])

    subject = SelectField(
        'Предмет',
        choices=[('', 'Выберите...'),
                 ('физика', 'Физика'),
                 ('информатика', 'Информатика'),
                 ('химия', 'Химия'),
                 ('биология', 'Биология'),
                 ('математика', 'Математика'),
                 ('физкультура', 'Физкультура'),
                 ('история', 'История'),
                 ('технология', 'Технология')]
    )

    submit = SubmitField('Добавить')
