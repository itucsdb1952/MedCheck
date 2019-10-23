import psycopg2 as dbapi2

DSN = {'user': "postgres",
       'password': "1234",
       'host': "127.0.0.1",
       'port': "5432",
       'database': "hebe"
       }

create_statement = '''
CREATE TABLE Place
  (ID INT PRIMARY KEY     NOT NULL,
  City varchar(255)    NOT NULL,
  State varchar(255)    NOT NULL,
  Hospital varchar(255) 
);

CREATE TABLE Docktor
  (ID INT PRIMARY KEY     NOT NULL,
  Human INT REFERENCES Human(TC) ,
  Workdays varchar(255)    NOT NULL, -- 1:monday .. 7:sunday
  Expertise varchar(255)    NOT NULL,
  Hospital varchar(255)    NOT NULL
);

CREATE TABLE History -- Sickness history
  (ID INT PRIMARY KEY     NOT NULL,
  Date TIMESTAMP NOT NULL,
  Doctor INT REFERENCES Docktor(ID),
  Sick varchar(255)    NOT NULL,
  Hospital varchar(255)    NOT NULL --
);

CREATE TABLE Human
  (TC INT PRIMARY KEY     NOT NULL,
  Authorize varchar(255) NOT NULL, -- ADMIN, DOCTOR, STAFF, NORMAL
  Name varchar(255)    NOT NULL,
  Surname varchar(255)    NOT NULL,
  Mail varchar(255)    NOT NULL,
  Adress INT REFERENCES Place(ID),
  Age INT,
  Height INT,
  Weight INT
);
'''

try:
    with dbapi2.connect(**DSN) as connection:
        with connection.cursor() as cursor:
            # Print PostgreSQL Connection properties
            print(connection.get_dsn_parameters(), "\n")

            # Print PostgreSQL version
            cursor.execute("SELECT version();")
            record = cursor.fetchone()

            cursor.execute(create_statement)
            connection.commit()
            print("Table created successfully in PostgreSQL ")

            print("You are connected to - ", record, "\n")

except (Exception, dbapi2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing database connection.
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
