Parts Implemented by Emre Faruk Kolac
=====================================


.. code-block:: python
	{% extends 'base.html' %}

	{% block title %}DOCTORS{% endblock %}

	{% block body %}

		<div class="container">
			<br>
			<div class="row">
				<div class="col">
					<h4 class="text-center">ADD HUMAN</h4>
					<hr>
					<form method="POST" action="{{ url_for('add_human') }}">
						<div class="form-group row">
							<label for="doctor_name" class="col-sm-2 col-form-label">Name:</label>
							<div class="col-sm-10">
								<input type="text" name="doctor_name" class="form-control" id="doctor_name" placeholder="Canan">
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_surname" class="col-sm-2 col-form-label">Surname: </label>
							<div class="col-sm-10">
								<input type="text" name="doctor_surname" class="form-control" id="doctor_surname" placeholder="Karatay">
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_tc" class="col-sm-2 col-form-label">TC: </label>
							<div class="col-sm-10">
								<input type="text" name="doctor_tc" class="form-control" id="doctor_tc" placeholder="Must be legit TC no">
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_password" class="col-sm-2 col-form-label">Password: </label>
							<div class="col-sm-10">
								<input type="text" name="doctor_password" class="form-control" id="doctor_password" placeholder="Password assigned to the doctor">
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_email" class="col-sm-2 col-form-label">E-mail: </label>
							<div class="col-sm-10">
								<input type="email" name="doctor_email" class="form-control" id="doctor_email" placeholder="Will be used to contact">
							</div>
						</div>
						<div class="form-group row">
							<label for="authorize_select" class="col-sm-2 col-form-label">Authorize: </label>
							<div class="col-sm-10">
								<select class="form-control" name="authorize_select" id="authorize_select">
									<option value="admin">Admin</option>
									<option value="doctor" selected>Doctor</option>
									<option value="normal">Normal</option>
								</select>
							</div>
						</div>
						<div class="form-group row">
							<label for="city_select_add" class="col-sm-2 col-form-label">City: </label>
							<div class="col-sm-4">
								<select class="form-control" name="city_select_add" id="city_select_add">
									{% for city in cities %}
										 <option value="{{ city }}">{{ city }}</option>
									{% endfor %}

							</select>
							</div>

							<label for="district_select_add" class="col-sm-2 col-form-label">District: </label>
							<div class="col-sm-4">
								<select class="form-control" name="district_select_add" id="district_select_add">
									 <option value="">Choose a City</option>
								</select>
							</div>
						</div>
						<div class="form-group row doctor_div">
							<label for="hospital_select_add" class="col-sm-2 col-form-label">Hospital: </label>
							<div class="col-sm-10">
								<select class="form-control" name="hospital_select_add" id="hospital_select_add">
									 <option value="">Choose a Hospital</option>
								</select>
							</div>
						</div>
						<div class="form-group row doctor_div">
							<div class="col-sm-2">Workdays: </div>
							<div class="col-sm-4">
								<div class="form-check">
									<input class="form-check-input" name="Monday" type="checkbox" id="gridCheck1">
									<label class="form-check-label" for="gridCheck1">
										Monday
									</label>
									<div></div>
									<input class="form-check-input" name="Tuesday" type="checkbox" id="gridCheck1">
									<label class="form-check-label" for="gridCheck1">
										Tuesday
									</label>
									<div></div>
									<input class="form-check-input" name="Wednesday" type="checkbox" id="gridCheck1">
									<label class="form-check-label" for="gridCheck1">
										Wednesday
									</label>
									<div></div>
									<input class="form-check-input" name="Thursday" type="checkbox" id="gridCheck1">
									<label class="form-check-label" for="gridCheck1">
										Thursday
									</label>
									<div></div>
									<input class="form-check-input" name="Friday" type="checkbox" id="gridCheck1">
									<label class="form-check-label" for="gridCheck1">
										Friday
									</label>
									<div></div>
									<input class="form-check-input" name="Saturday" type="checkbox" id="gridCheck1">
									<label class="form-check-label" for="gridCheck1">
										Saturday
									</label>
									<div></div>
									<input class="form-check-input" name="Sunday" type="checkbox" id="gridCheck1">
									<label class="form-check-label" for="gridCheck1">
										Sunday
									</label>
								</div>
							</div>
						</div>

						<div class="form-group row">
							<div class="col-sm-10">
								<button type="submit" id="hebe" class="btn btn-primary">Add Doctor</button>
							</div>
						</div>
					</form>
				</div>
				<div class="col">

					<h4 class="text-center">FILTER HUMAN</h4>
					<hr>

						<form method="POST" id="filter_human_form" action_url="{{url_for('filter_human_ajax')}}">
						<div class="form-group row">
							<label for="city_select_filter" class="col-sm-2 col-form-label">City: </label>
							<div class="col-sm-4">
								<select class="form-control" name="city_select_filter" id="city_select_filter">
									{% for city in cities %}
										 <option value="{{ city }}">{{ city }}</option>
									{% endfor %}

							</select>
							</div>

							<label for="district_select_filter" class="col-sm-2 col-form-label">District: </label>
							<div class="col-sm-4">
								<select class="form-control" name="district_select_filter" id="district_select_filter">
									 <option value="">Choose a District</option>
								</select>
							</div>
						</div>



						<div class="form-group row">
							<label for="human_name_filter" class="col-sm-2 col-form-label">Name:</label>
							<div class="col-sm-4">
								<input type="text" name="human_name_filter" class="form-control" id="human_name_filter" placeholder="Canan">
							</div>
							<label for="human_surname_filter" class="col-sm-2 col-form-label">Surname:</label>
							<div class="col-sm-4">
								<input type="text" name="human_surname_filter" class="form-control" id="human_surname_filter" placeholder="Karatay">
							</div>
						</div>

						<div class="form-group row">
							<label for="human_mail_filter" class="col-sm-2 col-form-label">Email:</label>
							<div class="col-sm-4">
								<input type="email" name="human_mail_filter" class="form-control" id="human_mail_filter">
							</div>
							<label for="authorize_select_filter" class="col-sm-2 col-form-label">Authorize: </label>
							<div class="col-sm-4">
								<select class="form-control" name="authorize_select_filter" id="authorize_select_filter">
									<option value="admin">Admin</option>
									<option value="doctor" selected>Doctor</option>
									<option value="normal">Normal</option>
								</select>
							</div>
						</div>
							<div class="col-sm-10">
								<button type="button" id="filter_human_button" onclick="filter_humans();" class="btn btn-danger">Get humans</button>
							</div>

					</form>
				</div>

			</div>

					<div class="modal fade" id="update_modal" data-backdrop="static" tabindex="-1" role="dialog" aria-labelledby="update_modal_label" aria-hidden="true">
			  <div class="modal-dialog" role="document">
			  <form method="POST" id="modal_update_form" action="{{ url_for('update_human', human_tc=0) }}">
				<div class="modal-content">
				  <div class="modal-header">
					<h5 class="modal-title" id="update_modal_label">UPDATE HUMAN</h5>
					<button type="button" class="close" data-dismiss="modal" aria-label="Close">
					  <span aria-hidden="true">&times;</span>
					</button>
				  </div>
				  <div class="modal-body">
						<div class="form-group row">
							<label for="modal_human_name" class="col-sm-2 col-form-label">Name:</label>
							<div class="col-sm-4">
								<input type="text" name="modal_human_name" class="form-control" id="modal_human_name">
							</div>
							<label for="modal_human_surname" class="col-sm-2 col-form-label">Surname:</label>
							<div class="col-sm-4">
								<input type="text" name="modal_human_surname" class="form-control" id="modal_human_surname">
							</div>
						</div>
						<div class="form-group row">
							<label for="modal_city_select" class="col-sm-2 col-form-label">City: </label>
							<div class="col-sm-4">
								<select class="form-control" name="modal_city_select" id="modal_city_select">
									{% for city in cities %}
										 <option value="{{ city }}">{{ city }}</option>
									{% endfor %}

							</select>
							</div>

							<label for="modal_district_select" class="col-sm-2 col-form-label">District: </label>
							<div class="col-sm-4">
								<select class="form-control" name="modal_district_select" id="modal_district_select">
									 <option value="">Choose a City</option>
								</select>
							</div>
						</div>
						<div class="form-group row">
							<label for="modal_human_mail" class="col-sm-2 col-form-label">Email:</label>
							<div class="col-sm-4">
								<input type="email" name="modal_human_mail" class="form-control" id="modal_human_mail">
							</div>

							<label for="modal_authorize_select" class="col-sm-2 col-form-label">Authorize: </label>
							<div class="col-sm-4">
								<select class="form-control" name="modal_authorize_select" id="modal_authorize_select">
									<option value="admin">Admin</option>
									<option value="doctor" selected>Doctor</option>
									<option value="normal">Normal</option>
								</select>
							</div>
						</div>

				  </div>
				  <div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
					<button type="submit" class="btn btn-primary">Update</button>
				  </div>
				</div>
			  </form>
			  </div>
			</div>


			<div id="human-table"></div>
		</div>


	{% endblock %}

	{% block JS %}
	<script>

