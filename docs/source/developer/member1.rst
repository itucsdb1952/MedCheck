Parts Implemented by Furkan Guvenc
==================================


.. code-block:: python

    import os
    import sys

    import psycopg2 as dbapi2
    from settings import db_url, SQL_DIR


    def read_sql_from_file(filename: str) -> list:
        filepath = os.path.join(SQL_DIR, filename)
        with open(filepath, 'r', encoding='windows-1254') as f:
            content = f.read()
            content = content.split(';')
            content = [row + ";" for row in content]
            return content


    def initialize(url: str) -> None:
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    print("Connected...", file=sys.stderr)

                    drop_statements = read_sql_from_file('drop_tables.sql')
                    for statement in drop_statements:
                        if len(statement) > 5:
                            cursor.execute(statement)
                    print("Drop tables...", file=sys.stderr)

                    create_statements = read_sql_from_file('create_tables.sql')
                    for statement in create_statements:
                        if len(statement) > 5:
                            cursor.execute(statement)
                    print("Create tables...", file=sys.stderr)

                    add_place_statements = read_sql_from_file('places.sql')
                    for statement in add_place_statements:
                        if len(statement) > 5:
                            cursor.execute(statement)
                    print("Places...", file=sys.stderr)

                    add_hospital_statements = read_sql_from_file('hospitals.sql')
                    for statement in add_hospital_statements:
                        if len(statement) > 5:
                            cursor.execute(statement)
                    print("Hospitals...", file=sys.stderr)

                    add_human_statements = read_sql_from_file('humans.sql')
                    for statement in add_human_statements:
                        if len(statement) > 5:
                            cursor.execute(statement)
                    print("Humans...", file=sys.stderr)

                    add_doctor_statements = read_sql_from_file('doctors.sql')
                    for statement in add_doctor_statements:
                        if len(statement) > 5:
                            cursor.execute(statement)
                    print("Doctors...", file=sys.stderr)
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

        finally:
            # closing database connection.
            if connection:
                cursor.close()
                connection.close()


    if __name__ == "__main__":
        print("Initializing...", file=sys.stderr)
        initialize(db_url)


Python file for initializing database.

.. code-block:: python

    import os.path
    import sys

    DSN_efk = {'user': "postgres",  # DSN for Emre Faruk Kolaç
               'password': "",
               'host': "127.0.0.1",
               'port': "5432",
               'database': "hebe2"
               }

    DSN_fg = {'user': "postgres",  # DSN for Furkan Güvenç
              'password': "1234",
              'host': "127.0.0.1",
              'port': "5432",
              'database': "hebe2"
              }

    fg_connection_url = "dbname={} user={} password={} host={} port={}".format(DSN_fg['database'], DSN_fg['user'],
                                                                               DSN_fg['password'], DSN_fg['host'],
                                                                               DSN_fg['port'])

    efk_connection_url = "dbname={} user={} password={} host={} port={}".format(DSN_efk['database'], DSN_efk['user'],
                                                                                DSN_efk['password'], DSN_efk['host'],
                                                                                DSN_efk['port'])
    HOME_PATH = os.path.expanduser("~").lower()  # home url of pc
    db_url = str()

    try:
        if 'furkan' in HOME_PATH:  # Pc of Furkan Güvenç
            db_url = fg_connection_url
        elif 'faruk' in HOME_PATH:  # Pc of Emre Faruk Kolaç
            db_url = efk_connection_url
        elif 'app' in HOME_PATH:  # Heroku
            db_url = os.getenv("DATABASE_URL")

    except Exception as e:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)

    #  postgres//user:pw@host:port/database
    SQL_DIR = "sqls"


/settings.py file makes required connections to database and runs "sqls" file which creates the database tables.

.. code-block:: python

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

Details will be given by furkan

