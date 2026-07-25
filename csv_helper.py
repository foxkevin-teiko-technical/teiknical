# Imports: Project
# ----------------
import database

# Imports: Standard Lib
# ---------------------
import csv


def populate_cell_count_csv(db_file = database.DEFAULT_DB, csv_data_file = "cell-count.csv"):
    with open(csv_data_file) as csv_file:
        csv_data = csv.reader(csv_file)
        next(csv_data)  # skip header row

        with database.get_connection(db_file) as db_connection:
            cursor = db_connection.cursor()
            cursor.executemany(f"""
                                   INSERT INTO cell_count(
                                   project, subject, condition, age, 
                                   sex, treatment, response, sample, 
                                   sample_type, time_from_treatment_start, 
                                   b_cell, cd8_t_cell, cd4_t_cell, 
                                   nk_cell, monocyte)
                                   VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                   csv_data)
