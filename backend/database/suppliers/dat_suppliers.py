from backend.database import helper_functions
from psycopg2._psycopg import cursor, Error, Warning

INSERT_QUERY = '''INSERT INTO suppliers 
                (supplier, description, address) VALUES (%s, %s, %s);'''

CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS bills (supplier VARCHAR, 
                                                    description VARCHAR, 
                                                    address VARCHAR), '''

DELETE_QUERY = '''DELETE FROM suppliers WHERE supplier = %s'''

SELECT_ALL_QUERY = '''SELECT * FROM bills WHERE supplier = %s'''

UPDATE_QUERY = f'''UPDATE suppliers SET price = %s WHERE supplier = %s'''

#inserts row into table suppliers
def insert(db_cursor: cursor, supplier: str, description: str, address: str) -> bool:
    try:
        query = INSERT_QUERY
        db_cursor.execute(query, (supplier, description, address))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True



#creates new table suppliers with columns: suppliers, description, address
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



#deletes from table suppliers
def delete(db_cursor:cursor, supp: str) -> bool:
    try:
        query = DELETE_QUERY
        db_cursor.execute(query, (supp))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#returns the whole row of table suppliers where the id matches
def select(db_cursor: cursor, supp: str) -> tuple[...] | None:
    try:
        query = SELECT_ALL_QUERY
        db_cursor.execute(query, (supp))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return


#return a specific value from suppliers
def get_column(db_cursor: cursor, supplier, column):
    allowed_columns = ['supplier', 'description', 'address']
    if column not in allowed_columns:
        return None
    query = f'''SELECT {column} FROM bills WHERE supplier = {supplier}'''
    return helper_functions.get_column_value(db_cursor, query)


def exist(db_cursor, supplier: str) -> bool:
    query = SELECT_ALL_QUERY
    cursor.execute(query, (supplier))
    row = cursor.fetchone()  # either a row or None

    if row is None:
        print("Not in the table.")
    else:
        print("Found:", row)

    return row is not None


def count_price(x: int, db_cursor: cursor, supplier) -> bool:
    if exist(db_cursor, supplier):
        count = get_column(db_cursor, supplier, 'price')
        if count is None:
            return False
        count += x
        query = f'''UPDATE suppliers SET price = {count} WHERE supplier = {supplier}'''
        db_cursor.execute(query)
        return True

    db_cursor.execute(create())
    db_cursor.execute(insert())
    return True