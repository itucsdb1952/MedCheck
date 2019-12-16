Parts Implemented by Furkan Guvenc
==================================


.. code-block:: python
	:linenos:
	
	def add_hospital(name: str = None, city: str = None, district: str = None, park: bool = False,
                 handicapped: bool = True) -> str:
    try:
        with dbapi2.connect(db_url) as connection:
            with connection.cursor() as cursor:

                address = get_address_id(cursor, city, district)

                add_statement = "INSERT INTO hospital(name, address,park,handicapped) " \
                                "VALUES('{}',{},'{}','{}');".format(name, address, park, handicapped)

                cursor.execute(add_statement)
                return "Succesfull"

    except (Exception, dbapi2.Error) as error:
        print("Error while connecting to PostgreSQL: {}".format(error), file=sys.stderr)
        return str(error)

    finally:
        if connection:
			cursor.close()
			connection.close()

add_hospital function called when add hospital button is clicked in admin_hospital.html file. This function takes all features that can not be NULL and creates a hospital.