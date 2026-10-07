# analysis.py
# All cost calculations and comparisons.
# Cost-category thresholds used here:
#     Total < 25,000              -> Low
#     Total 25,000 to 40,000      -> Medium
#     Total > 40,000              -> High
# These limits are stored as constants below so they are easy to
# find, explain and change. The sample record (total 45,000) is "High".

import database

LOW_LIMIT = 25000
HIGH_LIMIT = 40000

CATEGORIES = ["Seed", "Fertilizer", "Labour", "Irrigation"]

# Rule-based cost-control advice, one per possible highest-cost category.
SUGGESTIONS = {
    "Seed": "Seed cost is the major cost component. Compare seed suppliers and varieties.",
    "Fertilizer": "Fertilizer is the major cost component. Review fertilizer quantity and application planning.",
    "Labour": "Labour is the major cost component. Consider optimizing labour usage and scheduling.",
    "Irrigation": "Irrigation is the major cost component. Consider improving irrigation efficiency.",
}


def calculate_total(seed, fertilizer, labour, irrigation):
    """Total input cost = seed + fertilizer + labour + irrigation."""
    return seed + fertilizer + labour + irrigation


def get_highest_cost_category(seed, fertilizer, labour, irrigation):
    """Return the name of the cost category with the largest amount.

    If two categories tie, the first one in CATEGORIES order wins."""
    costs = {
        "Seed": seed,
        "Fertilizer": fertilizer,
        "Labour": labour,
        "Irrigation": irrigation,
    }
    return max(costs, key=costs.get)


def classify_cost(total):
    """Classify a total input cost as Low, Medium or High."""
    if total < LOW_LIMIT:
        return "Low"
    if total <= HIGH_LIMIT:
        return "Medium"
    return "High"


def get_suggestion(highest_category):
    """Return the cost-control suggestion for the highest-cost category."""
    return SUGGESTIONS.get(highest_category, "No suggestion available.")


def get_data_source(farm_id):
    """Return the data-source label for a farm record.

    Farm IDs starting with 'TN-' are Government Reference Data (Tamil Nadu
    state-average figures); everything else is assignment/sample data.
    """
    if farm_id.startswith("TN-"):
        return "Government Reference Data \u2014 Tamil Nadu"
    return "Sample Data"


def record_to_summary(row):
    """Convert one database row into a dict with calculated fields.

    Row layout: (id, farm_id, crop, seed, fertilizer, labour, irrigation, created_at)
    """
    seed, fertilizer, labour, irrigation = row[3], row[4], row[5], row[6]
    total = calculate_total(seed, fertilizer, labour, irrigation)
    highest = get_highest_cost_category(seed, fertilizer, labour, irrigation)
    return {
        "farm_id": row[1],
        "crop": row[2],
        "seed": seed,
        "fertilizer": fertilizer,
        "labour": labour,
        "irrigation": irrigation,
        "total": total,
        "highest": highest,
        "category": classify_cost(total),
    }


def farm_cost_summary():
    """Total input cost of every farm, highest first (calculated in SQL)."""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT farm_id, crop,
               seed_cost + fertilizer_cost + labour_cost + irrigation_cost AS total
        FROM farm_expenses
        ORDER BY total DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows  # list of (farm_id, crop, total)


def crop_comparison():
    """Per-crop record count, total cost and average cost (SQL GROUP BY)."""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT crop,
               COUNT(*) AS farms,
               SUM(seed_cost + fertilizer_cost + labour_cost + irrigation_cost) AS total,
               AVG(seed_cost + fertilizer_cost + labour_cost + irrigation_cost) AS average
        FROM farm_expenses
        GROUP BY crop
        ORDER BY total DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows  # list of (crop, farms, total, average)


def overall_category_totals():
    """Total spend on each cost category across ALL records (SQL SUM)."""
    conn = database.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT SUM(seed_cost), SUM(fertilizer_cost),
               SUM(labour_cost), SUM(irrigation_cost)
        FROM farm_expenses
    """)
    row = cursor.fetchone()
    conn.close()
    totals = {
        "Seed": row[0] or 0,
        "Fertilizer": row[1] or 0,
        "Labour": row[2] or 0,
        "Irrigation": row[3] or 0,
    }
    return totals
