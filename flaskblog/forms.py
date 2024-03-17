from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Length, Email, ValidationError, NumberRange
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=float('inf'))])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_password(self, password):
        pass

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
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')


class CarForm(FlaskForm):
    carname = StringField('Name', validators=[DataRequired()])

    choices_type = [('Седан', 'Седан'), ('Джип (SUV)', 'Джип (SUV)'), ('Купе', 'Купе'), ('Хетчбек', 'Хетчбек'), ('Мікро', 'Мікро')]
    type = SelectField('Car Type', choices=choices_type, validators=[DataRequired()])

    choices_usage = [('Робота', 'Для роботи'), ('Сімʼя', 'Поїздки із сімʼєю'), ('Місто', 'Поїздки містом'), ('Екстрім', 'Екстремальні подорожі')]
    usage = SelectField('Main Usage', choices=choices_usage, validators=[DataRequired()])

    choices_art = [('Електрика', 'Електричний'), ('Гібрид', 'Гібридний'), ('Бензин', 'Бензинний'), ('Дизель', 'Дизельний')]
    art = SelectField('Art', choices=choices_art, validators=[DataRequired()])

    year = IntegerField('Year', validators=[DataRequired(),  NumberRange(min=1990, max=2024)])
    engine_capacity = FloatField('Engine Capacity', validators=[DataRequired(), NumberRange(min=0, max=float('inf'))])
    price_per_hour = FloatField('Price per Hour', validators=[DataRequired(), NumberRange(min=0, max=float('inf'))])

    picture = FileField('Car Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')


class AnswersForm(FlaskForm):
    choices1 = [('Робота', 'Поїздки на роботу'), ('Сімʼя', 'Сімейні подорожі'), ('Місто', 'Поїздки по місту'), ('Екстрім', 'Пригодницькі/екстремальні дороги')]
    usage = SelectField('Яким буде основне використання транспортного засобу?', choices=choices1, validators=[DataRequired()])

    choices2 = [(1, '1-2'), (2, '3-4'), (3, '5-6')]
    size = SelectField('На скількох людей розрахована машина?', choices=choices2, validators=[DataRequired()])

    choices3 = [('Електрика', 'Електричний'), ('Гібрид', 'Гібридний'), ('Бензин', ' Бензинний'), ('Дизель', 'Дизельний')]
    art = SelectField('Якому типу автомобілей ви віддаєте перевагу?', choices=choices3, validators=[DataRequired()])

    choices4 = [("1,29", 'Економний'), ("30,79", 'Стандартний'), ("79,1000000", 'Преміум')]
    afford = SelectField('На яку цінову категорію автомобілей ви розраховуєте?', choices=choices4, validators=[DataRequired()])

    choices5 = [('Рік', 'Рік випуску'), ('Двигун', 'Потужність двигуна'), ('Рейтинг', 'Рейтинг машини')]
    preference = SelectField('На яку властивість автомобіля ви зважаєте найбільше?', choices=choices5, validators=[DataRequired()])

    submit = SubmitField('Submit')
