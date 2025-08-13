from typing import Union
import helper_functions
from psycopg2._psycopg import cursor, connection, Error, Warning


INSERT_QUERY = '''INSERT INTO bills (supplier, price, date)
                VALUES (%s, %s, %s);'''

CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS bills (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                                                    supplier VARCHAR(40), 
                                                    price REAL, 
                                                    date DATE);'''

DELETE_QUERY = '''DELETE FROM bills WHERE id = %s;'''

SELECT_QUERY = '''SELECT * FROM bills WHERE id = %s;'''

SELECT_COLUMN_QUERY = '''SELECT %s FROM bills WHERE id = %s;'''


#inserts row into the table bills
def insert(db_cursor: cursor) -> bool:
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


#creates new table bills with columns: id, supplier, price, date
def create(db_cursor: cursor) -> bool:
    try:
        query = CREATE_QUERY
        db_cursor.execute(query, ())

    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#deletes from table bills
def delete(db_cursor:cursor, id_num: int) -> bool:
    try:
        query = DELETE_QUERY
        db_cursor.execute(query, (id_num,))

    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#return the whole row of table bills where the id matches
def select(db_cursor: cursor, id_num: int) -> tuple[int, str, float, str] | None:
    try:
        query = INSERT_QUERY
        db_cursor.execute(query, (id_num,))
        row = db_cursor.fetchone()
    except Warning as e:
        print(e.__class__.__name__)
        return None
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return None
    return row


#return a specific value from table bills
def get_column(db_cursor: cursor, id_num: int, column: str) -> int | str | float | None:
    allowed_columns = ['supplier', 'price', 'id', 'date']
    if column not in allowed_columns:
        return None
    return helper_functions.get_column_value(db_cursor, SELECT_COLUMN_QUERY, column, id_num)
