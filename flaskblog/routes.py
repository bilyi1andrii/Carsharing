import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy import and_
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, CarForm, AnswersForm
from flaskblog.models import User, Car, CAR_TYPES



@app.route("/")
@app.route("/homepage")
def homepage():
    cars = Car.query.all()
    return render_template('homepage.html', cars=cars)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('homepage'))

        flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homepage'))

def save_picture(form_picture, way: str, size_ox: int, size_oy: int):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, f'static/{way}', picture_fn)

    output_size = (size_ox, size_oy)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'profile_pics', 125, 125)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route("/FAQ")
def faq():
    return render_template('FAQ.html', title='Frequently Asked Questions')

@app.route("/rating/<int:number>/<string:carsy>")
def tops(number, carsy):
    if carsy != 'Седа':
        cars = Car.query.filter_by(type=carsy).order_by(Car.rating.desc()).paginate(per_page=number)
    else:
        cars = Car.query.order_by(Car.rating.desc()).paginate(per_page=number)
    return render_template('topcars.html', cars=cars)


@app.route("/car/new", methods=['GET', 'POST'])
@login_required
def new_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(carname=form.carname.data,
                  type=form.type.data,
                  usage = form.usage.data,
                  art = form.art.data,
                  year=form.year.data,
                  engine_capacity=form.engine_capacity.data,
                  price_per_hour=form.price_per_hour.data,
                  author=current_user)
        if form.picture.data:
            image = save_picture(form.picture.data, 'car_pics', 300, 500)
            car.image_file = image

        car.size = CAR_TYPES.get(car.type)

        db.session.add(car)
        db.session.commit()
        flash('Your car has been posted!', 'success')
        return redirect(url_for('homepage'))
    return render_template('create_car.html', title='Car Submition',
                           form=form, legend='Car Submition')


def pick_the_best(cars, answer: str):
    if answer == 'Рік':
        new = sorted(cars, key= lambda x: x.year, reverse=True)
    elif answer == 'Двигун':
        new = sorted(cars, key= lambda x: x.engine_capacity, reverse=True)
    else:
        new = sorted(cars, key= lambda x: x.rating, reverse=True)
    return new


@app.route("/questionnaire", methods=['GET', 'POST'])
@login_required
def questionnaire():
    form = AnswersForm()
    if form.validate_on_submit():
        num1, num2 = list(map(int, form.afford.data.split(',')))
        cars = Car.query.filter(and_(Car.usage == form.usage.data,
                                Car.art == form.art.data,
                                Car.size >= form.size.data,
                                Car.price_per_hour >= num1,
                                Car.price_per_hour < num2))

        # find_affor(cars, rng[0], rng[1])
        answer = form.preference.data
        cars = pick_the_best(cars, answer)
        serialized_cars = [car.to_json() for car in cars]
        session['cars'] = serialized_cars
        return redirect(url_for('afterquestioning', carsy='Седа'))

    return render_template("questionnaire.html", form=form)


@app.route("/afterquestioning/<string:carsy>")
@login_required
def afterquestioning(carsy):
    serialized_cars = session.get('cars', [])
    cars = [Car.from_json(car_data) for car_data in serialized_cars]
    if carsy != 'Седа':
        cars = [car for car in cars if car.type == carsy]
    return render_template("afterquestioning.html", cars=cars)

@app.route("/car/<int:car_id>")
def carpage(car_id):
    car = Car.query.get_or_404(car_id)
    return render_template('carpage.html', car=car)
