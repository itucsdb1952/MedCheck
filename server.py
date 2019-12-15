from flask import Flask
from views import views, functions, ajax


def create_app():
    app = Flask(__name__)
    app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'

    # VIEWS
    app.add_url_rule("/", view_func=views.admin_page)
    app.add_url_rule("/hospitals", view_func=views.hospitals_page)
    app.add_url_rule("/hospital_patient", view_func=views.hospital_patient_page)
    app.add_url_rule("/login_page", view_func=views.login_page)
    app.add_url_rule("/register", view_func=views.register_page)
    app.add_url_rule("/doctors", view_func=views.doctors_page)
    app.add_url_rule("/how_to_use", view_func=views.how_to_use_page)

    # FUNCTIONS
    app.add_url_rule("/add_hospital", view_func=functions.add_hospital, methods=['POST'])
    app.add_url_rule("/del_hospital", view_func=functions.del_hospital, methods=['POST'])
    app.add_url_rule("/add_doctor", view_func=functions.add_doctor, methods=['POST'])
    app.add_url_rule("/delete_doctor", view_func=functions.delete_doctor, methods=['POST'])
    app.add_url_rule("/add_person", view_func=functions.add_person, methods=['POST'])
    app.add_url_rule("/login", view_func=functions.login, methods=['POST'])

    # AJAX
    app.add_url_rule("/get_districts", view_func=ajax.get_districts_ajax, methods=['POST'])
    app.add_url_rule("/get_hospitals", view_func=ajax.get_hospitals_ajax, methods=['POST'])

    return app


if __name__ == "__main__":
    app = create_app()
    app.debug = True
    app.run()