admin_humans page like any other admin pages, have the authority to add new members and filter humans.
admin_places.html and admin_hospitals.html work with the same logic. They all extend from base.html

.. code-block:: python
	<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>403 FORBIDDEN</title>
	</head>
	<body>
	<h1>You don't have permission to access!</h1>
	</body>
	</html>

403.html file is shown to user whenever they tried to access to page that they are not authorized. This works even user tries access the specific address using via internet address.
 .. code-block:: python
	{% extends 'base.html' %}

	{% block title %}How to Use{% endblock %}

	{% block body %}


		<div class="container">
			<br>

			<h4 class="text-center">Instructions</h4>
			<img src="{{ url_for('static', filename = 'howto.png') }}" width="985" height="902" class="d-inline-block align-top" alt="How to instructions">


		</div>
	{% endblock %}

This page shows users how to use the application. howto.png file guides through the process of registering to the system, signing in and taking an appointment.

.. code-block:: python
	{% extends 'base.html' %}

	{% block title %}Log In{% endblock %}

	{% block body %}
	<link rel="stylesheet" href="../static/css/login_page.css">

		<div class="container h-100">
			<div class="d-flex justify-content-center h-100">
				<div class="user_card">
					<div class="d-flex justify-content-center">
						<div class="brand_logo_container">
							<img src="../static/medchecklogo.png" class="brand_logo" alt="Logo">
						</div>
					</div>
					<div class="d-flex justify-content-center form_container">
						<form method="POST" action="{{ url_for('login')}}">
							<div class="input-group mb-3">
								<div class="input-group-append">
									<span class="input-group-text"><i class="fas fa-user"></i></span>
								</div>
								<input type="text" name="tc" class="form-control input_user" value="" placeholder="Social Security Number" required>
							</div>
							<div class="input-group mb-2">
								<div class="input-group-append">
									<span class="input-group-text"><i class="fas fa-key"></i></span>
								</div>
								<input type="password" name="password" class="form-control input_pass" value="" placeholder="password" required>
							</div>
							<div class="form-group">
								<div class="custom-control custom-checkbox">
									<input type="checkbox" class="custom-control-input" id="customControlInline">
									<label class="custom-control-label" for="customControlInline">Remember me</label>
								</div>
							</div>
								<div class="d-flex justify-content-center mt-3 login_container">
						<button type="submit" name="button" class="btn login_btn">Login</button>
					   </div>
						</form>
					</div>

					<div class="mt-4">
						<div class="d-flex justify-content-center links">
							Don't have an account? <a href="{{ url_for('register_page') }}" class="ml-2">Sign Up</a>
						</div>
					</div>
				</div>
			</div>
		</div>

	{% endblock %}

