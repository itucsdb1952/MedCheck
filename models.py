import psycopg2 as dbapi2
import sys
from settings import db_url


class Place:
    def __init__(self, city: str, district: str, id_: int = None):
        self.city = city
        self.district = district
        self.__id = id_

    @property
    def __get_id(self) -> int:
        """
        It returns address id from place table according to city and district

        :return: Address id of district of city
        """

        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    address_statement = "SELECT ID FROM place WHERE (city = '{}' AND district = '{}');".format(
                        self.city,
                        self.district)
                    cursor.execute(address_statement)
                    self.__id = cursor.fetchone()[0]

        finally:
            return self.__id

    def save(self):
        try:
            with dbapi2.connect(db_url) as connection:
                with connection.cursor() as cursor:
                    insert_statement = "INSERT INTO place(city, district) VALUES('{}','{}');".format(self.city,
                                                                                                     self.district)
                    cursor.execute(insert_statement)

        except (Exception, dbapi2.Error) as error:
            print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
            return -1

        else:
            self.__id = self.__get_id
            return self.__id

    @property
    def id(self):
        if self.__id is None:
            self.__id = self.__get_id
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value
