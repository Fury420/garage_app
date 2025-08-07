#inserts row into the table bills
import helper_functions


def insert():
    return '''INSERT INTO bills (id, supplier, price, date)
                VALUES (1, 'Book', 19.99, '12.3.2004');'''


#creates new table bills with columns: id, supplier, price, date
def create():
    return '''CREATE TABLE IF NOT EXISTS bills (id INT PRIMARY KEY, 
                                                supplier VARCHAR(40), 
                                                price REAL, 
                                                date VARCHAR(40))'''


#deletes from table bills
def delete(id):
    return f'''DELETE FROM bills WHERE id = {id}'''


#return the whole row of table bills where the id matches
def select(id):
    return f'''SELECT * FROM bills WHERE id = {id}'''


#return a specific value from table bills
def get_column(cursor, id, column):
    allowed_columns = ['supplier', 'price', 'id', 'date']
    if column not in allowed_columns:
        return None
    query = f'''SELECT {column} FROM bills WHERE id = {id}'''
    return helper_functions.get_column_value(cursor, query)
