from database.database import get_db_connection, get_cursor


def get_owner_by_id(owner_id, connection = None):
    if connection is None:
        con = get_db_connection()
    else:
        con = connection
    cur = get_cursor(con)
    cur.execute('SELECT * FROM Owners WHERE id = %s', (owner_id,))
    owner = cur.fetchone()
    if connection is None:
        con.close()
    return owner


def get_animal_by_id(animal_id, connection = None):
    if connection is None:
        con = get_db_connection()
    else:
        con = connection
    cur = get_cursor(con)
    cur.execute('SELECT * FROM Animals WHERE id = %s', (animal_id,))
    animal = cur.fetchone()
    if connection is None:
        con.close()
    return animal


def get_animal_count(connection = None):
    if connection is None:
        con = get_db_connection()
    else:
        con = connection
    cur = get_cursor(con)
    cur.execute('SELECT COUNT(*) AS count FROM Animals')
    animal_count = cur.fetchone()["count"]
    if connection is None:
        con.close()
    return animal_count


def get_owner_count(connection = None):
    if connection is None:
        con = get_db_connection()
    else:
        con = connection
    cur = get_cursor(con)
    cur.execute('SELECT COUNT(*) AS count FROM Owners')
    owner_count = cur.fetchone()["count"]
    if connection is None:
        con.close()
    return owner_count