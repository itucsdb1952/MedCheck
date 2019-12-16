from flask import request
from models import Place, Hospital


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
