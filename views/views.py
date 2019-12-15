from flask import render_template

from models import Place
from views import functions


def admin_page():
    try:
        hospitals = functions.get_hospitals_with_place()

    except Exception as e:
        return e
    else:
        return render_template('admin.html', hospitals=hospitals)


def hospitals_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]

    return render_template('admin_hospitals.html', cities=cities)


def doctors_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]

    return render_template('admin_doctors.html', cities=cities)


def hospital_patient_page():
    return render_template('hospital_patient.html')


def login_page():
    return render_template("login.html")


def register_page():
    return render_template("Register.html")


def how_to_use_page():
    return render_template("How to Use.html")