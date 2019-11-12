import psycopg2 as dbapi2
import sys
import os

DSN = {'user': "postgres",
       'password': "1234",
       'host': "127.0.0.1",
       'port': "5432",
       'database': "hebe2"
       }


def get_hospitals(limit: int = 100, city: str = None, district: str = None) -> list:
    """

    :param limit:
    :param city:
    :param district:
    :return:
    """

    try:
        # with dbapi2.connect(os.getenv(**DSN)) as connection: TODO: LOCAL
        with dbapi2.connect(os.getenv("DATABASE_URL")) as connection:  # TODO: HOST
            with connection.cursor() as cursor:
                statement = "SELECT hospital.name, place.city, place.district, hospital.rate, hospital.handicapped, hospital.park " \
                            "FROM hospital, place "
                if city:
                    if district:  # city and district
                        statement += "WHERE hospital.address = place.id AND place.city = '{}' " \
                                     "AND place.district = '{}' ".format(city, district)
                    else:  # just city
                        statement += "WHERE hospital.address = place.id AND place.city = '{}' ".format(city)

                elif district:  # just district
                    statement += "WHERE hospital.address = place.id AND place.district = '{}' ".format(district)
                else:  # fetch all hospitals
                    statement += "WHERE hospital.address = place.id "

                statement += "LIMIT {}".format(limit)

                cursor.execute(statement)
                record = cursor.fetchall()
                return record

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()

