"""load_data.py

Main module for the technical exam
"""
# Imports: Project
# ----------------
import analysis
import csv_helper
import database
import schema


def main():
    # part 0
    database.reset_db()

    # part 1
    database.create_table(schema.create_cell_count_table)
    csv_helper.populate_cell_count_csv()

    # part 2
    database.create_table(schema.create_cell_relative_frequency_table)
    analysis.populate_relative_frequency_table()

    # part 3
    # TODO

    # part 4
    analysis.query_melanoma_miraclib_baseline()


if __name__ == "__main__":
    main()
