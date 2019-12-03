import psycopg2 as dbapi2
import sys
from settings import db_url


# CRUD

class Place:
    def __init__(self, *args, **kwargs):
        self.city = None
        self.district = None
        self.__id = None

        if len(args) >= 2:
            self.city, self.district = args[:2]
        elif len(args) == 1:
            self.city = args[0]

        if 'city' in kwargs.keys():
            self.city = kwargs['city']
        if 'district' in kwargs.keys():
            self.district = kwargs['district']
        if 'id' in kwargs.keys():
            self.__id = kwargs['id']

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
                        address_statement += "WHERE (city = '{}' AND district = '{}');".format(self.city, self.district)
                    elif self.city:
                        address_statement += "WHERE (city = '{}');".format(self.city)
                    elif self.district:
                        address_statement += "WHERE (district = '{}');".format(self.district)
                    cursor.execute(address_statement)
                    records = cursor.fetchall()  # records = [(id,city,district),(id2,city2,district2)]
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            place_objects = list()
            for record in records:
                place_objects.append(
                    Place(city=record[1], district=record[2], id=record[0]))  # record = (id,city,district)
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
                    address_statement = "SELECT ID, city, district FROM place WHERE id = {} ;".format(self.__id)
                    cursor.execute(address_statement)
                    record = cursor.fetchone()  # record = (id,city,district),
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
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
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            self.__id = record[0]
            return self.__id

    def save(self):
        """
        CREATE
        It saves the object to database
        :return: Object id
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    insert_statement = "INSERT INTO place(city, district) VALUES('{}','{}');".format(self.city,
                                                                                                     self.district)
                    cursor.execute(insert_statement)

        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            self.__id = self.__get_id()
            return self.__id

    def delete(self) -> None:
        """
        DELETE
        It deletes object in database according to id
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    delete_statement = "DELETE FROM place WHERE id = '{}';".format(self.__id)
                    cursor.execute(delete_statement)


        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
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
                        .format(self.city, self.district, self.__id)
                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return "{}: {} {}".format(self.__class__.__name__, self.city, self.district)


class Hospital:
    def __init__(self, *args, **kwargs):

        self.name = None
        self.address = None
        self.rate = 0  # not needed
        self.capacity = 5
        self.handicapped = True
        self.park = False
        self.__id = None

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
            self.__id = kwargs['id']

    def get_objects(self) -> list:
        """
        READ
        It returns objects according to address
        :return: list of objects
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT id,name,address,rate,capacity,handicapped,park FROM hospital "
                    if self.name and self.address:
                        address_statement += "WHERE (name = '{}' AND address = '{}');".format(self.name,
                                                                                              self.address)
                    elif self.name:
                        address_statement += "WHERE (name = '{}');".format(self.name)
                    elif self.address:
                        address_statement += "WHERE (address = '{}');".format(self.address)
                    cursor.execute(address_statement)
                    records = cursor.fetchall()  # records = [(id,city,district),(id2,city2,district2)]
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            objects = list()
            for record in records:
                objects.append(
                    Hospital(name=record[1], address=record[2], rate=record[3], capacity=record[4],
                             handicapped=record[5], park=record[6], id=record[0]))
            return objects

    def __get_id(self) -> int:
        """
        READ
        It returns address id according to city and district
        :return: Object id
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT ID FROM hospital WHERE (name = '{}' AND address = '{}');".format(
                        self.name,
                        self.address)
                    cursor.execute(address_statement)
                    record = cursor.fetchone()
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            self.__id = record[0]
            return self.__id

    def save(self):
        """
        CREATE
        It saves the object to database
        :return: Object id
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    insert_statement = "INSERT INTO hospital(name, address, rate, capacity, handicapped, park)" \
                                       " VALUES('{}','{}','{}','{}','{}','{}');".format(self.name, self.address,
                                                                                        self.rate, self.capacity,
                                                                                        self.handicapped, self.park)
                    cursor.execute(insert_statement)

        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

    def delete(self) -> None:
        """
        DELETE
        It deletes object in database according to id
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    delete_statement = "DELETE FROM hospital WHERE id = '{}';".format(self.__id)
                    cursor.execute(delete_statement)


        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def update(self, name: str = None, address: int = None, rate: int = None, capacity: int = None,
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
                    update_statement = "UPDATE hospital SET name='{}', address='{}', rate='{}', capacity='{}', handicapped='{}', park='{}' WHERE (id='{}');" \
                        .format(self.name, self.address, self.rate, self.capacity, self.handicapped, self.park,
                                self.__id)
                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return "{}: {} C:{} H:{} P:{}".format(self.__class__.__name__, self.name, self.capacity, self.handicapped,
                                              self.park)


class Human:
    def __init__(self, *args, **kwargs):

        self.tc = None
        self.password = None
        self.authorize = 'normal'  # ADMIN, DOCTOR, STAFF, NORMAL
        self.name = None
        self.surname = None
        self.mail = None
        self.address = None
        self.age = None  # not needed
        self.weight = None  # not needed
        self.height = None  # not needed

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
                    address_statement = "SELECT tc, password, authorize, name, surname, mail, address, age, height, weight FROM human "
                    if self.name and self.surname:
                        address_statement += "WHERE (name = '{}' AND surname = '{}');".format(self.name,
                                                                                              self.surname)
                    elif self.name:
                        address_statement += "WHERE (name = '{}');".format(self.name)
                    elif self.surname:
                        address_statement += "WHERE (surname = '{}');".format(self.surname)
                    elif self.authorize:
                        address_statement += "WHERE (authorize = '{}');".format(self.authorize)
                    elif self.address:
                        address_statement += "WHERE (address = '{}');".format(self.address)
                    cursor.execute(address_statement)
                    records = cursor.fetchall()
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            objects = list()
            for record in records:
                objects.append(Human(*record))
            return objects

    def save(self):
        """
        CREATE
        It saves the object to database
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    insert_statement = "INSERT INTO human(tc, password, authorize, name, surname, mail, address, age, height, weight)" \
                                       " VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}');".format(self.tc,
                                                                                                            self.password,
                                                                                                            self.authorize,
                                                                                                            self.name,
                                                                                                            self.surname,
                                                                                                            self.mail,
                                                                                                            self.address,
                                                                                                            self.age,
                                                                                                            self.height,
                                                                                                            self.weight)
                    cursor.execute(insert_statement)

        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

    def delete(self) -> None:
        """
        DELETE
        It deletes object in database according to tc
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    delete_statement = "DELETE FROM human WHERE tc = '{}';".format(self.tc)
                    cursor.execute(delete_statement)


        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    def update(self, tc: str = None, password: str = None, authorize: str = None, name: str = None,
               surname: str = None, mail: str = None, address: int = None, age: int = None, weight: int = None,
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
                                                                  self.address,
                                                                  self.age,
                                                                  self.height,
                                                                  self.weight,
                                                                  self.tc)

                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)
        else:
            self.tc = tc

    def __str__(self):
        return "{}: {} {} TC:{}".format(self.__class__.__name__, self.name, self.surname, self.tc)
