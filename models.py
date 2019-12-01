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
        :return: list of place objects
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
                    update_statement = "UPDATE place SET city='{}', district='{}' WHERE (city='{}' AND district= '{}');" \
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
    def __init__(self, *args, **kwargs):

        self.name = None
        self.address = None
        self.rate = None  # not needed
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
        :return: list of hospital objects
        """
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT id,name,address,rate,capacity,handicapped,park FROM hospital "
                    if self.name and self.address:
                        address_statement += "WHERE (name = '{}' AND address = '{}');".format(self.name, self.address.id)
                    elif self.name:
                        address_statement += "WHERE (name = '{}');".format(self.name)
                    elif self.address:
                        address_statement += "WHERE (address = '{}');".format(self.address.id)
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

                    address_statement = "SELECT ID FROM hospital WHERE (name = '{}');".format(self.name)
                    cursor.execute(address_statement)
                    records = cursor.fetchall()
                    if len(records) > 1:
                        raise ValueError("There are more then one hospital object!")
                    elif len(records) == 0:
                        raise ValueError("There is no hospital object!")
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
                    insert_statement = "INSERT INTO hospital(name, address, rate, capacity, handicapped, park)" \
                                       " VALUES('{}','{}','{}','{}','{}','{}');".format(self.name, self.address.id,
                                                                                        self.rate, self.capacity,
                                                                                        self.handicapped, self.park)
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
                    delete_statement = "DELETE FROM hospital WHERE id = '{}';".format(self.__id)
                    cursor.execute(delete_statement)


        except dbapi2.Error as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        except Exception as e:
            print(e, file=sys.stderr)

    # def update(self, new_city: str, new_district: str) -> None:
    #     """
    #     UPDATE
    #     :param new_city: city will be change with it
    #     :param new_district: district will be change with it
    #     """
    #     try:
    #         with dbapi2.connect(db_url) as connection:
    #             with connection.cursor() as cursor:
    #                 update_statement = "UPDATE place SET city='{}', district='{}' WHERE (city='{}' AND district= '{}');" \
    #                     .format(new_city, new_district, self.city, self.district)
    #                 cursor.execute(update_statement)
    #
    #     except dbapi2.Error as error:
    #         print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
    #     except Exception as e:
    #         print(e, file=sys.stderr)

    @property
    def id(self):
        return self.__id

    def __str__(self):
        return "Hospital: {} {} {} {}".format(self.name, self.capacity, self.handicapped, self.park)
