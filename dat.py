import psycopg2
import bills
import items
import suppliers
import helper_functions

hostname = 'localhost'
database = 'postgres'
user = 'postgres'
password = 'admin'
port = '5432'

try:
    connect = psycopg2.connect(
        host=hostname,
        database=database,
        user=user,
        password=password,
        port=port)

    cursor = connect.cursor()


    #cursor.execute(bills.create())
    #connect.commit()

    #cursor.execute(bills.insert())
    #connect.commit()

    number = bills.get_column(cursor, 1, 'price')
    #number = cursor.fetchone()
    #connect.commit()
    print(number)
except Exception as error:
    print(error)

finally:
    if cursor is not None:
        cursor.close()
    if connect is not None:
        connect.close()



