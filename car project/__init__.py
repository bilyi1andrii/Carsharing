from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from carproject.config import Config
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from carproject.users.routes import users
    from carproject.cars.routes import cars
    from carproject.main.routes import main
    from carproject.quests.routes import quests
    from carproject.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(cars)
    app.register_blueprint(main)
    app.register_blueprint(quests)
    app.register_blueprint(errors)

    return app

