from flask import Flask, render_template
from flask import request

from views import *

app = Flask(__name__)


# app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'

@app.route("/")
def admin_page():
    try:
        hospitals = get_hospitals()
        print("Rendering...", file=sys.stderr)
    except Exception as e:
        return e
    else:
        return render_template('admin.html', hospitals=hospitals)


@app.route("/hospitals")
def hospitals_page():
    cities = get_cities()
    cities = [city[0] for city in cities]

    districts = get_districts()
    districts = [district[0] for district in districts]
    return render_template('admin_hospitals.html', cities=cities, districts=districts)


@app.route("/add_hospital", methods=['POST'])
def add_hospital_page():
    hospital_name = request.form.get('hospital_name')
    city = request.form.get('city_select')
    district = request.form.get('district_select')
    park = request.form.get('park')
    if park == 'on':
        park = True
    else:
        park = False
    handicapped = request.form.get('handicapped')
    if handicapped == 'on':
        handicapped = True
    else:
        handicapped = False
    response = add_hospital(hospital_name, city, district, park, handicapped)

    return response


@app.route("/doctors")
def doctors_page():
    return render_template('admin_doctors.html')


@app.route("/add_doctor", methods=['POST'])
def add_doctor_page():
    print("belki buraya gelmistir")
    doctor_name = request.form.get("doctor_name")
    doctor_surname = request.form.get("doctor_surname")
    doctor_tc = request.form.get("doctor_tc")
    doctor_password = request.form.get("doctor_password")
    doctor_email = request.form.get("doctor_email")
    doctor_address = request.form.get("doctor_address")
    doctor_workdays = request.form.get("doctor_workdays")
    doctor_expertise = request.form.get("doctor_expertise")
    doctor_hospital = request.form.get("doctor_hospital")
    doctor_authorize = 2
    response = add_human(doctor_tc, doctor_password, doctor_authorize, doctor_name, doctor_surname, doctor_email, doctor_address)
    return response

@app.route("/log_in")
def log_in_page():
    return render_template("Log_in.html")


@app.route("/register")
def register_page():
    return render_template("Register.html")


@app.route("/how_to_use")
def how_to_use_page():
    return render_template("How to Use.html")


@app.route("/get_districts", methods=['POST', 'GET'])
def get_districts_ajax_page():
    districts = get_districts_ajax(request.form['city_name'])
    districts = [district[0] for district in districts]
    response = " ".join(['<option value="{}">{}</option>'.format(district, district) for district in districts])
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()
