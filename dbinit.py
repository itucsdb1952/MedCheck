import os
import sys

import psycopg2 as dbapi2


def read_sql_from_file(filename: str) -> list:
    with open(filename, 'r') as f:
        content = f.read()
        content = content.split(';')
        content = [row + ";" for row in content]
        return content


def initialize(url: str) -> None:
    with dbapi2.connect(url) as connection:
        with connection.cursor() as cursor:

            drop_statements = read_sql_from_file('drop_tables.sql')
            for statement in drop_statements:
                cursor.execute(statement)

            create_statements = read_sql_from_file('create_tables.sql')
            for statement in create_statements:
                cursor.execute(statement)

            add_place_statements = read_sql_from_file('places.sql')
            for statement in add_place_statements:
                cursor.execute(statement)

            add_hospital_statements = read_sql_from_file('hospitals.sql')
            for statement in add_hospital_statements:
                cursor.execute(statement)


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
