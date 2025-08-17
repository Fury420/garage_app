from psycopg2._psycopg import cursor, Error, Warning
from backend.database.employee.class_employee import Employee
from backend.database.income.class_income import Income

def get_column_value(db_cursor: cursor, query, column: str, id: int) \
                                            -> int | float | str | None:
    if not query:
        return None
    try:
        db_cursor.execute(query, (column, id))
        row = db_cursor.fetchone()
    except Warning as e:
        print(e.__class__.__name__)
        return None
    except Error as e:
        print(f"{e.__class__.__name__} : {e.pgerror}")
        return None
    return row[0] if row else None


def employee_check(employee: Employee) -> bool:
    if employee.name is None:
        return False
    if employee.surname is None:
        return False
    if employee.salary is None:
        return False
    if employee.status is None:
        return False
    return True


def income_check(income: Income) -> bool:
    if income.amount is None:
        return False
    if income.date is None:
        return False
    return True