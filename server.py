from flask import Flask, render_template, redirect, url_for
from flask import request

from views import views, helpers
from models import Place, Hospital, Human, Doctor

app = Flask(__name__)


# app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'

@app.route("/")
def admin_page():
    try:
        hospitals = views.get_hospitals_with_place()

    except Exception as e:
        return e
    else:
        url = url_for('admin_page')

        return render_template('admin.html', hospitals=hospitals, url=url)


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

    p = Place(city, district).get_objects()[0]
    Hospital(hospital_name, p.id, park=park, handicapped=handicapped).save()

    return redirect('/')


@app.route("/del_hospital", methods=['POST'])
def del_hospital():
    hospital_id = request.form.get('hospital_select_del')
    Hospital(id=hospital_id).delete()
    return redirect('/')


@app.route("/doctors")
def doctors_page():
    return render_template('admin_doctors.html')


@app.route("/hospital_patient")
def hospital_patient_page():
    return render_template('hospital_patient.html')


@app.route("/add_doctor", methods=['POST'])
def add_doctor_page():
    print("belki buraya gelmistir")
    name = request.form.get("doctor_name")
    surname = request.form.get("doctor_surname")
    tc = request.form.get("doctor_tc")
    password = request.form.get("doctor_password")
    email = request.form.get("doctor_email")
    address = request.form.get("doctor_address")
    workdays = str()
    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i, day in enumerate(day_list):
        if request.form.get(day) == "on":
            workdays += str(i + 1)
    print("workdays:", workdays)
    expertise = request.form.get("doctor_expertise")
    hospital_name = request.form.get("doctor_hospital")
    print("doctor page info", name, surname, tc)

    human_for_check = Human(tc=tc).get_object()
    if human_for_check is None:
        human = Human(tc=tc, password=password, authorize='doctor', name=name, surname=surname, mail=email,
                      address=address)
        human.save()
        doctor = Doctor(human=human, workdays=workdays, expertise=expertise, hospital=hospital_name)
        doctor.save()

    return redirect(url_for('doctors_page'))


@app.route("/delete_doctor", methods=['POST'])
def delete_doctor_page():
    tc = request.form.get("doctor_tc")
    human_for_check = Human(tc=tc).get_object()
    if human_for_check is not None:
        Doctor(human=human_for_check).delete()
    return redirect(url_for('doctors_page'))


@app.route("/log_in")
def log_in_page():
    return render_template("Log_in.html")


@app.route("/log_in_check", methods=['POST'])
def log_in_check():
    tc = request.form.get("tc")
    password = request.form.get("password")
    response_for_log_in = views.log_in(tc, password)
    return response_for_log_in


@app.route("/register")
def register_page():
    return render_template("Register.html")


@app.route("/add_person", methods=['POST'])
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

    return redirect(url_for('log_in_page'))


@app.route("/how_to_use")
def how_to_use_page():
    return render_template("How to Use.html")


@app.route("/get_districts", methods=['POST'])
def get_districts_ajax():
    places = Place(request.form.get('city_name')).get_objects()
    response = " ".join(['<option value="{}">{}</option>'.format(place.district, place.district) for place in places])
    return response


@app.route("/get_hospitals", methods=['POST'])
def get_hospitals_ajax():
    place = Place(request.form.get('city_name'), request.form.get('district_name'), ).get_objects()[0]
    hospitals = Hospital(address=place.id).get_objects()
    response = " ".join(
        ['<option value="{}">{}</option>'.format(hospital.id, hospital.name) for hospital in hospitals])
    return response


if __name__ == "__main__":
    app.debug = True
    app.run()
