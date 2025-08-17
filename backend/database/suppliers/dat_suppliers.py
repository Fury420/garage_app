from backend.database import helper_functions
from psycopg2._psycopg import cursor, Error, Warning
from class_supplier import Supplier

INSERT_QUERY = '''INSERT INTO suppliers 
                (supplier, description, address, phone, price) VALUES (%s, %s, %s, %s, %s);'''

CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS bills (supplier VARCHAR, 
                                                    description VARCHAR, 
                                                    address VARCHAR
                                                    phone VARCHAR
                                                    price FLOAT), '''

DELETE_QUERY = '''DELETE FROM suppliers WHERE supplier = %s'''

SELECT_ALL_QUERY = '''SELECT * FROM bills WHERE supplier = %s'''

UPDATE_QUERY = f'''UPDATE suppliers SET price = %s WHERE supplier = %s'''

#inserts row into table suppliers
def insert(db_cursor: cursor, suppliers: Supplier) -> bool:
    try:
        query = INSERT_QUERY
        db_cursor.execute(query, (suppliers.supplier, suppliers.description, suppliers.address,
                                  suppliers.phone))
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
def delete(db_cursor:cursor, suppliers: Supplier) -> bool:
    try:
        query = DELETE_QUERY
        db_cursor.execute(query, (suppliers.supplier,))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#returns the whole row of table suppliers where the id matches
def select(db_cursor: cursor, suppliers: Supplier) -> Supplier | None:
    try:
        query = SELECT_ALL_QUERY
        db_cursor.execute(query, (suppliers.supplier,))
        row = db_cursor.fetchone()
    except Warning as e:
        print(e.__class__.__name__)
        return None
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return None

    suppliers.description, suppliers.address, suppliers.phone = row

    return suppliers


def count_price(x: int, db_cursor: cursor, suppliers:Supplier) -> bool:
    if exist(db_cursor, suppliers):
        count = get_column(db_cursor, suppliers, 'price')
        if count is None:
            return False
        count += x
        query = UPDATE_QUERY
        db_cursor.execute(query, (suppliers.amount , suppliers.supplier,))
        return True

    create(db_cursor)
    insert(db_cursor, suppliers)
    return True


#return a specific value from suppliers
def get_column(db_cursor: cursor, suppliers: Supplier, column: str) -> str | None:
    allowed_columns = ['supplier', 'description', 'address']
    if column not in allowed_columns:
        return None
    query = f'''SELECT {column} FROM bills WHERE supplier = {suppliers.supplier}'''
    return helper_functions.get_column_value(db_cursor, query)


def exist(db_cursor: cursor, suppliers: Supplier) -> bool:
    query = SELECT_ALL_QUERY
    db_cursor.execute(query, (suppliers.supplier,))
    row = db_cursor.fetchone()  # either a row or None

    if row is None:
        print("Not in the table.")
    else:
        print("Found:", row)

    return row is not None
