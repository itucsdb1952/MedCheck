from flask import render_template, session, redirect, url_for

from models import *
from views import functions
from views.functions import let_to


@let_to(['admin', 'doctor', 'normal'])
def home_page():
    user_auth = session['user_auth']
    if user_auth == 'admin':
        hospitals = functions.get_hospitals_with_place()
        return render_template('admin.html', hospitals=hospitals, user_auth=user_auth)
    elif user_auth == 'doctor':
        doctor = Doctor(Human(tc=session['user_tc']).get_object()).get_object()
        histories = History(doctor=doctor).get_objects()
        return render_template("doctor_history.html", histories=histories,
                               user_auth=session['user_auth'])  # user_auth: for navbar
    elif user_auth == 'normal':
        places = Place().get_objects(distinct_city=True)
        cities = [place.city for place in places]
        return render_template('user_home.html', cities=cities, user_auth=user_auth)


@let_to(['admin'])
def admin_places_page():
    return render_template('admin_places.html', user_auth='admin')


@let_to(['admin'])
def admin_hospitals_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]

    return render_template('admin_hospitals.html', cities=cities, user_auth='admin')


@let_to(['admin'])
def admin_humans_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]

    return render_template('admin_humans.html', cities=cities, user_auth='admin')


def hospital_patient_page():
    return render_template('hospital_patient.html')


def login_page():
    if 'user_tc' and 'user_auth' in session:
        return redirect(url_for(home_page.__name__))
    else:
        return render_template("login.html")


def register_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]
    return render_template("Register.html", cities=cities)


def how_to_use_page():
    return render_template("How to Use.html", user_auth=session['user_auth'])


def forbidden_403_page():
    return render_template("403.html")


@let_to(['normal'])
def user_home_page():
    return render_template("user_home.html")


@let_to(['normal'])
def user_history_page():
    patient = Human(tc=session['user_tc']).get_object()
    histories = History(patient=patient).get_objects()

    return render_template("user_history.html", histories=histories,
                           user_auth=session['user_auth'])  # user_auth: for navbar
