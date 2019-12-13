import psycopg2 as dbapi2
import sys
from settings import db_url


def get_hospitals_with_place(limit: int = 100, city: str = None, district: str = None) -> list:
    """

    :param limit:
    :param city:
    :param district:
    :return:
    """

    try:
        with dbapi2.connect(db_url) as connection:
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

                statement += "ORDER BY name LIMIT {}".format(limit)

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


def add_human(tc, password, authorize, name, surname, mail, address) -> str:
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                print(tc, password, authorize, name, surname, mail, address)
                statement = "insert into human " \
                            "values ('{}','{}','{}','{}','{}','{}','{}');".format(tc, password, authorize, name,
                                                                                  surname, mail, address)
                cursor.execute(statement)
                return "successful"

    except (Exception, dbapi2.Error) as error:
        return "Error"
    finally:
        if connection:
            cursor.close()
            connection.close()


def delete_doctor(doctor_tc) -> str:
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                statement = "delete from doctor where id = '{}';".format(doctor_tc)
                cursor.execute(statement)
                return "successful"
    finally:
        if connection:
            cursor.close()
            connection.close()


def add_doctor(human_id, workdays, expertise, hospital_id):
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                print("yeni doktordayız")
                statement = "insert into doctor(human, workdays, expertise, hospital)" \
                            "values('{}','{}','{}','{}');".format(human_id, workdays, expertise, hospital_id)
                cursor.execute(statement)
                return "successful"

    finally:
        if connection:
            cursor.close()
            connection.close()


def log_in(tc, password):
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                statement = "select password from human where tc='{}';".format(tc)
                cursor.execute(statement)
                result = cursor.fetchone()[0]
                if result == password:
                    return "congrats"
                return "sth is wrong"
    finally:
        if connection:
            cursor.close()
            connection.close()


def select_doctor(id):
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                return "sth"
    finally:
        if connection:
            print("s")
