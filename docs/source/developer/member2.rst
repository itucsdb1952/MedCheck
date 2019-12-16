Parts Implemented by Emre Faruk Kolac
=====================================


.. code-block:: python
	:linenos:

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

Since doctors are first needed to be created as human class, first add_human function called in order to create a human.

.. code-block:: python
	:linenos:

	def add_doctor(human_id, workdays, expertise, hospital_id):
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                print("yeni doktordayız")
                statement = "insert into doctor(human, workdays, expertise, hospital)"\
                "values('{}','{}','{}','{}');".format(human_id, workdays, expertise, hospital_id)
                cursor.execute(statement)
                return "successful"

    finally:
        if connection:
            cursor.close()
            connection.close()
			
Then add_doctor function is called from the information obtained from add_human function. 