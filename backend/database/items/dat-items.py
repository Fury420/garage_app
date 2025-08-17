from psycopg2._psycopg import cursor, Error, Warning
from backend.database.invoices.class_invoice import InvoiceItem
from backend.database.receipts.class_bill import BillItem

INSERT_QUERY = f'''INSERT INTO items (description, unit_price, quantity, status)
                VALUES (%s, %s, %s, %s);'''

CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS items (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                                                    description VARCHAR(255), 
                                                    unit_price FLOAT,
                                                    quantity INTEGER
                                                    status VARCHAR(10));'''

DELETE_QUERY = f'''DELETE FROM items WHERE id = %s;'''

SELECT_QUERY = f'''SELECT * FROM items WHERE id = %s'''


#inserts row into the table items
def insert(db_cursor: cursor, items: InvoiceItem | BillItem) -> bool:
    try:
        query = INSERT_QUERY
        db_cursor.execute(query, (items.description, items.unit_price, items.quantity, ))
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


#deletes from table items
def delete(db_cursor: cursor, item: InvoiceItem | BillItem) -> bool:
    try:
        query = DELETE_QUERY
        db_cursor.execute(query, (item.id, ))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#return the whole row of table an item where the id matches
def select(db_cursor: cursor, items: InvoiceItem | BillItem) -> None:
    try:
        query = SELECT_QUERY
        db_cursor.execute(query, (items.id,))
        row = db_cursor.fetchone()
    except Warning as e:
        print(e.__class__.__name__)
        return None
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return None


    '''
    if not :
        return None
    '''
    return None