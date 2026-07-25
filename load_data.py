import database
import csv_helper
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
    ## sample, total_count (sum of all cells), population, count, relative frequency (%)
    ## each row is one population from one sample
    database.create_table(schema.create_cell_relative_frequency_table)
    # part 3
    # part 4
    pass

if __name__ == "__main__":
    main()