.. code-block:: python
    import psycopg2 as dbapi2
    import sys
    from settings import db_url
    from views import helpers



    class Place:
        def __init__(self, *args, **kwargs):
            self.city = None
            self.district = None
            self.id = None

            if len(args) >= 2:
                self.city, self.district = args[:2]

            elif len(args) == 1:
                self.city = args[0]

            if 'city' in kwargs.keys():
                self.city = kwargs['city']
            if 'district' in kwargs.keys():
                self.district = kwargs['district']
            if 'id' in kwargs.keys():
                self.id = kwargs['id']

        def get_objects(self, distinct_city: bool = False) -> list:
            """
            READ
            It returns objects according to city and district
            :param:  distinct_city: cities are distinct?
            :return: list of objects
            """
            try:
                with dbapi2.connect(db_url) as connection:
                    with connection.cursor() as cursor:
                        if distinct_city:
                            query = "SELECT DISTINCT ON (city) ID, city, district FROM place "
                        else:
                            query = "SELECT ID, city, district FROM place "

                        query += helpers.check_where_exist(query, self.city, r"city LIKE '%{}%'")
                        query += helpers.check_where_exist(query, self.district, r"district LIKE '%{}%'")

                        cursor.execute(query)
                        records = cursor.fetchall()  # records = [(id,city,district),(id2,city2,district2)]
            except (Exception, dbapi2.Error) as error:
                print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
            else:
                place_objects = list()
                for id_, city, district in records:
                    place_objects.append(
                        Place(city=city, district=district, id=id_))  # record = (id,city,district)
                return place_objects

        def get_object(self) -> object:
            """
            READ
            It returns object according to id
            :return: object
            """
            try:
                with dbapi2.connect(db_url) as connection:
                    with connection.cursor() as cursor:
                        query = "SELECT ID, city, district FROM place WHERE id = {}  ".format(self.id)
                        cursor.execute(query)
                        record = cursor.fetchone()
            except (Exception, dbapi2.Error) as error:
                print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
            else:
                if record is None:
                    return None
                else:
                    place = Place(city=record[1], district=record[2], id=record[0])  # record = (id,city,district)
                    return place

        def save(self):
            """
            CREATE
            It saves the object to database
            """
            try:
                with dbapi2.connect(db_url) as connection:
                    with connection.cursor() as cursor:
                        query = "INSERT INTO place(city, district) VALUES('{}','{}') RETURNING id".format(self.city,
                                                                                                          self.district)
                        cursor.execute(query)
                        record = cursor.fetchone()

            except (Exception, dbapi2.Error) as error:
                print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
            else:
                self.id = record[0]

        def delete(self) -> None:
            """
            DELETE
            It deletes object in database according to id
            """
            try:
                with dbapi2.connect(db_url) as connection:
                    with connection.cursor() as cursor:
                        query = "DELETE FROM place WHERE id = '{}' ".format(self.id)
                        cursor.execute(query)

            except dbapi2.Error as error:
                print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
            except Exception as e:
                print(e, file=sys.stderr)

        def update(self, city: str = None, district: str = None) -> None:
            """
            UPDATE
            It updates the object according to given parameters.
            """
            if city is not None:
                self.city = city.upper()
            if district is not None:
                self.district = district.upper()
            try:
                with dbapi2.connect(db_url) as connection:
                    with connection.cursor() as cursor:
                        query = "UPDATE place SET city='{}', district='{}' WHERE (id='{}') " \
                            .format(self.city, self.district, self.id)
                        cursor.execute(query)

            except dbapi2.Error as error:
                print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
            except Exception as e:
                print(e, file=sys.stderr)

        def __str__(self):
            return "{}: {} {}".format(self.__class__.__name__, self.city, self.district)

This is our place model. Models are our fundamental tool to make database management easily. It consist of 6 parts. First there is constructor then, get_objects, get_object, save, delete and update.

get_objects: returns objects according to city and district
get_object: returns object according to id
save: saves the object to database
delete: deletes object in database according to id
update: updates the object according to given parameters.

Models are also available for doctor, human, hospital, appointment and history. They all have the same attributes with place. Early parts of the models done collectively.

