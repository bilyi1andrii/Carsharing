import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, CarForm
from flaskblog.models import User, Car



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

@app.route("/rating")
def tops():
    cars = Car.query.order_by(Car.rating.desc())
    return render_template('topcars.html', cars=cars)


@app.route("/car/new", methods=['GET', 'POST'])
@login_required
def new_car():
    form = CarForm()
    if form.validate_on_submit():
        car = Car(carname=form.carname.data,
                  type=form.type.data,
                  year=form.year.data,
                  engine_capacity=form.engine_capacity.data,
                  rating=form.rating.data,
                  price_per_hour=form.price_per_hour.data,
                  author=current_user)
        if form.picture.data:
            image = save_picture(form.picture.data, 'car_pics', 300, 500)
            car.image_file = image
        db.session.add(car)
        db.session.commit()
        flash('Your car has been posted!', 'success')
        return redirect(url_for('homepage'))
    return render_template('create_car.html', title='Car Submition',
                           form=form, legend='Car Submition')


@app.route("/questionnaire")
@login_required
def questionnaire():
    # if request.method == "POST":
    return render_template("questionnaire.html")


@app.route("/afterquestioning", methods=["GET", "POST"])
@login_required
def afterquestioning():
    # rf = request.form
    # tpl = (rf['primary_use'], rf['passengers'], rf['important_feature'], rf['vehicle_preference'], rf['budget'], rf['extra_space'])
    cars = Car.query.order_by(Car.rating.desc())
    # with sq.connect("super_cars.db") as con:
    #     cur = con.cursor()
    #     cur.execute("INSERT INTO user_preferences VALUES(NULL, ?, ?, ?, ?, ?, ?)", tpl)
    return render_template("afterquestioning.html", cars=cars)

@app.route("/carpage")
def carpage():
    # car = Car.query.get_or_404(car_id)
    return render_template('carpage.html')