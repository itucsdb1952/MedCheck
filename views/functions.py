from flask import redirect, url_for, session, request
from flask import request

from werkzeug.utils import secure_filename

from views import helpers, views
from models import Place, Hospital, Human, Doctor

import psycopg2 as dbapi2
import sys, os
from settings import db_url
import csv

import functools

ALLOWED_EXTENSIONS = ['csv']
UPLOAD_FOLDER = 'static/uploads'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def get_hospitals_with_place(limit: int = 100, city: str = None, district: str = None) -> list:
    """

    :param limit:
    :param city:
    :param district:
    :return:
    """

    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                statement = "SELECT hospital.name, place.city, place.district, hospital.rate, hospital.handicapped, hospital.park " \
                            "FROM hospital, place "
                if city:
                    if district:  # city and district
                        statement += "WHERE hospital.address = place.id AND place.city = '{}' " \
                                     "AND place.district = '{}' ".format(city, district)
                    else:  # just city
                        statement += "WHERE hospital.address = place.id AND place.city = '{}' ".format(city)

                elif district:  # just district
                    statement += "WHERE hospital.address = place.id AND place.district = '{}' ".format(district)
                else:  # fetch all hospitals
                    statement += "WHERE hospital.address = place.id "

                statement += "ORDER BY name LIMIT {}".format(limit)

                cursor.execute(statement)
                record = cursor.fetchall()
                return record

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


def login():
    tc = request.form.get('tc')
    password = request.form.get('password')
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                query = "select tc, password, authorize from human where tc='{}' ".format(tc)
                cursor.execute(query)
                record = cursor.fetchone()
                if record:
                    tc_, password_, authorize_ = record
                    if password_ == password:
                        session['user_tc'] = tc_
                        session['user_auth'] = authorize_
                    return redirect('/')
    except (Exception, dbapi2.Error) as error:
        print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)


def add_place():
    city = request.form.get('add_city')
    district = request.form.get('add_district')
    places = Place(city, district).get_objects()
    if len(places) == 0:
        Place(city, district).save()
    return redirect(url_for(views.admin_places_page.__name__))


def del_place(place_id):
    Place(id=place_id).delete()
    return redirect(url_for(views.admin_places_page.__name__))


def update_place(place_id):
    city = request.form.get('modal_city')
    district = request.form.get('modal_district')

    Place(id=place_id).update(city, district)
    return redirect(url_for(views.admin_places_page.__name__))


def upload_place():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file = request.files['place_file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    pass
                    line_count += 1
                else:
                    city, district = row
                    Place(city, district).save()
                    line_count += 1
    return redirect(url_for(views.admin_places_page.__name__))


def add_hospital():
    hospital_name = request.form.get('hospital_name')
    city = request.form.get('city_select')
    district = request.form.get('district_select')
    park = helpers.checkbox_to_bool(request.form.get('park'))
    handicapped = helpers.checkbox_to_bool(request.form.get('handicapped'))

    p = Place(city, district).get_objects()[0]
    Hospital(hospital_name, p.id, park=park, handicapped=handicapped).save()
    return redirect(url_for(views.admin_hospitals_page.__name__))


def del_hospital(hospital_id):
    Hospital(id=hospital_id).delete()
    return redirect(url_for(views.admin_hospitals_page.__name__))


def update_hospital(hospital_id):
    hospital_name = request.form.get('modal_hospital_name')
    city = request.form.get('modal_city_select')
    district = request.form.get('modal_district_select')
    a = request.form.get('modal_park')
    park = helpers.checkbox_to_bool(request.form.get('modal_park'))
    handicapped = helpers.checkbox_to_bool(request.form.get('modal_handicapped'))

    if city and district:
        address = Place(city, district).get_objects()[0]
    else:
        address = None

    Hospital(id=hospital_id).update(hospital_name, address, handicapped=handicapped, park=park)
    return redirect(url_for(views.admin_hospitals_page.__name__))


def add_human():
    name = request.form.get("doctor_name")
    surname = request.form.get("doctor_surname")
    tc = request.form.get("doctor_tc")
    password = request.form.get("doctor_password")
    email = request.form.get("doctor_email")
    authorize = request.form.get("authorize_select")
    city = request.form.get("city_select_add")
    district = request.form.get("district_select_add")
    address = Place(city=city, district=district).get_objects()[0]

    human = Human(tc=tc).get_object()
    if human is None:
        human = Human(tc=tc, password=password, authorize=authorize, name=name, surname=surname, mail=email,
                      address=address)
        human.save()

    if authorize == 'doctor':
        workdays = str()
        day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(day_list):
            if request.form.get(day) == "on":
                workdays += str(i + 1)
        expertise = request.form.get("doctor_expertise")
        hospital_id = request.form.get("hospital_select_add")
        hospital = Hospital(id=hospital_id).get_object()

        doctor = Doctor(human=human).get_object()
        if doctor is None:
            doctor = Doctor(human=human, workdays=workdays, expertise=expertise, hospital=hospital)
            doctor.save()
        #  else doctor is already created

    return redirect(url_for(views.admin_humans_page.__name__))


def del_human(human_tc):
    Human(tc=human_tc).delete()
    return redirect(url_for(views.admin_humans_page.__name__))


def update_human(human_tc):
    name = request.form.get('modal_human_name')
    surname = request.form.get('modal_human_name')
    city = request.form.get('modal_city_select')
    district = request.form.get('modal_district_select')
    mail = request.form.get('modal_human_mail')
    authorize = request.form.get('modal_authorize_select')

    if city and district:
        address = Place(city, district).get_objects()[0]
    else:
        address = None

    Human(tc=human_tc).update(address=address, name=name, surname=surname, mail=mail, authorize=authorize)
    return redirect(url_for(views.admin_humans_page.__name__))


def delete_doctor():
    tc = request.form.get("doctor_tc")
    human_for_check = Human(tc=tc).get_object()
    if human_for_check is not None:
        Doctor(human=human_for_check).delete()
    return redirect(url_for('admin_humans_page'))


def add_person():
    name = request.form.get("name")
    surname = request.form.get("surname")
    tc = request.form.get("tc")
    email = request.form.get("email")
    address = request.form.get("address")
    password = request.form.get("password")
    authorization = request.form.get("authorization")
    human_for_check = Human(tc=tc).get_object()
    if human_for_check is None:
        human = Human(tc=tc, password=password, authorize=authorization, name=name, surname=surname, mail=email,
                      address=address)
        human.save()

    return redirect(url_for('login_page'))


def let_to(auths: list):
    def decorator_let_to(view_func):
        @functools.wraps(view_func)
        def wrapper_view_func(*args, **kwargs):
            # ------------------------------------------------------
            if 'user_auth' in session:
                user_auth = session['user_auth']
                if user_auth in auths:
                    returned_value = view_func(*args, **kwargs)
                else:
                    return redirect(url_for(views.forbidden_403_page.__name__))
            else:
                return redirect(url_for(views.login_page.__name__))
            # ------------------------------------------------------
            return returned_value

        return wrapper_view_func

    return decorator_let_to