.. code-block:: python
    <!doctype html>
    <html lang="en">
    <head>
        <title>{% block title %}MedCheck{% endblock %}</title>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">


        <link rel="stylesheet" href="../static/bootstrap-4.3.1-dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.6.1/css/all.css" integrity="sha384-gfdkjb5BdAXd+lj+gudLWI+BXq4IuLW5IT+brZEZsLFm++aCMlF1V92rMkPaX4PP" crossorigin="anonymous">



    </head>
    <body>

    {% if user_auth == 'admin' %}
    {% include 'navbars/admin_navbar.html' %}
        {% elif user_auth == 'doctor' %}
        {% include 'navbars/doctor_navbar.html' %}
        {% elif user_auth == 'normal' %}
        {% include 'navbars/normal_navbar.html' %}
    {% endif %}



    {% block body %}

    {% endblock %}



    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
            integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
            crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
            integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
            crossorigin="anonymous"></script>

    <script src="../static/bootstrap-4.3.1-dist/js/bootstrap.min.js"></script>

    {% block JS %}

    {% endblock %}


    </body>
    </html>

This is the base.html which other pages are extend from.

.. code-block:: python
    <nav class="navbar navbar-expand-lg navbar-dark bg-info">
      <a class="navbar-brand" href="/">
          <img src="{{ url_for('static', filename = 'medchecklogo.png') }}" width="30" height="30" class="d-inline-block align-top" alt="">
        MedCheck
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarText">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item {% if url_for('home_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('home_page') }}">Home </a>
          </li>

        <li class="nav-item {% if url_for('admin_places_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('admin_places_page') }}">Places </a>
          </li>

          <li class="nav-item {% if url_for('admin_hospitals_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('admin_hospitals_page') }}">Hospitals </a>
          </li>
          <li class="nav-item {% if url_for('admin_humans_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('admin_humans_page') }}">Humans </a>
          </li>
            <li class="nav-item {% if url_for('how_to_use_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('how_to_use_page') }}">How to Use </a>
          </li>
            <li class="nav-item {% if url_for('login_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('login_page') }}">Log in </a>
          </li>
            <li class="nav-item  {% if url_for('register_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('register_page') }}">Register </a>
          </li>
            <li class="nav-item {% if url_for('hospital_patient_page') == url_for(request.endpoint) %}active{% endif %}">
            <a class="nav-link" href="{{ url_for('hospital_patient_page') }}">Hospital for Patient </a>
          </li>
        </ul>
        <span class="navbar-text " style="margin-right: 20px">
          <a href="#">Profile</a>
        </span>
        <span class="navbar-text">
          <a href="{{ url_for('logout') }}">Logout</a>
        </span>
      </div>
    </nav>
This page shows which sections admin can access. doctor_navbar.html and normal_navbar have limited authority compared to admin.

.. code-block:: python
    {% if hospitals %}
    <br>
    <hr>
    <h4 class="text-center">HOSPITALS</h4>

    <table class="table table-hover table-inverse">
        <thead class="thead-inverse">
        <tr>
            <th>Name</th>
            <th>Address</th>
            <th>Rate</th>
            <th>Capacity</th>
            <th>Handicapped</th>
            <th>Park</th>
            <th>Options</th>
        </tr>
        </thead>
        <tbody>
        {% for hospital in hospitals %}
        <tr id="tr_{{ hospital.id }}">
            <td>{{ hospital.name }}</td>
            <td>{{ hospital.address.city }}/{{ hospital.address.district }}</td>
            <td>{{ hospital.rate }}</td>
            <td>{{ hospital.capacity }}</td>
            <td>{{ hospital.handicapped }}</td>
            <td>{{ hospital.park }}</td>
            <td>
                <a data-toggle="modal" data-target="#update_modal" onclick="update_modal({{ hospital.id }});" href="#">
                    <i class="fa fa-edit"></i>
                </a>
                <a href="{{ url_for('del_hospital', hospital_id = hospital.id) }}"><i class="fa fa-trash-alt"></i></a>
            </td>
        </tr>
        {% endfor %}

        </tbody>
    </table>
    {% endif %}
sub_templates shows the result of search done according to doctor, place or human.

