import psycopg2
import bills
import suppliers
import get_dat_config as config

DATABASE_CONFIG_PATH = "./database_configuration.json"
DATABASE_CONFIG_HOSTNAME = "hostname"
DATABASE_CONFIG_DATABASENAME="database"
DATABASE_CONFIG_USERNAME = "user"
DATABASE_CONFIG_DATABASEPASSWORD = "password"
DATABASE_CONFIG_PORT = "port"


def database(invoice):
    data = config.get_config()
    hostname = data.hostname
    database = data.database
    user = data.user
    password = data.password
    port = data.port

    try:
        connect = psycopg2.connect(
            host=hostname,
            database=database,
            user=user,
            password=password,
            port=port)

        cursor = connect.cursor()


        cursor.execute(bills.create())
        connect.commit()

        cursor.execute(bills.insert(), (invoice.vendor_name, invoice.total_amount_without_vat, invoice.date))
        connect.commit()

        #cursor.execute(bills.insert(), (2, 'Frantisek', 29.99, '18.9.2008') )
        #connect.commit()

        #if(bills.get_column(cursor, 1, 'price') is None):
            #print("error")
        #number = cursor.fetchone()
        #connect.commit()
        #print(number)
    except Exception as error:
        print("error: ")

    finally:
        if cursor is not None:
            cursor.close()
        if connect is not None:
            connect.close()


def log_in_create():
    data = config.get_config()
    hostname = data.hostname
    database = data.database
    user = data.user
    password = data.password
    port = data.port

    try:
        connect = psycopg2.connect(
            host=hostname,
            database=database,
            user=user,
            password=password,
            port=port)

        cursor = connect.cursor()

        cursor.execute(bills.create())
        cursor.execute(suppliers.create())
        connect.commit()

    except Exception as error:
        print("error: cant create database")

    finally:
        if cursor is not None:
            cursor.close()
        if connect is not None:
            connect.close()
