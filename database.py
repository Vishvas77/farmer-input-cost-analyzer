# database.py
# All SQLite database operations for the Farmer Input Cost Analyzer.
# Every SQL query is parameterized (uses ? placeholders) so user input
# can never break the query or inject SQL.

import sqlite3

DB_NAME = "farmer_costs.db"


def get_connection():
    """Open a connection to the SQLite database file."""
    return sqlite3.connect(DB_NAME)


def create_table():
    """Create the farm_expenses table if it does not already exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farm_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farm_id TEXT NOT NULL UNIQUE,
            crop TEXT NOT NULL,
            seed_cost REAL NOT NULL,
            fertilizer_cost REAL NOT NULL,
            labour_cost REAL NOT NULL,
            irrigation_cost REAL NOT NULL,
            created_at TEXT DEFAULT (datetime('now', 'localtime'))
        )
    """)
    conn.commit()
    conn.close()


def add_expense(farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost):
    """Insert one farm expense record. Returns True on success."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO farm_expenses
            (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost))
    conn.commit()
    conn.close()
    return True


def get_all_expenses():
    """Return every expense record, oldest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farm_expenses ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expense_by_farm(farm_id):
    """Return the single record for a farm_id, or None if not found."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farm_expenses WHERE farm_id = ?", (farm_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def search_expenses(keyword):
    """Search records by farm_id or crop (partial match allowed)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM farm_expenses
        WHERE farm_id LIKE ? OR crop LIKE ?
        ORDER BY id
    """, ("%" + keyword + "%", "%" + keyword + "%"))
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_expense(farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost):
    """Update the record for a farm_id. Returns number of rows changed."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE farm_expenses
        SET crop = ?, seed_cost = ?, fertilizer_cost = ?,
            labour_cost = ?, irrigation_cost = ?
        WHERE farm_id = ?
    """, (crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost, farm_id))
    changed = cursor.rowcount
    conn.commit()
    conn.close()
    return changed


def delete_expense(farm_id):
    """Delete the record for a farm_id. Returns number of rows deleted."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM farm_expenses WHERE farm_id = ?", (farm_id,))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted


def farm_exists(farm_id):
    """Check whether a farm_id is already present in the table."""
    return get_expense_by_farm(farm_id) is not None


def count_records():
    """Return how many expense records exist (used for empty-database checks)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM farm_expenses")
    count = cursor.fetchone()[0]
    conn.close()
    return count
