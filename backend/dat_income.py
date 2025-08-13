import helper_functions
from class_income import Income
from psycopg2._psycopg import cursor, connection, Error, Warning

INSERT_QUERY = f'''INSERT INTO income (amount, date)
                VALUES (%s, %s);'''

CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS income (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                                                    amount FLOAT, 
                                                    date DATE)'''

DELETE_QUERY = f'''DELETE FROM income WHERE id = %s;'''

SELECT_QUERY = f'''SELECT * FROM income WHERE id = %s'''


#inserts row into the table income
def insert(db_cursor: cursor, income: Income) -> bool:
    try:
        query = INSERT_QUERY
        db_cursor.execute(query, (income.amount, income.date))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#creates new table income with columns: id, amount, date
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


#deletes a row from table income
def delete(db_cursor: cursor, income: Income) -> bool:
    try:
        query = DELETE_QUERY
        db_cursor.execute(query, (income.id,))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#return the whole row of table income where the id matches and stores it to the class Income
def select(db_cursor: cursor, income: Income) -> Income | None:
    try:
        query = SELECT_QUERY
        db_cursor.execute(query, (income.id,))
        row = db_cursor.fetchone()
    except Warning as e:
        print(e.__class__.__name__)
        return None
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return None

    income.amount = row[0]
    income.date = row[1]

    if not helper_functions.income_check(income):
        return None
    return income

