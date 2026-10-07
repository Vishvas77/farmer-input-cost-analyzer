# main.py
# Menu-driven command-line interface for the Farmer Input Cost Analyzer.
# Run with:  python main.py

import database
import analysis
import reports
import validation


def print_header():
    print()
    print("=" * 50)
    print("       FARMER INPUT COST ANALYZER")
    print("=" * 50)


def print_menu():
    print()
    print("1.  Add farm expense record")
    print("2.  View all records")
    print("3.  Search records")
    print("4.  Update a record")
    print("5.  Delete a record")
    print("6.  Calculate total input cost")
    print("7.  View cost breakdown")
    print("8.  Compare farms")
    print("9.  Compare crops")
    print("10. Identify highest-cost category")
    print("11. Generate cost report")
    print("12. Show cost-control suggestions")
    print("13. Exit")


def has_records():
    """True when the database contains at least one record."""
    if database.count_records() == 0:
        print("\nNo records found. Please add a record first (option 1).")
        return False
    return True


def read_costs():
    """Read the four cost amounts from the user with validation."""
    seed = validation.get_positive_amount("Seed cost (Rs): ")
    fertilizer = validation.get_positive_amount("Fertilizer cost (Rs): ")
    labour = validation.get_positive_amount("Labour cost (Rs): ")
    irrigation = validation.get_positive_amount("Irrigation cost (Rs): ")
    return seed, fertilizer, labour, irrigation


def show_record(row):
    """Print one database row in a readable one-line format."""
    summary = analysis.record_to_summary(row)
    source = analysis.get_data_source(summary["farm_id"])
    print(f"Farm: {summary['farm_id']} | Crop: {summary['crop']} | "
          f"Seed: {reports.format_rupees(summary['seed'])} | "
          f"Fertilizer: {reports.format_rupees(summary['fertilizer'])} | "
          f"Labour: {reports.format_rupees(summary['labour'])} | "
          f"Irrigation: {reports.format_rupees(summary['irrigation'])} | "
          f"Total: {reports.format_rupees(summary['total'])} [{source}]")


def add_record():
    print("\n--- Add Farm Expense Record ---")
    farm_id = validation.get_non_empty_input("Farm ID (e.g. F07): ")
    if database.farm_exists(farm_id):
        print(f"Farm ID '{farm_id}' already exists. Use option 4 to update it.")
        return
    crop = validation.get_non_empty_input("Crop (e.g. Cotton): ")
    seed, fertilizer, labour, irrigation = read_costs()
    database.add_expense(farm_id, crop, seed, fertilizer, labour, irrigation)
    total = analysis.calculate_total(seed, fertilizer, labour, irrigation)
    print(f"\nRecord added. Total input cost: {reports.format_rupees(total)}")


def view_records():
    print("\n--- All Farm Expense Records ---")
    rows = database.get_all_expenses()
    if not rows:
        print("No records found.")
        return
    for row in rows:
        show_record(row)
    print(f"\nTotal records: {len(rows)}")
    print("[Sample Data] = assignment/sample records | "
          "[Government Reference Data \u2014 Tamil Nadu] = TN DES Table XI.1 state averages")


def search_records():
    if not has_records():
        return
    print("\n--- Search Records ---")
    keyword = validation.get_non_empty_input("Enter farm ID or crop to search: ")
    rows = database.search_expenses(keyword)
    if not rows:
        print(f"No records found matching '{keyword}'.")
        return
    for row in rows:
        show_record(row)


def update_record():
    if not has_records():
        return
    print("\n--- Update Record ---")
    farm_id = validation.get_non_empty_input("Enter farm ID to update: ")
    row = database.get_expense_by_farm(farm_id)
    if row is None:
        print(f"No record found for farm ID '{farm_id}'.")
        return
    print("Current record:")
    show_record(row)
    crop = validation.get_non_empty_input("New crop: ")
    seed, fertilizer, labour, irrigation = read_costs()
    database.update_expense(farm_id, crop, seed, fertilizer, labour, irrigation)
    print("Record updated successfully.")


def delete_record():
    if not has_records():
        return
    print("\n--- Delete Record ---")
    farm_id = validation.get_non_empty_input("Enter farm ID to delete: ")
    row = database.get_expense_by_farm(farm_id)
    if row is None:
        print(f"No record found for farm ID '{farm_id}'.")
        return
    show_record(row)
    confirm = input("Delete this record? (y/n): ").strip().lower()
    if confirm == "y":
        database.delete_expense(farm_id)
        print("Record deleted.")
    else:
        print("Delete cancelled.")


def calculate_total_cost():
    if not has_records():
        return
    print("\n--- Calculate Total Input Cost ---")
    farm_id = validation.get_non_empty_input("Enter farm ID: ")
    row = database.get_expense_by_farm(farm_id)
    if row is None:
        print(f"No record found for farm ID '{farm_id}'.")
        return
    summary = analysis.record_to_summary(row)
    print(f"\nFarm: {summary['farm_id']} | Crop: {summary['crop']}")
    print(f"Seed ({reports.format_rupees(summary['seed'])}) + "
          f"Fertilizer ({reports.format_rupees(summary['fertilizer'])}) + "
          f"Labour ({reports.format_rupees(summary['labour'])}) + "
          f"Irrigation ({reports.format_rupees(summary['irrigation'])})")
    print(f"Total Input Cost: {reports.format_rupees(summary['total'])}")


