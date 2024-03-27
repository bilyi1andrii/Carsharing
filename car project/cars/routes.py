import random
from flask import render_template, url_for, flash, redirect, Blueprint, abort
from flask_login import current_user, login_required
from carproject import db
from carproject.cars.forms import CarForm
from carproject.models import Car
from carproject.users.utils import save_picture

CAR_TYPES = {
    'Седан': 2,
    'Хетчбек': 2,
    'Купе': 2,
    'Джип (SUV)': 3,
    'Мікро': 1,
}

cars = Blueprint('cars', __name__)

@cars.route("/car/new", methods=['GET', 'POST'])
@login_required
def new_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(carname=form.carname.data,
                  type=form.type.data,
                  usage = form.usage.data,
                  art = form.art.data,
                  year=form.year.data,
                  location=form.location.data,
                  engine_capacity=form.engine_capacity.data,
                  price_per_hour=form.price_per_hour.data,
                  author=current_user)
        if form.picture.data:
            image = save_picture(form.picture.data, 'car_pics', 600, 800)
            car.image_file = image

        car.size = CAR_TYPES.get(car.type)
        car.rating = random.randrange(1, 6)

        db.session.add(car)
        db.session.commit()
        flash('Your car has been posted!', 'success')
        return redirect(url_for('main.homepage'))
    return render_template('create_car.html', title='Car Submition',
                           form=form, legend='Car Submition')

@cars.route("/car/<int:car_id>")
@login_required
def carpage(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('carpage.html', car=car)

@cars.route("/car/<int:car_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    if car.author != current_user:
        abort(403)
    db.session.delete(car)
    db.session.commit()
    flash('Your car has been deleted!', 'success')
    return redirect(url_for('main.homepage'))

@cars.route("/account/<int:user_id>/mycars", methods=['GET', 'POST'])
@login_required
def mycars(user_id):
    if user_id != current_user.id:
        abort(403)
    carss = Car.query.filter_by(user_id=user_id)
    return render_template('user_cars.html', cars=carss)
