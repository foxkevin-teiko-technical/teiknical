import sqlite3

DEFAULT_DB = "app.db"


def get_connection(db_file = DEFAULT_DB):
    db_connection = sqlite3.connect(db_file)
    db_connection.execute("PRAGMA foreign_keys = ON")
    return db_connection


def create_table(schema_function, db_file = DEFAULT_DB):
    """

    Args:
        schema_function (function):
        db_file (str):

    Returns:

    """
    with get_connection(db_file) as db_connection:
        cursor = db_connection.cursor()
        schema_function(cursor)

# DEV ONLY
def reset_db():
    with get_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS cell_relative_frequency")
        cursor.execute("DROP TABLE IF EXISTS cell_count")
