from flask import render_template, url_for, redirect, session, Blueprint, request, flash, abort
from flask_login import login_required, current_user
from sqlalchemy import and_
from carproject.models import Car
from carproject.quests.utils import find_shortest_location, pick_the_best



quests = Blueprint('quests', __name__)
answers_dict = {}

@quests.route("/quest1", methods=["GET", "POST"])
@login_required
def quest1():
    return render_template("quests/quest1.html")


@quests.route("/quest2", methods=["GET", "POST"])
@login_required
def quest2():
    if request.method == "POST":
        answers_dict["Q1"] = request.form["Q1"]
        return render_template("quests/quest2.html")
    abort(403)


@quests.route("/quest3", methods=["GET", "POST"])
@login_required
def quest3():
    if request.method == "POST":
        answers_dict["Q2"] = int(request.form["Q2"])
        return render_template("quests/quest3.html")
    abort(403)


@quests.route("/quest4", methods=["GET", "POST"])
@login_required
def quest4():
    if request.method == "POST":
        answers_dict["Q3"] = request.form["Q3"]
        return render_template("quests/quest4.html")
    abort(403)


@quests.route("/quest5", methods=["GET", "POST"])
@login_required
def quest5():
    if request.method == "POST":
        answers_dict["Q4"] = request.form["Q4"]
        return render_template("quests/quest5.html")
    abort(403)

@quests.route("/quest6", methods=["GET", "POST"])
@login_required
def quest6():
    if request.method == "POST":
        answers_dict["Q5"] = request.form["Q5"]
        return render_template("quests/quest6.html")
    abort(403)

@quests.route("/questionnaire", methods=['GET', 'POST'])
@login_required
def questionnaire():
    if request.method == "POST":
        answers_dict["Q6"] = request.form["Q6"]
        best_location = answers_dict['Q6']
        if best_location == 'Best':
            best_location = find_shortest_location(current_user.location)
        if best_location is None:
            flash('Адреса яку ви ввели є неіснуючою! Будь ласка, більше так не робіть', 'danger')
            return redirect(url_for('main.homepage'))
        num1, num2 = list(map(int, answers_dict['Q4'].split(',')))
        cars = Car.query.filter_by(location=best_location).filter(and_(Car.usage == answers_dict["Q1"],
                                Car.art == answers_dict["Q3"],
                                Car.size >= answers_dict["Q2"],
                                Car.price_per_hour >= num1,
                                Car.price_per_hour < num2))

        answer = answers_dict["Q5"]
        cars = pick_the_best(cars, answer)
        serialized_cars = [car.to_json() for car in cars]
        session['cars'] = serialized_cars
        return redirect(url_for('main.afterquestioning', carsy='Седа'))
    abort(403)