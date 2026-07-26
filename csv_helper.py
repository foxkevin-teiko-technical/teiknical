"""csv_helper.py

Module for interfacing with the provided CSV file

functions:
    - export_counter_to_csv
    - export_tuple_list_to_csv
    - export_sqlite_rows_to_csv
    - populate_cell_count_csv
"""
# Imports: Project
# ----------------
import database

# Imports: Standard Lib
# ---------------------
from collections import Counter
import csv
import sqlite3


# Certainly could have combined and/or abstracted the following three helper functions more, since they all do very
#   similar actions. export_counter and export_tuple_list especially
def export_counter_to_csv(csv_output_file: str, header_row: list[str], counter: Counter) -> None:
    """Export a collections.Counter to a csv file

    Args:
        csv_output_file (str): path to the output csv file
        header_row (list[str]): list of strings with the header row values
        counter (Counter): a collections.Counter object with iterable row information

    Returns:
        None
    """
    with open(csv_output_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header_row)

        for key, count in counter.items():
            writer.writerow([key, count])


def export_tuple_list_to_csv(csv_output_file: str, header_row: list[str], list_data: list[tuple]) -> None:
    """Export a list of tuples to a csv file

    Args:
        csv_output_file (str): path to the output csv file
        header_row (list[str]): list of strings with the header row values
        list_data (list[tuple]): list of tuples with the row information

    Returns:
        None
    """
    with open(csv_output_file, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header_row)

        writer.writerows(list_data)


def export_sqlite_rows_to_csv(csv_output_file: str, sqlite_rows: list[sqlite3.Row]) -> None:
    """Export a list of sqlite3 rows returned from cursor.fetchall() to a csv file

    Args:
        csv_output_file (str): path to the output csv file
        sqlite_rows (list[sqlite3.Row]): list of sqlite3.Row objects

    Returns:
        None
    """
    with open(csv_output_file, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=sqlite_rows[0].keys())
        writer.writeheader()

        for row in sqlite_rows:
            writer.writerow(dict(row))


def populate_cell_count_csv(csv_data_file: str = "cell-count.csv") -> None:
    """Opens the csv (default: cell-count.csv) and inserts its contents in the app.db cell_count table

    cell_count table columns mirror the cell-count csv columns.

    Args:
        csv_data_file (str): path to the csv file - optional, defaults to cell-count.csv

    Returns:
        None
    """
    # Open the csv file and create a reader object to interface with the file contents
    with (open(csv_data_file) as csv_file):
        csv_data = csv.reader(csv_file)
        next(csv_data)  # skip header row

        # while we keep the csv reader object open, we connect to the database to update it with the csv contents
        with database.get_connection() as db_connection:
            cursor = db_connection.cursor()
            cursor.executemany(
                """
                INSERT INTO cell_count
                (
                    project, subject, condition, age, 
                    sex, treatment, response, sample, 
                    sample_type, time_from_treatment_start, 
                    b_cell, cd8_t_cell, cd4_t_cell, 
                    nk_cell, monocyte
                )
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                """,
                csv_data
            )
            # for VALUES, could have condensed the 15 ?s using something like {"?, " * 15} or a join statement, but
            # it was confusing the IDE because it was expecting 15 inputs, so I kept it expanded
