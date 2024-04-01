from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from carproject import db, bcrypt
from carproject.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from carproject.models import User
from carproject.users.utils import save_picture, send_reset_email, send_confirmation_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, location=form.location.data)
        db.session.add(user)
        db.session.commit()
        send_confirmation_email(user)
        flash('Лист з підтвердженням реєстрації був надісланий!', 'info')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and not user.confirmed:
            flash('Неуспішний логін. Будь ласка підтвердіть вашу реєстрацію!', 'danger')
            return redirect(url_for('users.login'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))

        flash('Неуспішний логін. Будь ласка, перевірте запис пошти і пароль!', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'profile_pics', 125, 125)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Ваш акаунт було змінено!', 'success')
        return redirect(url_for('users.account'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.location.data = current_user.location

    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Аккаунт',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Лист з інструкцією до зміни паролю був надісланий на вашу пошту.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Зміна Паролю', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Цей токен є не валідним', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Ваш пароль було оновлено!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Зміна Паролю', form=form)

@users.route('/confirm/<token>')
def confirm_email(token):
    user = User.verify_reset_token(token)
    if user is not None:
        user.confirmed = True
        db.session.commit()
        flash('Ваш акаунт було підтверджено! Тепер ви можете увійти!', 'success')
    else:
        flash('Посилання не валідне або не дійсне.', 'danger')
    return redirect(url_for('users.login'))
