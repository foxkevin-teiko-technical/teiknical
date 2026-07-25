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
    ## create database
    database.create_table(schema.create_cell_count_table)
    ## initialize database with data
    csv_helper.populate_cell_count_csv()
    # part 2
    ## frequency of each cell type in each sample
    ## each row is one population from one sample
    database.create_table(schema.create_cell_relative_frequency_table)
    analysis.populate_relative_frequency_table()
    # part 3
    # part 4


if __name__ == "__main__":
    main()
