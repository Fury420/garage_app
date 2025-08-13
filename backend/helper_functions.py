from psycopg2._psycopg import cursor, connection, Error, Warning

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