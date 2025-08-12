from backend import helper_functions


#inserts row into table suppliers
def insert():
    return '''INSERT INTO suppliers 
                (supplier, description, address) VALUES (%s, %s, %s);'''



#creates new table suppliers with columns: suppliers, description, address
def create():
    return '''CREATE TABLE IF NOT EXISTS bills (supplier VARCHAR, 
                                                description VARCHAR, 
                                                address VARCHAR), '''



#deletes from table suppliers
def delete(id):
    return f'''DELETE FROM suppliers WHERE supplier = {id}'''


#returns the whole row of table suppliers where the id matches
def select(id):
    return f'''SELECT * FROM bills WHERE supplier = {id}'''


#return a specific value from suppliers
def get_column(cursor, supplier, column):
    allowed_columns = ['supplier', 'description', 'address']
    if column not in allowed_columns:
        return None
    query = f'''SELECT {column} FROM bills WHERE supplier = {supplier}'''
    return helper_functions.get_column_value(cursor, query)

def exist(cursor, supplier) -> bool:
    query = f'''SELECT * FROM suppliers WHERE supplier = %s
    )'''
    cursor.execute(query, (supplier,))
    row = cursor.fetchone()  # either a row or None

    if row is None:
        print("Not in the table.")
    else:
        print("Found:", row)

    return row is not None


def count_price(x: int, cursor, supplier) -> bool:
    if exist(cursor, supplier):
        count = get_column(cursor, supplier, 'price')
        if count is None:
            return False
        count += x
        query = f'''UPDATE suppliers SET price = {count} WHERE supplier = {supplier}'''
        cursor.execute(query)
        return True

    cursor.execute(create())
    return True