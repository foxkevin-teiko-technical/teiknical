"""analysis.py

Module to perform required data analysis and transformation tasks

functions:
    - populate_relative_frequency_table
    - query_melanoma_miraclib_baseline

constants
    - POPULATIONS (tuple): tuple of strings with the names of cell populations e.g. "b_cell"
"""
# Imports: Project
# ----------------
import csv_helper
import database

# Imports: Standard Lib
# ---------------------
from collections import Counter

# Constants
# ---------
POPULATIONS = ("b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte")  # column names from cell_count


def populate_relative_frequency_table() -> None:
    """Updates the app.db cell_relative_frequency table with calculated values from the cell_count table

    For each sample in cell_count, calculates the total number of cells across all five populations. Then, computes the
    relative frequency of each population as a percentage of the total cell count for that sample. Each row represents
    one population from one sample.

    Then updates the cell_relative_frequency_table. See schema.create_cell_relative_frequency_table for column & table
    info.

    Returns:
        None
    """
    with database.get_connection() as db_connection:
        cursor = db_connection.cursor()

        # select subset of columns from all rows in cell count: we want the sample ID and the population counts
        # the join statement outputs the POPULATIONS strings with a comma in between each
        population_columns = ", ".join(POPULATIONS)  # "b_cell, cd8_t_cell, <...>"
        cursor.execute(f"SELECT sample, {population_columns} FROM cell_count")
        rows = cursor.fetchall()

        # what needs to be calculated from the problem statement:
        # - sample: the sample id as in column sample in cell-count.csv
        # - total_count: total cell count of sample
        # - population: name of the immune cell population (e.g. b_cell, cd8_t_cell, etc.)
        # - count: cell count
        # - percentage: relative frequency in percentage

        # initialize empty list that will be used to store the calculated values for batch db entry
        calculated_relative_frequency_rows = []

        # iterate through each row from the cell_count table (each row is one sample)
        for row in rows:
            # calculate total number of cells from each population column
            total_count = sum(row[1:])  # ignoring index 0 because that's the sample ID

            # now for each row (i.e. sample), we are going to generate len(POPULATIONS) [in this case: 5] new rows
            #  one row per population per sample - our cell_count csv has 10500 rows, so this will have 52,500 rows
            for population in POPULATIONS:
                # get the cell count of the currently focused population - using same terminology as the prob statement
                count = row[population]
                # problem statement did not specify if these should be saved as XY.Z% or 0.XYZ: saving it as XY.Z%
                #  for readability, but I would normally ask the requestor how they'd like it formatted
                percentage = (count / total_count) * 100

                calculated_relative_frequency_rows.append(
                    (
                        row["sample"],
                        total_count,
                        population,
                        count,
                        percentage
                    )
                )

        # update the cell_relative_frequency table with our newly calculated data
        cursor.executemany(
            """
            INSERT INTO cell_relative_frequency
            (
                sample, total_count, population, count, percentage
            )
            VALUES(?, ?, ?, ?, ?)
            """,
            calculated_relative_frequency_rows
        )

        # While it's in a db table already, for demonstration purposes, I will also output this as a csv
        csv_helper.export_tuple_list_to_csv(
            "output/part2_cell_relative_frequency.csv",
            ["sample", "total_count", "population", "count", "percentage"],
            calculated_relative_frequency_rows
        )


def query_melanoma_miraclib_baseline() -> None:
    """Query all melanoma PBMC samples at baseline from patients who have been treated with miraclib

    Also, within that subset, count how many samples were from each project,
    how many subjects were responders/non-responders, and
    how many subjects were males/females

    Since this is a query, it does not create a new database table, but instead exports to csv for this exercise

    Returns:
        None
    """
    with database.get_connection() as db_connection:
        cursor = db_connection.cursor()

        # For the SELECT (column) criteria, excluded condition treatment sample_type and time_from_treatment_start as
        #   we know these values since we're querying for them specifically. Included all other columns however as its
        #   meant to be an exploratory query
        cursor.execute(
            """
            SELECT
                project, subject, age, sex, response, sample, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte
            FROM cell_count
            WHERE condition = 'melanoma'
                AND treatment = 'miraclib'
                AND sample_type = 'PBMC'
                AND time_from_treatment_start = 0
            """
        )

        rows = cursor.fetchall()

        # save the initial query output to a csv
        csv_helper.export_sqlite_rows_to_csv("output/part4_melanoma_miraclib_baseline.csv", rows)

        # using Counter() to check frequencies of different projects, sexes, and responses
        counter_dict = {
            "project": Counter(),
            "sex": Counter(),
            "response": Counter()
        }

        for row in rows:
            # could do this:
            #   for counter_name, counter in counter_dict.items():
            #       counter[row[counter_name]] += 1
            # while it's cleaner than the below (I don't love the hardcoded strings), I believe it's more difficult to
            #   understand what's happening
            counter_dict["project"][row["project"]] += 1
            counter_dict["sex"][row["sex"]] += 1
            counter_dict["response"][row["response"]] += 1

        # create one csv file for each: project, sex, and response. Could do a single csv file as a summary as well
        for counter_name, counter in counter_dict.items():
            csv_helper.export_counter_to_csv(
                f"output/part4_{counter_name}.csv",
                [counter_name, "count"],
                counter
            )
