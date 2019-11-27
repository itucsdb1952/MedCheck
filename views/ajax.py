import psycopg2 as dbapi2
import sys
from settings import db_url

def get_districts(city: str = None) -> list:
    """

    :param city:
    :return:
    """

    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:
                if city:
                    statement = "SELECT district FROM place WHERE city = '{}'".format(city)

                    cursor.execute(statement)
                    record = cursor.fetchall()
                    return record
                else:
                    return [('il seciniz',)]

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()