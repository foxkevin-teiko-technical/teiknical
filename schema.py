# Imports: Standard Lib
# ---------------------
import sqlite3


def create_cell_count_table(cursor: sqlite3.Cursor) -> None:
    """Definition for the cell count table to be used by the database logic. Column definitions are the same as found in
    cell-count.csv - sample is the Primary key

    Args:
        cursor (sqlite3.Cursor): SQLite3 cursor object used to CREATE TABLE

    Returns:
        None
    """
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cell_count (
            project TEXT,
            subject TEXT,
            condition TEXT,
            age INTEGER,
            sex TEXT,
            treatment TEXT,
            response TEXT,
            sample TEXT PRIMARY KEY,
            sample_type TEXT,
            time_from_treatment_start INTEGER,
            b_cell INTEGER,
            cd8_t_cell INTEGER,
            cd4_t_cell INTEGER,
            nk_cell INTEGER,
            monocyte INTEGER
        )
        """
    )


def create_cell_relative_frequency_table(cursor: sqlite3.Cursor) -> None:
    """Definition for the cell relative frequency table to be used by the database logic. Column definitions are defined
    in the part 2 of the technical exam:

    - sample: the sample id as in column sample in cell-count.csv
    - total_count: total cell count of sample
    - population: name of the immune cell population (e.g. b_cell, cd8_t_cell, etc.)
    - count: cell count
    - percentage: relative frequency in percentage

    Args:
        cursor (sqlite3.Cursor): SQLite3 cursor object used to CREATE TABLE

    Returns:
        None
    """
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cell_relative_frequency (
            sample TEXT,
            total_count INTEGER,
            population TEXT,
            count INTEGER,
            percentage REAL,
            FOREIGN KEY(sample) REFERENCES cell_count(sample)
        )
        """
    )
