# load_sample_data.py
# Loads sample_data.sql into farmer_costs.db.
# Run with:  python load_sample_data.py
# Safe to run multiple times: existing farm IDs are skipped
# (farm_id is UNIQUE in the table).

import sqlite3
import database


def main():
    database.create_table()
    with open("sample_data.sql", "r", encoding="utf-8") as f:
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
    print(f"Sample data load complete: {loaded} inserted, {skipped} already present.")


if __name__ == "__main__":
    main()
