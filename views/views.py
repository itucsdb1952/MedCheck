from flask import render_template, session, redirect, url_for

from models import Place, Human
from views import functions
from views.functions import let_to


@let_to(['admin'])
def admin_page():
    try:
        hospitals = functions.get_hospitals_with_place()

    except Exception as e:
        return e
    else:
        return render_template('admin.html', hospitals=hospitals)


@let_to(['admin'])
def admin_hospitals_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]

    return render_template('admin_hospitals.html', cities=cities)


@let_to(['admin'])
def admin_humans_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]

    return render_template('admin_humans.html', cities=cities)


def hospital_patient_page():
    return render_template('hospital_patient.html')


def login_page():
    print(session)
    if 'user_tc' and 'user_auth' in session:
        user_tc = session['user_tc']
        user_auth = session['user_auth']
        if user_auth == 'normal':
            return user_tc + " " + user_auth
        elif user_auth == 'doctor':
            return user_tc + " " + user_auth
        elif user_auth == 'admin':
            return redirect(url_for(admin_page.__name__))

    print("no user tc or auth")
    return render_template("login.html")


def register_page():
    return render_template("Register.html")


def how_to_use_page():
    return render_template("How to Use.html")


def forbidden_403_page():
    return render_template("403.html")
