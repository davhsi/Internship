import sqlite3

_connection = None

def connect(db_path):
    global _connection
    _connection = sqlite3.connect(db_path)
    return _connection

def get_connection():
    global _connection
    if _connection is None:
        raise RuntimeError("No database connection! Call connect() first.")
    return _connection

def close():
    global _connection
    if _connection:
        _connection.close()
        _connection = None