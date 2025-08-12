#inserts row into the table employee
def insert():
    return f'''INSERT INTO employee (name, surname, salary, status)
                VALUES (%s, %s, %s, %s);'''


#creates new table employee with columns: id, name, surname, salary, status
def create():
    return '''CREATE TABLE IF NOT EXISTS bills (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, 
                                                name VARCHAR(20), 
                                                surname VARCHAR(30), 
                                                salary FLOAT, 
                                                status INT)'''


#deletes from table employee
def delete(id):
    return f'''DELETE FROM employee WHERE id = {id}'''


#return the whole row of table employee where the id matches
def select(id):
    return f'''SELECT * FROM employee WHERE id = {id}'''