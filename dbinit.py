import os
import sys

import psycopg2 as dbapi2

DSN = {'user': "postgres",
       'password': "101095",
       'host': "127.0.0.1",
       'port': "5432",
       'database': "hebe2"
       }


def read_sql_from_file(filename: str) -> list:
    with open(filename, 'r', encoding='windows-1254') as f:
        content = f.read()
        content = content.split(';')
        content = [row + ";" for row in content]
        return content


def initialize(url: str) -> None:
    try:
        with dbapi2.connect(**DSN) as connection:
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
    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    print("Initializing...", file=sys.stderr)
    initialize(url)
