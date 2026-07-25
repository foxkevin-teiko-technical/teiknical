"""csv_helper.py

Module for interfacing with the provided CSV file

functions:
    - populate_cell_count_csv
"""
# Imports: Project
# ----------------
import database

# Imports: Standard Lib
# ---------------------
import csv


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
