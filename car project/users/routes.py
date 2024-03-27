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
        flash('An email to confirm your registration was sent', 'info')
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
            flash('Login Unsuccessful. Please verify your registration', 'danger')
            return redirect(url_for('users.login'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.homepage'))

        flash('Login Unsuccessful. Please check email and password', 'danger')
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
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.location.data = current_user.location

    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)

@users.route('/confirm/<token>')
def confirm_email(token):
    user = User.verify_reset_token(token)
    if user is not None:
        user.confirmed = True
        db.session.commit()
        flash('Your account has been confirmed!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('users.login'))
