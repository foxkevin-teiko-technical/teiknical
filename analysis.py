"""analysis.py

Module to perform required data analysis and transformation tasks

functions:
    - populate_relative_frequency_table

constants
    - POPULATIONS (tuple): tuple of strings with the names of cell populations e.g. "b_cell"
"""
# Imports: Project
# ----------------
import database

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
