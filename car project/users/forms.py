import re
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from carproject.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=float('inf'))])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])
    location = StringField('Current Location', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

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
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    location = StringField('Current Location', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_password(self, password):
        pattern=re.compile(r'^(?=.*\d)(?=.*[A-ZА-Я]).{8,}$')
        if not pattern.match(password.data):
            raise ValidationError('Неправильний пароль. Пароль має містити букви, цифри і велику літеру (англійської або української мови)')