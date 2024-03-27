from flask import render_template, Blueprint, session
from flask_login import login_required, current_user
from carproject.models import Car

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/homepage")
def homepage():
    cars = Car.query.paginate(per_page=18)
    return render_template('homepage.html', cars=cars)

@main.route("/FAQ")
def faq():
    return render_template('FAQ.html', title='Frequently Asked Questions')

@main.route("/rating/<int:number>/<string:carsy>")
def tops(number, carsy):
    if carsy != 'Седа':
        cars = Car.query.filter_by(type=carsy).order_by(Car.rating.desc()).paginate(per_page=number)
    else:
        cars = Car.query.order_by(Car.rating.desc()).paginate(per_page=number)
    return render_template('topcars.html', cars=cars)

@main.route("/afterquestioning/<string:carsy>")
@login_required
def afterquestioning(carsy):
    serialized_cars = session.get('cars', [])
    cars = [Car.from_json(car_data) for car_data in serialized_cars]
    if carsy != 'Седа':
        cars = [car for car in cars if car.type == carsy]
    return render_template("afterquestioning.html", cars=cars)


@main.route("/calendar")
def calendar():
    return render_template('calendar.html', title='calendar')

@main.route("/message")
def message():
    return render_template('message.html', title='message', user=current_user)
