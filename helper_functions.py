import bills

def get_column_value(cursor, query):
    if not query:
        return None

    cursor.execute(query)
    row = cursor.fetchone()
    return row[0] if row else None