# load_real_data.py
# Loads real, open-source Tamil Nadu cost-of-cultivation data
# (real_data_tn.sql) into farmer_costs.db.
# Run with:  python load_real_data.py
# Safe to run multiple times: existing farm IDs are skipped
# (farm_id is UNIQUE in the table).
#
# NOTE: this adds 8 records ALONGSIDE any existing records.
# The default sample data (F01-F07) is left untouched.

import sqlite3
import database


def main():
    database.create_table()
    with open("real_data_tn.sql", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Remove comment lines and blank lines, then join into one script.
    statements = "".join(
        line for line in lines
        if line.strip() and not line.strip().startswith("--")
    )

    conn = database.get_connection()
    cursor = conn.cursor()
    loaded = 0
    skipped = 0
    # INSERT OR IGNORE skips rows whose farm_id already exists.
    for statement in statements.split(";"):
        clean = statement.strip()
        if not clean:
            continue
        try:
            cursor.execute(clean.replace("INSERT INTO", "INSERT OR IGNORE INTO", 1))
            if cursor.rowcount > 0:
                loaded += 1
            else:
                skipped += 1
        except sqlite3.Error as e:
            print(f"Skipped a statement ({e})")
    conn.commit()
    conn.close()
    print(f"Real-data load complete: {loaded} inserted, {skipped} already present.")
    print("Source: TN Directorate of Economics and Statistics, Table XI.1")


if __name__ == "__main__":
    main()
