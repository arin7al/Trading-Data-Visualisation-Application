import mysql.connector

_connection = None
config = {
    'user': 'root',
    'password': 'helloworld',
    'host': 'localhost',
    'port': 3308,
    'database': 'trading_data',
    'raise_on_warnings': True
}


def get_connection():
    global _connection
    if not _connection:
        _connection = mysql.connector.connect(**config)
    return _connection

def is_connection_open():
    global _connection
    if _connection is not None:
        return True
    else:
        return False

def close_connection():
    global _connection
    if _connection is not None:
        _connection.close()

def get_all_deals():
    SQL_STATEMENT = ("SELECT * FROM deal")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(SQL_STATEMENT)
    return cursor.fetchall()


