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
            self.city = args[0]
            self.district = args[1]
        elif len(args) == 1:
            self.city = args[0]
            self.district = None

        if 'city' in kwargs.keys():
            self.city = kwargs['city']
        if 'district' in kwargs.keys():
            self.district = kwargs['district']
        if 'id' in kwargs.keys():
            self.__id = kwargs['id']

    def get_objects(self) -> list:
        """
        READ
        It returns objects according to city and district
        :return: list of place objects
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT ID FROM place WHERE (city = '{}' AND district = '{}');".format(
                        self.city,
                        self.district)
                    cursor.execute(address_statement)
                    records = cursor.fetchall()  # records = [(id,),(id2,)]
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            place_objects = list()
            for record in records:
                place_objects.append(Place(self.city, self.district, id=record[0]))  # record = (id,)
            return place_objects

    @property
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
                    records = cursor.fetchall()
                    print(len(records), records)
                    if len(records) > 1:
                        raise ValueError("There are more then one place object!")
                    elif len(records) == 0:
                        raise ValueError("There is no place object!")
        except ValueError as e:
            print(e, file=sys.stderr)
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        else:
            self.__id = records[0][0]
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

        except ValueError as e:
            print(e, file=sys.stderr)
        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

        else:
            self.__id = self.__get_id
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

    def update(self, new_city: str, new_district: str) -> None:
        """
        UPDATE
        :param new_city: city will be change with it
        :param new_district: district will be change with it
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    update_statement = "UPDATE place SET city='{}', district='{}' WHERE (city='{}' AND district= '{}');"\
                        .format(new_city, new_district, self.city, self.district)
                    cursor.execute(update_statement)

        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return "Place: {} {}".format(self.city, self.district)


class Hospital:
    def __init__(self, name: str, address: Place, rate: int, capacity: int, handicapped: bool, park: bool,
                 id_: int = None):

        self.address = address
        self.name = name
        self.park = park
        self.rate = rate
        self.capacity = capacity
        self.handicapped = handicapped
        self.id = id_

    @property
    def __get_id(self) -> int:
        """
        It returns hospital id from hospital table according to name and address

        :return: Hospital id
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT ID FROM hospital WHERE (name = '{}' AND address = '{}');".format(
                        self.name,
                        self.address.id)
                    cursor.execute(address_statement)



        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
            return -1

        else:
            self.id = cursor.fetchone()[0]
            return self.id

    def save(self):
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    insert_statement = "INSERT INTO hospital(name, address, rate, capacity, handicapped, park)" \
                                       " VALUES('{}','{}','{}','{}','{}','{}');".format(self.name, self.address.id,
                                                                                        self.rate, self.capacity,
                                                                                        self.handicapped, self.park)
                    cursor.execute(insert_statement)

        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
            return -1

        else:
            self.id = self.__get_id
            return self.id

    @property
    def id(self):
        if self.id is None:
            self.id = self.__get_id
        return self.id

    @id.setter
    def id(self, value):
        self._id = value
