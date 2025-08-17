import helper_functions
from psycopg2._psycopg import cursor, connection, Error, Warning
from class_invoice import InvoiceItem
from class_bill import BillItem
from psycopg2 import sql

INSERT_QUERY = f'''INSERT INTO items (description, unit_price, amount)
                VALUES (%s, %s, %s, %s);'''

CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS items (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                                                    description VARCHAR(255), 
                                                    unit_price FLOAT,
                                                    amount INTEGER);'''

DELETE_QUERY = f'''DELETE FROM items WHERE id = %s;'''

SELECT_QUERY = f'''SELECT * FROM items WHERE id = %s'''


#inserts row into the table items
def insert(db_cursor: cursor, items: InvoiceItem | BillItem) -> bool:
    try:
        query = INSERT_QUERY
        db_cursor.execute(query, ())
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#creates new table items with columns: description, unit_price, amount
def create(db_cursor: cursor) -> bool:
    try:
        query = CREATE_QUERY
        db_cursor.execute(query)
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#deletes from table employee
def delete(db_cursor: cursor, item: InvoiceItem | BillItem) -> bool:
    try:
        query = DELETE_QUERY
        db_cursor.execute(query, ())
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True