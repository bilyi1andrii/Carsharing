import random
from flaskblog import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    cars = db.relationship('Car', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    carname = db.Column(db.String(30), unique=True, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    usage = db.Column(db.String, nullable=False)
    art = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    engine_capacity = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.String(100), default='default_car.jpg')
    rating = db.Column(db.Float, default=random.randrange(1, 6))
    price_per_hour = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f'Car({self.carname}, {self.type}, {self.year})'

    def to_json(self):
        return {
            'id': self.id,
            'carname': self.carname,
            'type': self.type,
            'usage': self.usage,
            'art': self.art,
            'size': self.size,
            'user_id': self.user_id,
            'year': self.year,
            'engine_capacity': self.engine_capacity,
            'image_file': self.image_file,
            'rating': self.rating,
            'price_per_hour': self.price_per_hour,
                }

    @staticmethod
    def from_json(json_data):
        return Car(
            carname=json_data['carname'],
            type=json_data['type'],
            usage=json_data['usage'],
            art=json_data['art'],
            size=json_data['size'],
            user_id=json_data['user_id'],
            year=json_data['year'],
            engine_capacity=json_data['engine_capacity'],
            image_file=json_data['image_file'],
            id=json_data['id'],
            rating=json_data['rating'],
            price_per_hour=json_data['price_per_hour'],
            )

CAR_TYPES = {
    'Седан': 2,
    'Хетчбек': 2,
    'Купе': 2,
    'Джип (SUV)': 3,
    'Мікро': 1,
}
