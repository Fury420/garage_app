import psycopg2
import create

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
    test = '''CREATE TABLE IF NOT EXISTS ahoj (id int PRIMARY KEY, name VARCHAR(50))'''
    cursor.execute(test)
    #cursor.execute(create.create_faktura())
    connect.commit()
    print("ahoj")
except Exception as error:
    print(error)

finally:
    if cursor is not None:
        cursor.close()
    if connect is not None:
        connect.close()



