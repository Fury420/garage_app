from mindee_demo import Invoice
from psycopg2._psycopg import cursor, connection, Error, Warning
from typing import Tuple, Any


INSERT_QUERY = f'''
    INSERT INTO invoices 
    (date, vendor_name, invoice_number, total_amount_without_vat) 
    VALUES (%s, %s, %s, %s);'''
CREATE_TABLE_QUERY = f'''
    CREATE TABLE IF NOT EXISTS invoices (
    id INT PRIMARY KEY, 
    date DATE, 
    vendor_name VARCHAR(128), 
    invoice_number VARCHAR(64), 
    total_amount_without_vat REAL);'''
SELECT_BY_ID_QUERY = f'''
    SELECT * FROM invoices
    WHERE id = %s;'''
DELETE_BY_ID_QUERY = f'''
    DELETE FROM invoices
    WHERE id = %s;'''


def insert(connect: connection, db_cursor: cursor, invoice: Invoice) -> None:
    try:
        db_cursor.execute(
            query=INSERT_QUERY,
            vars=(None, invoice.date, invoice.vendor_name, invoice.invoice_number, invoice.total_amount_without_vat))
        connect.commit()
    except Warning as e:
        print(e.__class__.__name__)
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")


def create(connect: connection, db_cursor: cursor) -> None:
    try:
        db_cursor.execute(
            query=CREATE_TABLE_QUERY,
            vars=None)
        connect.commit()
    except Warning as e:
        print(e.__class__.__name__)
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")


def select(db_cursor: cursor, invoice_id: int) -> Tuple[Any, ...] | None:
    try:
        db_cursor.execute(
            query=SELECT_BY_ID_QUERY,
            vars=(invoice_id))
        return db_cursor.fetchone()
    except Warning as e:
        print(e.__class__.__name__)
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")


def delete(connect: connection, db_cursor: cursor, invoice_id: int) -> None:
    try:
        db_cursor.execute(
            query=DELETE_BY_ID_QUERY,
            vars=(invoice_id))
        connect.commit()
    except Warning as e:
        print(e.__class__.__name__)
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
