from flask import Flask, render_template, redirect
from flask import request
import sys
from views import views, helpers
from models import Place, Hospital

app = Flask(__name__)


# app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'

@app.route("/")
def admin_page():
    try:
        hospitals = views.get_hospitals()
        print("Rendering...", file=sys.stderr)
    except Exception as e:
        return e
    else:
        return render_template('admin.html', hospitals=hospitals)


@app.route("/hospitals")
def hospitals_page():
    places = Place().get_objects(distinct_city=True)
    cities = [place.city for place in places]

    return render_template('admin_hospitals.html', cities=cities)


@app.route("/add_hospital", methods=['POST'])
def add_hospital_page():
    hospital_name = request.form.get('hospital_name')
    city = request.form.get('city_select')
    district = request.form.get('district_select')
    park = helpers.checkbox_to_bool(request.form.get('park'))
    handicapped = helpers.checkbox_to_bool(request.form.get('handicapped'))

    response = views.add_hospital(hospital_name, city, district, park, handicapped)

    return redirect('/')


@app.route("/del_hospital", methods=['POST'])
def del_hospital():
    hospital_id = request.form.get('hospital_select_del')
    Hospital(id=hospital_id).delete()
    return redirect('/')


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
    doctor_workdays = ""  # sonradan degistirelecek
    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i, day in enumerate(day_list):
        if request.form.get(day) == "on":
            doctor_workdays += str(i + 1)
    print("workdays:", doctor_workdays)
    doctor_expertise = request.form.get("doctor_expertise")
    doctor_hospital = request.form.get("doctor_hospital")
    doctor_authorize = 2
    print("doctor page info", doctor_name, doctor_surname, doctor_tc)
    response_for_human = views.add_human(doctor_tc, doctor_password, doctor_authorize, doctor_name, doctor_surname,
                                         doctor_email, doctor_address)
    response_for_doctor = views.add_doctor(doctor_tc, doctor_workdays, doctor_expertise, doctor_hospital)
    return response_for_human, response_for_doctor


@app.route("/delete_doctor", methods=['POST'])
def delete_doctor_page():
    doctor_tc = request.form.get("doctor_tc")
    response_for_doctor = views.delete_doctor(doctor_tc)
    return response_for_doctor


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
    places = Place(request.form.get('city_name')).get_objects()
    response = " ".join(['<option value="{}">{}</option>'.format(place.district, place.district) for place in places])
    return response


@app.route("/get_hospitals", methods=['POST', 'GET'])
def get_hospitals_ajax_page():
    place = Place(request.form.get('city_name'), request.form.get('district_name'), ).get_objects()[0]
    hospitals = Hospital(address=place).get_objects()
    response = " ".join(
        ['<option value="{}">{}</option>'.format(hospital.id, hospital.name) for hospital in hospitals])
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()
