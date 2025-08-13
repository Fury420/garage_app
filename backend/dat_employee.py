import helper_functions
from psycopg2._psycopg import cursor, connection, Error, Warning
from employee import Employee
from psycopg2 import sql

INSERT_QUERY = f'''INSERT INTO employee (name, surname, salary, status)
                VALUES (%s, %s, %s, %s);'''

CREATE_QUERY = '''CREATE TABLE IF NOT EXISTS bills (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                                                    name VARCHAR(20), 
                                                    surname VARCHAR(30), 
                                                    salary FLOAT, 
                                                    status INT)'''

DELETE_QUERY = f'''DELETE FROM bills WHERE id = %s;'''

SELECT_QUERY = f'''SELECT * FROM employee WHERE id = %s'''


#inserts row into the table employee
def insert(db_cursor: cursor, employee: Employee) -> bool:
    try:
        query = INSERT_QUERY
        db_cursor.execute(query, (employee.name,employee.surname, employee.salary, employee.status))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#creates new table employee with columns: id, name, surname, salary, status
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
def delete(db_cursor: cursor) -> bool:
    try:
        query = DELETE_QUERY
        db_cursor.execute(query)
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True


#return the whole row of table employee where the id matches
def select(db_cursor: cursor, employee: Employee) -> Employee | None:
    try:
        query = SELECT_QUERY
        db_cursor.execute(query, (employee.id,))
        row = db_cursor.fetchone()
    except Warning as e:
        print(e.__class__.__name__)
        return None
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return None

    employee.name = row[0]
    employee.surname = row[1]
    employee.salary = row[2]
    employee.status = row[3]

    if not helper_functions.employee_check(employee):
        return None
    return employee


#updates the row employee
def update(db_cursor: cursor, employee: Employee, value:int, column:str) -> bool:

    allowed_columns = ['name','surname','salary','status']
    if column not in allowed_columns:
        return False
    try:
        query = sql.SQL("UPDATE employee SET {col} = %s WHERE id = %s").format(
                col=sql.Identifier(column))
        db_cursor.execute(query, (value, employee.id))
    except Warning as e:
        print(e.__class__.__name__)
        return False
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return False
    return True
