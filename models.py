import psycopg2 as dbapi2
import sys
from settings import db_url


# CRUD
# get objects, objeli ver
# get object, id e göre objeyi döner
# save, obje verilir id li keydeder
# update, obje verilir id li kaydeder
# delete, id e göre siler

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
        :return: list of objects
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    if distinct_city:
                        address_statement = "SELECT DISTINCT ON (city) ID, city, district FROM place "
                    else:
                        address_statement = "SELECT ID, city, district FROM place "
                    if self.city and self.district:
                        address_statement += f"WHERE (city = '{self.city}' AND district = '{self.district}');"
                    elif self.city:
                        address_statement += f"WHERE (city = '{self.city}');"
                    elif self.district:
                        address_statement += f"WHERE (district = '{self.district}');"
                    cursor.execute(address_statement)
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
                    address_statement = "SELECT ID, city, district FROM place WHERE id = {} ;".format(self.id)
                    cursor.execute(address_statement)
                    record = cursor.fetchone()  # record = (id,city,district),
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            place = Place(city=record[1], district=record[2], id=record[0])  # record = (id,city,district)
            return place

    def __get_id(self) -> int:
        """
        READ
        It returns address id according to city and district
        :return: Object id
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT ID FROM place WHERE (city = '{}' AND district = '{}');".format(
                        self.city,
                        self.district)
                    cursor.execute(address_statement)
                    record = cursor.fetchone()
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            self.id = record[0]
            return self.id

    def save(self):
        """
        CREATE
        It saves the object to database
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    insert_statement = "INSERT INTO place(city, district) VALUES('{}','{}');".format(self.city,
                                                                                                     self.district)
                    cursor.execute(insert_statement)

        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            self.id = self.__get_id()

    def delete(self) -> None:
        """
        DELETE
        It deletes object in database according to id
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    delete_statement = "DELETE FROM place WHERE id = '{}';".format(self.id)
                    cursor.execute(delete_statement)

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
            self.city = city
        if district is not None:
            self.district = district
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    update_statement = "UPDATE place SET city='{}', district='{}' WHERE (id='{}');" \
                        .format(self.city, self.district, self.id)
                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def __str__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.city, self.district)


class Hospital:
    def __init__(self, *args, **kwargs):

        self.name = None
        self.address = None  # Place object
        self.rate = 0  # not needed
        self.capacity = 5
        self.handicapped = True
        self.park = False
        self.id = None

        if len(args) >= 6:
            self.name, self.address, self.rate, self.capacity, self.handicapped, self.park = args[:6]
        elif len(args) == 5:
            self.name, self.address, self.rate, self.capacity, self.handicapped = args[:5]
        elif len(args) == 4:
            self.name, self.address, self.rate, self.capacity = args[:4]
        elif len(args) == 3:
            self.name, self.address, self.rate = args[:3]
        elif len(args) == 2:
            self.name, self.address = args[:2]

        if 'name' in kwargs.keys():
            self.name = kwargs['name']
        if 'address' in kwargs.keys():
            self.address = kwargs['address']
        if 'rate' in kwargs.keys():
            self.rate = kwargs['rate']
        if 'capacity' in kwargs.keys():
            self.capacity = kwargs['capacity']
        if 'handicapped' in kwargs.keys():
            self.handicapped = kwargs['handicapped']
        if 'park' in kwargs.keys():
            self.park = kwargs['park']
        if 'id' in kwargs.keys():
            self.id = kwargs['id']

    def get_objects(self, limit: int = 100) -> list:
        """
        READ
        It returns objects according to [address, name, address and name]
        :return: list of objects
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT id,name,address,rate,capacity,handicapped,park FROM hospital "
                    if self.name and self.address:
                        address_statement += f"WHERE (name = '{self.name}' AND address = '{self.address.id}') "
                    elif self.name:
                        address_statement += f"WHERE (name = '{self.name}') "
                    elif self.address:
                        address_statement += f"WHERE (address = '{self.address.id}') "
                    if limit:
                        address_statement += f"LIMIT {limit}"

                    cursor.execute(address_statement)
                    records = cursor.fetchall()  # records = [(id,city,district),(id2,city2,district2)]
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            objects = list()
            for id_, name, address_id, rate, capacity, handicapped, park in records:
                objects.append(
                    Hospital(name=name, address=Place(id=address_id).get_object(), rate=rate, capacity=capacity,
                             handicapped=handicapped, park=park, id=id_))
            return objects

    def get_object(self) -> object:
        """
        READ
        It returns object according to id
        :return: object
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    query = f"SELECT id,name,address,rate,capacity,handicapped,park FROM hospital WHERE id = {self.id} ;"
                    cursor.execute(query)
                    record = cursor.fetchone()  # record = (id,city,district),
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            id_, name, address, rate, capacity, handicapped, park = record
            hospital = Hospital(name=name, address=Place(id=address).get_object(), rate=rate, capacity=capacity,
                                handicapped=handicapped, park=park, id=id_)  # record = (id,city,district)
            return hospital

    def __get_id(self) -> int:
        """
        READ
        It returns hospital id according to [name and address]
        :return: Object id
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = f"SELECT ID FROM hospital WHERE (name = '{self.name}' AND address = '{self.address.id}'); "
                    cursor.execute(address_statement)
                    record = cursor.fetchone()
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            self.id = record[0]
            return self.id

    def save(self):
        """
        CREATE
        It saves the object to database
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    insert_statement = "INSERT INTO hospital(name, address, rate, capacity, handicapped, park)" \
                                       f" VALUES('{self.name}','{self.address.id}','{self.rate}','{self.capacity}','{self.handicapped}','{self.park}');"
                    cursor.execute(insert_statement)

        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)

        else:
            self.id = self.__get_id()

    def delete(self) -> None:
        """
        DELETE
        It deletes object in database according to id
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    delete_statement = f"DELETE FROM hospital WHERE id = '{self.id}';"
                    cursor.execute(delete_statement)

        except dbapi2.Error as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def update(self, name: str = None, address: Place = None, rate: int = None, capacity: int = None,
               handicapped: bool = None, park: bool = None) -> None:
        """
        UPDATE
        It updates the object according to given parameters.
        """
        if name is not None:
            self.name = name
        if address is not None:
            self.address = address
        if rate is not None:
            self.rate = rate
        if capacity is not None:
            self.capacity = capacity
        if handicapped is not None:
            self.handicapped = handicapped
        if park is not None:
            self.park = park
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    update_statement = f"UPDATE hospital SET name='{self.name}', address='{self.address.id}'," \
                                       f" rate='{self.rate}', capacity='{self.capacity}', " \
                                       f"handicapped='{self.handicapped}', park='{self.park}' WHERE (id='{self.id}');"

                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} C:{self.capacity} H:{self.handicapped} P:{self.park}"


