from flask import Flask, render_template, jsonify
from flask import request

from views import *

app = Flask(__name__)


# app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'


# @app.route("/")
# def home_page():
#     return "Welcome to MedCheck Project!"


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


@app.route("/add_hospital",methods=['POST'])
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


@app.route("/get_districts", methods=['POST', 'GET'])
def get_districts_ajax_page(city_name):
    print("GET DISTRICT AJAX")
    districts = get_districts_ajax(city_name)
    districts = [district[0] for district in districts]
    result = jsonify(districts)
    print(result)
    return result


@app.route("/get_hebe", methods=['POST', 'GET'])
def hebe_ajax(city_name):
    return jsonify({'data': 'Loooooo'})


if __name__ == "__main__":
    app.debug = True
    app.run()