Log in page welcomes user if he is not recognized. Has a link to register page in case user is not registered to the system.

.. code-block:: python
	{% extends 'base.html' %}

	{% block title %}Register{% endblock %}

	{% block body %}


		<div class="container">
			<br>
			<h4 class="text-center">Welcome</h4>
					<form method="POST" action="/add_person">
						<div class="form-group row">
							<label for="doctor_name" class="col-sm-2 col-form-label">Name:</label>
							<div class="col-sm-10">
								<input type="text" name="name" class="form-control" id="doctor_name" placeholder="Mehmet">
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_select" class="col-sm-2 col-form-label">Surname: </label>
							<div class="col-sm-10">
								<input type="text" name="surname" class="form-control" id="doctor_name" placeholder="Yıldız">
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_select" class="col-sm-2 col-form-label">TC: </label>
							<div class="col-sm-10">
								<input type="text" name="tc" class="form-control" id="doctor_name" placeholder="Must be legit TC no">
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_select" class="col-sm-2 col-form-label">E-mail: </label>
							<div class="col-sm-10">
								<input type="text" name="email" class="form-control" id="doctor_name" placeholder="Will be used to contact">
							</div>
						</div>
						<div class="form-group row">
							<label for="city_select" class="col-sm-2 col-form-label">City: </label>
							<div class="col-sm-4">
								<select class="form-control" name="city_select" id="city_select">
									{% for city in cities %}
										 <option value="{{ city }}">{{ city }}</option>
									{% endfor %}

							</select>
							</div>

							<label for="district_select" class="col-sm-2 col-form-label">District: </label>
							<div class="col-sm-4">
								<select class="form-control" name="district_select" id="district_select">
									 <option value="">Choose a District</option>
								</select>
							</div>
						</div>
						<div class="form-group row">
							<label for="doctor_select" class="col-sm-2 col-form-label">Password: </label>
							<div class="col-sm-10">
								<input type="text" name="password" class="form-control" id="doctor_name" placeholder="Declare a password">
							</div>
						</div>
						<div class="form-group row">
							<div class="col-sm-10">
								<button type="submit" id="hebe" class="btn btn-primary">Register</button>
							</div>
						</div>
					</form>
				</div>


	{% endblock %}

	{% block JS %}
	<script>

	$(document).ready(function() {


		$('#city_select').change(function () {

			var url = "/get_districts";
			var city_name = $(this).val();
			$.ajax({
				type: 'POST',
				url: url,
				data: {
					'city_name': city_name
				},
				success: function (data) {
					$('#district_select').html(data);
				}
			});
		});
	});

	</script>
	{% endblock %}

Register page allows new users to register to system. Ajax is used to extract district information from selected city.