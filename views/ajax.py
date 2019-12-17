from flask import request, render_template
from models import Place, Hospital, Human, Doctor
from views import helpers


def get_districts_ajax():
    places = Place(request.form.get('city_name')).get_objects()
    response = " ".join(['<option value="{}">{}</option>'.format(place.district, place.district) for place in places])
    return response


def get_hospitals_ajax():
    place = Place(request.form.get('city_name'), request.form.get('district_name')).get_objects()[0]
    hospitals = Hospital(address=place).get_objects()
    response = " ".join(
        ['<option value="{}">{}</option>'.format(hospital.id, hospital.name) for hospital in hospitals])
    return response


def get_doctors_ajax():
    hospital = Hospital(id=request.form.get('hospital_id')).get_object()
    doctors = Doctor(hospital=hospital).get_objects()
    response = " ".join(
        ['<option value="{}">{}</option>'.format(doctor.human.tc, doctor.human.name) for doctor in doctors])
    return response


def get_doctor_info_ajax():
    human = Human(tc=request.form.get('doctor_tc')).get_object()
    doctor = Doctor(human=human).get_object()
    day_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    workdays_ = doctor.workdays
    workdays = list()
    for i, workday_ in enumerate(workdays_):
        if int(workday_) == i + 1:
            workdays.append(day_list[i + 1])
    return render_template('sub_templates/doctor_info.html', doctor=doctor, workdays=workdays)


def filter_place_ajax():
    city = request.form.get('city')
    district = request.form.get('district')
    if city == '':
        city = None
    if district == '':
        district = None

    places = Place(city, district).get_objects()

    return render_template('sub_templates/filtered_place_table.html', places=places)


def filter_hospital_ajax():
    city = request.form.get('city')
    district = request.form.get('district')
    name = request.form.get('name')
    if name == '':
        name = None
    capacity = request.form.get('capacity')
    rate = request.form.get('rate')
    park = helpers.checkbox_to_bool(request.form.get('park'))
    handicapped = helpers.checkbox_to_bool(request.form.get('handicapped'))
    if city and district:
        address = Place(city, district).get_objects()[0]
    else:
        address = None

    hospitals = Hospital(address=address, name=name, capacity=capacity, rate=rate, park=park,
                         handicapped=handicapped).get_objects()

    return render_template('sub_templates/filtered_hospital_table.html', hospitals=hospitals)


def filter_human_ajax():
    city = request.form.get('city')
    district = request.form.get('district')
    authorize = request.form.get('authorize')
    name = request.form.get('name')
    surname = request.form.get('surname')
    mail = request.form.get('mail')
    if name == '':
        name = None
    if surname == '':
        surname = None
    if authorize == '':
        authorize = None
    if city and district:
        address = Place(city, district).get_objects()[0]
    else:
        address = None

    humans = Human(name=name, surname=surname, mail=mail, authorize=authorize, address=address).get_objects()

    return render_template('sub_templates/filtered_human_table.html', humans=humans)
