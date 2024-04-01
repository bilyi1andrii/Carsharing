import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from carproject.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Імʼя Користувача',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Пошта',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=float('inf'))])
    confirm_password = PasswordField('Підтвердіть Пароль',
                                     validators=[DataRequired()])
    location = StringField('Поточне Місце Розташування', validators=[DataRequired()])
    submit = SubmitField('Зареєструватись')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Ця пошта зайнята. Будь ласка виберіть іншу.')

    def validate_password(self, password):
        pattern=re.compile(r'^(?=.*\d)(?=.*[A-ZА-Я]).{8,}$')
        if not pattern.match(password.data):
            raise ValidationError('Неправильний пароль. Пароль має містити букви, цифри і велику літеру (англійської або української мови)')

    def validate_location(self, location):
        pattern = r'^\d{1,3},\s*(?:[\w\s]+),\s*(?:[\w\s]+)$'

        regex = re.compile(pattern, re.IGNORECASE | re.UNICODE)

        if not regex.match(location.data):
            raise ValidationError('Неправильний запис вулиці, буль ласка напишіть у такому форматі: номер(тільки цифри), назва вулиці, місто')


class LoginForm(FlaskForm):
    email = StringField('Пошта',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запамʼятати мене')
    submit = SubmitField('Увійти')

class UpdateAccountForm(FlaskForm):
    username = StringField('Імʼя Користувача',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Пошта',
                        validators=[DataRequired(), Email()])
    location = StringField('Поточне Місце Розташування', validators=[DataRequired()])
    picture = FileField('Змінити Зображення Профілю', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Оновити')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Ця пошта зайнята. Будь ласка виберіть іншу.')

    def validate_location(self, location):
        pattern = r'^\d{1,3},\s*(?:[\w\s]+),\s*(?:[\w\s]+)$'

        regex = re.compile(pattern, re.IGNORECASE | re.UNICODE)

        if not regex.match(location.data):
            raise ValidationError('Неправильний запис вулиці, буль ласка напишіть у такому форматі: номер(тільки цифри), назва вулиці, місто')

class RequestResetForm(FlaskForm):
    email = StringField('Пошта',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Запросити Дозвіл')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Немає акаунту, зареєстрованого з такою поштою. Будь ласка, зареєструйтесь.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Підтвердіть Пароль',
                                     validators=[DataRequired()])
    submit = SubmitField('Оновити Пароль')

    def validate_password(self, password):
        pattern=re.compile(r'^(?=.*\d)(?=.*[A-ZА-Я]).{8,}$')
        if not pattern.match(password.data):
            raise ValidationError('Неправильний пароль. Пароль має містити букви, цифри і велику літеру (англійської або української мови)')