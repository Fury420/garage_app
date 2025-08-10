import psycopg2
import bills


def database(invoice):
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

        cursor.execute(bills.insert(), (2, invoice.vendor_name, invoice.total_amount_without_vat, invoice.date))
        connect.commit()

        #cursor.execute(bills.insert(), (2, 'Frantisek', 29.99, '18.9.2008') )
        #connect.commit()

        #if(bills.get_column(cursor, 1, 'price') is None):
            #print("error")
        #number = cursor.fetchone()
        #connect.commit()
        #print(number)
    except Exception as error:
        print(error)

    finally:
        if cursor is not None:
            cursor.close()
        if connect is not None:
            connect.close()



