from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

class CarForm(FlaskForm):
    carname = StringField('Назва вашого автомобіля', validators=[DataRequired(), Length(min=2, max=20)])

    choices_type = [('Седан', 'Седан'), ('Джип (SUV)', 'Джип (SUV)'), ('Купе', 'Купе'), ('Хетчбек', 'Хетчбек'), ('Мікро', 'Мікро')]
    type = SelectField('Укажіть тип автомобіля', choices=choices_type, validators=[DataRequired()])

    choices_usage = [('Робота', 'Для роботи'), ('Сімʼя', 'Поїздки із сімʼєю'), ('Місто', 'Поїздки містом'), ('Екстрім', 'Екстремальні подорожі')]
    usage = SelectField('Основний засіб використання', choices=choices_usage, validators=[DataRequired()])

    choices_art = [('Електрика', 'Електричний'), ('Гібрид', 'Гібридний'), ('Бензин', 'Бензинний'), ('Дизель', 'Дизельний')]
    art = SelectField('Вкажіть тип палива', choices=choices_art, validators=[DataRequired()])

    choices_location = [('12,Козловського,Львів', 'вулиця Козловського, 12'),
                        ('100,Ряшівська,Львів', 'вулиця Ряшівська, 100'),
                        ('16,Богданівська,Львів', 'вулиця Богданівська, 16'),
                        ('42,Джерельна,Львів', 'вулиця Джерельна, 42'),
                        ("2,Бойчука,Львів", "вулиця Бойчука, 2")]
    location = SelectField('Виберіть місце реєстрації вашого авто', choices=choices_location, validators=[DataRequired()])

    year = IntegerField('Рік (з 1990 по 2024)', validators=[DataRequired(),  NumberRange(min=1990, max=2024)])

    engine_capacity = FloatField('Потужність двигуна', validators=[DataRequired(), NumberRange(min=0, max=float('inf'))])
    price_per_hour = FloatField('Ціна за годину (грн)', validators=[DataRequired(), NumberRange(min=0, max=float('inf'))])



    picture = FileField('Зображення', validators=[FileAllowed(['png'])])
    submit = SubmitField('Опублікувати')