def cost_breakdown():
    if not has_records():
        return
    print("\n--- Cost Breakdown ---")
    farm_id = validation.get_non_empty_input("Enter farm ID: ")
    row = database.get_expense_by_farm(farm_id)
    if row is None:
        print(f"No record found for farm ID '{farm_id}'.")
        return
    summary = analysis.record_to_summary(row)
    total = summary["total"]
    print(f"\nFarm: {summary['farm_id']} | Crop: {summary['crop']}")
    for name in ["seed", "fertilizer", "labour", "irrigation"]:
        amount = summary[name]
        share = (amount / total * 100) if total > 0 else 0
        print(f"{name.capitalize():<12}: {reports.format_rupees(amount):>10}  ({share:.1f}%)")
    print(f"\nTotal: {reports.format_rupees(total)}")
    print(f"Highest cost: {summary['highest']}")


def compare_farms():
    if not has_records():
        return
    print("\n--- Farm Comparison (by total input cost) ---")
    rows = analysis.farm_cost_summary()
    print(f"\n{'Farm':<13}{'Crop':<12}{'Total Cost':>12}")
    print("-" * 37)
    for farm_id, crop, total in rows:
        print(f"{farm_id:<13}{crop:<12}{reports.format_rupees(total):>12}")
    highest = rows[0]
    print(f"\nHighest-cost farm: {highest[0]} ({highest[1]}) "
          f"at {reports.format_rupees(highest[2])}")


def compare_crops():
    if not has_records():
        return
    print("\n--- Crop Comparison ---")
    rows = analysis.crop_comparison()
    print(f"\n{'Crop':<12}{'Farms':>7}{'Total Cost':>13}{'Avg Cost':>13}")
    print("-" * 47)
    for crop, farms, total, average in rows:
        print(f"{crop:<12}{farms:>7}{reports.format_rupees(total):>13}"
              f"{reports.format_rupees(average):>13}")
    highest = rows[0]
    print(f"\nHighest-cost crop: {highest[0]} "
          f"at {reports.format_rupees(highest[2])} total")


def highest_cost_category():
    if not has_records():
        return
    print("\n--- Highest-Cost Category (all farms combined) ---")
    totals = analysis.overall_category_totals()
    for name in analysis.CATEGORIES:
        print(f"{name:<12}: {reports.format_rupees(totals[name])}")
    highest = max(totals, key=totals.get)
    print(f"\nHighest-cost category overall: {highest} "
          f"({reports.format_rupees(totals[highest])})")
    print(f"Suggestion: {analysis.get_suggestion(highest)}")


def generate_report():
    if not has_records():
        return
    print("\n--- Generate Cost Report ---")
    farm_id = validation.get_non_empty_input("Enter farm ID: ")
    row = database.get_expense_by_farm(farm_id)
    if row is None:
        print(f"No record found for farm ID '{farm_id}'.")
        return
    summary = analysis.record_to_summary(row)
    reports.print_report(summary)
    save = input("Save this report to a text file? (y/n): ").strip().lower()
    if save == "y":
        filename = f"report_{summary['farm_id']}.txt"
        reports.save_report(summary, filename)
        print(f"Report saved to {filename}")


def show_suggestions():
    if not has_records():
        return
    print("\n--- Cost-Control Suggestions ---")
    farm_id = validation.get_non_empty_input("Enter farm ID: ")
    row = database.get_expense_by_farm(farm_id)
    if row is None:
        print(f"No record found for farm ID '{farm_id}'.")
        return
    summary = analysis.record_to_summary(row)
    print(f"\nFarm: {summary['farm_id']} | Crop: {summary['crop']}")
    print(f"Highest cost category: {summary['highest']}")
    print(f"Suggestion: {analysis.get_suggestion(summary['highest'])}")


def main():
    database.create_table()
    print_header()
    while True:
        print_menu()
        choice = validation.get_menu_choice("\nEnter your choice: ", 1, 13)
        if choice == 1:
            add_record()
        elif choice == 2:
            view_records()
        elif choice == 3:
            search_records()
        elif choice == 4:
            update_record()
        elif choice == 5:
            delete_record()
        elif choice == 6:
            calculate_total_cost()
        elif choice == 7:
            cost_breakdown()
        elif choice == 8:
            compare_farms()
        elif choice == 9:
            compare_crops()
        elif choice == 10:
            highest_cost_category()
        elif choice == 11:
            generate_report()
        elif choice == 12:
            show_suggestions()
        else:
            print("\nThank you for using Farmer Input Cost Analyzer. Goodbye!")
            break


if __name__ == "__main__":
    main()
