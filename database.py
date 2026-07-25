"""database.py

Module with database utilities

functions
    - get_connection
    - create_table
    - reset_db

constants
    - DEFAULT_DB (str): path to the default database file - "app.db"
"""
# Imports: Standard Lib
# ---------------------
from collections.abc import Callable
import sqlite3

# Constants
# ---------
DEFAULT_DB = "app.db"


def create_table(schema_function: Callable[[sqlite3.Cursor], None]) -> None:
    """Create a table in database db_file given a function which defines the table creation

    Opens a connection to the database, and invokes the schema_function while passing it the db cursor. While
    schema_function type is indeed <class: 'function'>, using Callable[[sqlite3.Cursor], None] (also accurate) in the
    type hint for IDE clarity since all schema.py functions take a sqlite3.Cursor input and return None.

    While this would work with other callables, for the exam purposes, I will only be using schema.py functions.

    Args:
        schema_function (function): a function from schema.py which contains definitions and logic for creating a table

    Returns:
        None
    """
    with get_connection() as db_connection:
        cursor = db_connection.cursor()
        schema_function(cursor)


def get_connection(db_file: str = DEFAULT_DB) -> sqlite3.Connection:
    """Return a sqlite3 connection to the give database at db_file location (default app.db)

    Recommend using as a context manager:
        >>> with get_connection() as connection:
        >>>     # interact with database

    Args:
        db_file (str): path to the database file, "app.db" by default

    Returns:
        sqlite3.Connection
    """
    db_connection = sqlite3.connect(db_file)
    db_connection.row_factory = sqlite3.Row
    db_connection.execute("PRAGMA foreign_keys = ON")
    return db_connection


# DEV ONLY
def reset_db():
    with get_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS cell_relative_frequency")
        cursor.execute("DROP TABLE IF EXISTS cell_count")
