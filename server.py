from flask import Flask
from views import views, functions, ajax

app = Flask(__name__)
app.secret_key = b'\xe7x\xd2\xd3\x028\xb1\xf15\xb1?\xc1\x8d\xa9\xdaz'

# VIEWS
app.add_url_rule("/home", view_func=views.home_page)
app.add_url_rule("/places", view_func=views.admin_places_page)
app.add_url_rule("/hospitals", view_func=views.admin_hospitals_page)
app.add_url_rule("/hospital_patient", view_func=views.hospital_patient_page)
app.add_url_rule("/", view_func=views.login_page)
app.add_url_rule("/register", view_func=views.register_page)
app.add_url_rule("/humans", view_func=views.admin_humans_page)
app.add_url_rule("/how_to_use", view_func=views.how_to_use_page)
app.add_url_rule("/403", view_func=views.forbidden_403_page)

app.add_url_rule("/my_history", view_func=views.user_history_page)

# FUNCTIONS
app.add_url_rule("/add_place", view_func=functions.add_place, methods=['POST'])
app.add_url_rule("/del_place/<int:place_id>", view_func=functions.del_place, methods=['GET'])
app.add_url_rule("/update_place/<int:place_id>", view_func=functions.update_place, methods=['POST'])
app.add_url_rule("/upload_place", view_func=functions.upload_place, methods=['POST'])

app.add_url_rule("/add_hospital", view_func=functions.add_hospital, methods=['POST'])
app.add_url_rule("/del_hospital/<int:hospital_id>", view_func=functions.del_hospital, methods=['GET'])
app.add_url_rule("/update_hospital/<int:hospital_id>", view_func=functions.update_hospital, methods=['POST'])

app.add_url_rule("/add_human", view_func=functions.add_human, methods=['POST'])
app.add_url_rule("/del_human/<string:human_tc>", view_func=functions.del_human, methods=['GET'])
app.add_url_rule("/update_human/<string:human_tc>", view_func=functions.update_human, methods=['POST'])

app.add_url_rule("/add_history", view_func=functions.add_history, methods=['POST'])

app.add_url_rule("/delete_doctor", view_func=functions.delete_doctor, methods=['POST'])
app.add_url_rule("/add_person", view_func=functions.add_person, methods=['POST'])
app.add_url_rule("/login", view_func=functions.login, methods=['POST'])
app.add_url_rule("/logout", view_func=functions.logout, methods=['GET'])

# AJAX
app.add_url_rule("/get_districts", view_func=ajax.get_districts_ajax, methods=['POST'])
app.add_url_rule("/get_hospitals", view_func=ajax.get_hospitals_ajax, methods=['POST'])
app.add_url_rule("/get_doctors", view_func=ajax.get_doctors_ajax, methods=['POST'])
app.add_url_rule("/get_doctor_info", view_func=ajax.get_doctor_info_ajax, methods=['POST'])
app.add_url_rule("/filter_place", view_func=ajax.filter_place_ajax, methods=['POST'])
app.add_url_rule("/filter_hospital", view_func=ajax.filter_hospital_ajax, methods=['POST'])
app.add_url_rule("/filter_human", view_func=ajax.filter_human_ajax, methods=['POST'])

if __name__ == "__main__":
    app.debug = True
    app.run()