class Human:
    def __init__(self, *args, **kwargs):

        self.tc = None
        self.password = None
        self.authorize = 'normal'  # ADMIN, DOCTOR, STAFF, NORMAL
        self.name = None
        self.surname = None
        self.mail = None
        self.address = None
        self.age = 0  # not needed
        self.weight = 0  # not needed
        self.height = 0  # not needed

        if len(args) >= 10:
            self.tc, self.password, self.authorize, self.name, self.surname, self.mail, self.address, self.age, self.weight, self.height = args[
                                                                                                                                           :10]
        elif len(args) == 9:
            self.tc, self.password, self.authorize, self.name, self.surname, self.mail, self.address, self.age, self.weight = args[
                                                                                                                              :9]
        elif len(args) == 8:
            self.tc, self.password, self.authorize, self.name, self.surname, self.mail, self.address, self.age = args[
                                                                                                                 :8]
        elif len(args) == 7:
            self.tc, self.password, self.authorize, self.name, self.surname, self.mail, self.address = args[:7]
        elif len(args) == 6:
            self.tc, self.password, self.authorize, self.name, self.surname, self.mail = args[:6]
        elif len(args) == 5:
            self.tc, self.password, self.authorize, self.name, self.surname = args[:5]
        elif len(args) == 4:
            self.tc, self.password, self.authorize, self.name = args[:4]
        elif len(args) == 3:
            self.tc, self.password, self.authorize = args[:3]
        elif len(args) == 2:
            self.tc, self.password = args[:2]
        elif len(args) == 1:
            self.tc = args[:1]

        if 'tc' in kwargs.keys():
            self.tc = kwargs['tc']
        if 'password' in kwargs.keys():
            self.password = kwargs['password']
        if 'authorize' in kwargs.keys():
            self.authorize = kwargs['authorize']
        if 'name' in kwargs.keys():
            self.name = kwargs['name']
        if 'surname' in kwargs.keys():
            self.surname = kwargs['surname']
        if 'mail' in kwargs.keys():
            self.mail = kwargs['mail']
        if 'address' in kwargs.keys():
            self.address = kwargs['address']
        if 'age' in kwargs.keys():
            self.age = kwargs['age']
        if 'weight' in kwargs.keys():
            self.weight = kwargs['weight']
        if 'height' in kwargs.keys():
            self.height = kwargs['height']

    def get_objects(self) -> list:
        """
        READ
        It returns objects according to name and surname, name, surname, address, authorize
        :return: list of objects
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    query = "SELECT tc, password, authorize, name, surname, mail, address, age, height, weight FROM human "
                    if self.name and self.surname:
                        query += f"WHERE (name = '{self.name}' AND surname = '{self.surname}');"
                    elif self.name:
                        query += f"WHERE (name = '{self.name}');"
                    elif self.surname:
                        query += f"WHERE (surname = '{self.surname}');"
                    elif self.authorize:
                        query += f"WHERE (authorize = '{self.authorize}');"
                    elif self.address:
                        query += f"WHERE (address = '{self.address}');"
                    cursor.execute(query)
                    records = cursor.fetchall()
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            objects = list()
            for tc, password, authorize, name, surname, mail, address, age, height, weight in records:
                objects.append(
                    Human(tc, password, authorize, name, surname, mail, Place(id=address).get_object(), age, height,
                          weight))
            return objects

    def get_object(self) -> object:
        """
        READ
        It returns object according to tc
        :return: object
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    query = f"SELECT tc, password, authorize, name, surname, mail, address, age, height, weight FROM human WHERE tc = {self.tc} ;"
                    cursor.execute(query)
                    record = cursor.fetchone()  # record = (id,city,district),
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            tc, password, authorize, name, surname, mail, address, age, height, weight = record
            human = Human(name=name, surname=surname, authorize=authorize, mail=mail,
                          address=Place(id=address).get_object(), password=password, age=age, height=height,
                          weight=weight, tc=tc)  # record = (id,city,district)
            return human

    def save(self):
        """
        CREATE
        It saves the object to database
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    query = "INSERT INTO human(tc, password, authorize, name, surname, mail, address, age, height, weight)" \
                            " VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(self.tc,
                                                                                                 self.password,
                                                                                                 self.authorize,
                                                                                                 self.name,
                                                                                                 self.surname,
                                                                                                 self.mail,
                                                                                                 self.address.id,
                                                                                                 self.age,
                                                                                                 self.height,
                                                                                                 self.weight)
                    cursor.execute(query)

        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)

    def delete(self) -> None:
        """
        DELETE
        It deletes object in database according to tc
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    delete_statement = f"DELETE FROM human WHERE tc = '{self.tc}';"
                    cursor.execute(delete_statement)

        except dbapi2.Error as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def update(self, tc: str = None, password: str = None, authorize: str = None, name: str = None,
               surname: str = None, mail: str = None, address: Place = None, age: int = None, weight: int = None,
               height: int = None) -> None:
        """
        UPDATE
        It updates the object according to given parameters.
        """

        if password is not None:
            self.password = password
        if authorize is not None:
            self.authorize = authorize
        if name is not None:
            self.name = name
        if surname is not None:
            self.surname = surname
        if mail is not None:
            self.mail = mail
        if address is not None:
            self.address = address
        if age is not None:
            self.age = age
        if weight is not None:
            self.weight = weight
        if height is not None:
            self.height = height
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    update_statement = "UPDATE human SET tc='{}', password='{}', authorize='{}', name='{}'," \
                                       " surname='{}', mail='{}', address='{}', age='{}', weight='{}', height='{}'" \
                                       " WHERE (tc='{}');".format(tc,
                                                                  self.password,
                                                                  self.authorize,
                                                                  self.name,
                                                                  self.surname,
                                                                  self.mail,
                                                                  self.address.id,
                                                                  self.age,
                                                                  self.height,
                                                                  self.weight,
                                                                  self.tc)

                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)
        else:
            self.tc = tc

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name} {self.surname} TC:{self.tc}"


