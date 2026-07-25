# Imports: Project
# ----------------
import database

POPULATIONS = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]


def populate_relative_frequency_table():
    with database.get_connection() as db_connection:
        cursor = db_connection.cursor()
        cursor.execute(f"SELECT sample, {", ".join(POPULATIONS)} FROM cell_count")
        rows = cursor.fetchall()

        calculated_relative_frequency_rows = []

        for row in rows:
            total_count = sum(row[1:])  # ignoring index 0 because that's the sample ID
            for pop in POPULATIONS:
                count = row[pop]
                percentage = (count / total_count) * 100
                calculated_relative_frequency_rows.append(
                    (
                        row["sample"],
                        total_count,
                        pop,
                        count,
                        percentage
                    )
                )

        cursor.executemany("""
                           INSERT INTO cell_relative_frequency(
                           sample, total_count, population, count, percentage)
                           VALUES(?, ?, ?, ?, ?)""",
                           calculated_relative_frequency_rows)