class Doctor:
    def __init__(self, *args, **kwargs):

        self.human = None  # Human object
        self.workdays = None
        self.expertise = None
        self.hospital = None  # Hospital object
        self.rate = 0

        if len(args) >= 5:
            self.human, self.workdays, self.expertise, self.hospital, self.rate = args[:5]
        elif len(args) == 4:
            self.human, self.workdays, self.expertise, self.hospital = args[:4]
        elif len(args) == 3:
            self.human, self.workdays, self.expertise = args[:3]
        elif len(args) == 2:
            self.human, self.workdays = args[:2]
        elif len(args) == 1:
            self.human = args[0]

        if 'human' in kwargs.keys():
            self.human = kwargs['human']
        if 'workdays' in kwargs.keys():
            self.workdays = kwargs['workdays']
        if 'expertise' in kwargs.keys():
            self.expertise = kwargs['expertise']
        if 'hospital' in kwargs.keys():
            self.hospital = kwargs['hospital']
        if 'rate' in kwargs.keys():
            self.rate = kwargs['rate']

    def get_objects(self, limit: int = 100) -> list:
        """
        READ
        It returns objects according to [workdays, hospital, workdays and hospital, expertise]
        :return: list of objects
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    query = "SELECT humantc,workdays,expertise,hospital,rate FROM doctor "
                    if self.workdays and self.hospital:
                        query += f"WHERE (workdays = '{self.workdays}' AND hospital = '{self.hospital.id}') "
                    elif self.workdays:
                        query += f"WHERE (workdays = '{self.workdays}') "
                    elif self.hospital:
                        query += f"WHERE (hospital = '{self.hospital.id}') "
                    elif self.expertise:
                        query += f"WHERE (expertise = '{self.expertise}') "
                    if limit:
                        query += f"LIMIT {limit}"

                    cursor.execute(query)
                    records = cursor.fetchall()  # records = [(id,city,district),(id2,city2,district2)]
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            objects = list()
            for humantc, workdays, expertise, hospital, rate in records:
                objects.append(
                    Doctor(human=Human(tc=humantc).get_object(), workdays=workdays, expertise=expertise,
                           hospital=Hospital(id=hospital).get_object(), rate=rate))
            return objects

    def get_object(self) -> object:
        """
        READ
        It returns object according to tc
        :return: object
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    query = f"SELECT humantc,workdays,expertise,hospital,rate FROM doctor WHERE humantc = {self.human.tc} ;"
                    cursor.execute(query)
                    record = cursor.fetchone()  # record = (id,city,district),
        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        else:
            humantc, workdays, expertise, hospital, rate = record
            doctor = Doctor(workdays=workdays, expertise=expertise, hospital=hospital, rate=rate,
                            human=humantc.tc)  # record = (id,city,district)
            return doctor

    def save(self):
        """
        CREATE
        It saves the object to database
        :return: Object id
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    query = "INSERT INTO doctor(humantc,workdays,expertise,hospital,rate)" \
                            f" VALUES('{self.human.tc}','{self.workdays}','{self.expertise}','{self.hospital.id}','{self.rate}');"
                    cursor.execute(query)

        except (Exception, dbapi2.Error) as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)

    def delete(self) -> None:
        """
        DELETE
        It deletes object in database according to id
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    delete_statement = f"DELETE FROM doctor WHERE humantc = '{self.human.tc}';"
                    cursor.execute(delete_statement)

        except dbapi2.Error as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def update(self, human: Human = None, hospital: Hospital = None, workdays: str = None, rate: int = None,
               expertise: str = None) -> None:
        """
        UPDATE
        It updates the object according to given parameters.
        """
        tc = self.human.tc

        if human is not None:
            self.human = human
        if hospital is not None:
            self.hospital = hospital
        if rate is not None:
            self.rate = rate
        if workdays is not None:
            self.workdays = workdays
        if rate is not None:
            self.rate = rate
        if expertise is not None:
            self.expertise = expertise
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    update_statement = f"UPDATE doctor SET humantc='{self.human.tc}', hospital='{self.hospital.id}'," \
                                       f" rate='{self.rate}', workdays='{self.workdays}', " \
                                       f"expertise='{self.expertise}' WHERE (humantc='{tc}');"

                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print(f"Error while connecting to PostgreSQL: {error}", file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.human.name} C:{self.human.surname} Hosp:{self.hospital.name} TC:{self.human.tc}"
