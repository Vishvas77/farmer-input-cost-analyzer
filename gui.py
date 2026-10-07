# gui.py — Optional basic desktop frontend (tkinter, standard library only)
#
# This is a DEMO EXTRA, not part of the submitted coursework. The submitted
# project is the menu-driven CLI (main.py). This file only *displays* and
# *calls* the existing modules — all calculations still happen in
# analysis.py and all data access still goes through database.py.
#
# Run with:  python gui.py

import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog, ttk

import analysis
import database


def rupees(value):
    """Format a number as Indian rupees, e.g. 45000 -> ₹45,000."""
    return f"₹{int(value):,}"


def selected_farm_id(tree):
    """Return the farm_id of the highlighted table row, or None."""
    chosen = tree.selection()
    if not chosen:
        messagebox.showwarning("No selection", "Please select a farm row first.")
        return None
    return tree.item(chosen[0])["values"][0]


def refresh_table(tree):
    """Reload every record from the database into the table."""
    for row in tree.get_children():
        tree.delete(row)
    for record in database.get_all_expenses():
        summary = analysis.record_to_summary(record)
        tree.insert("", "end", values=(
            summary["farm_id"],
            summary["crop"],
            rupees(summary["seed"]),
            rupees(summary["fertilizer"]),
            rupees(summary["labour"]),
            rupees(summary["irrigation"]),
            rupees(summary["total"]),
            summary["highest"],
            summary["category"],
            analysis.get_data_source(summary["farm_id"]),
        ))


def show_output(output_box, text):
    """Display text in the read-only output panel."""
    output_box.config(state="normal")
    output_box.delete("1.0", "end")
    output_box.insert("1.0", text)
    output_box.config(state="disabled")


def record_form(parent, title, initial=None):
    """Pop-up form for adding / updating a record. Returns a dict or None."""
    initial = initial or {}
    fields = ["Farm ID", "Crop", "Seed Cost", "Fertilizer Cost",
              "Labour Cost", "Irrigation Cost"]
    keys = ["farm_id", "crop", "seed", "fertilizer", "labour", "irrigation"]
    entries = {}
    result = {}

    window = tk.Toplevel(parent)
    window.title(title)
    window.resizable(False, False)

    for i, field in enumerate(fields):
        tk.Label(window, text=field + ":").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(window, width=30)
        entry.grid(row=i, column=1, padx=10, pady=5)
        if field in initial:
            entry.insert(0, str(initial[field]))
        entries[keys[i]] = entry
    if initial:  # updating: farm id identifies the row, so lock it
        entries["farm_id"].config(state="disabled")

    def on_save():
        data = {k: e.get().strip() for k, e in entries.items()}
        if not data["farm_id"] or not data["crop"]:
            messagebox.showerror("Invalid input", "Farm ID and Crop are required.")
            return
        try:
            for cost_key in ("seed", "fertilizer", "labour", "irrigation"):
                data[cost_key] = float(data[cost_key])
                if data[cost_key] < 0:
                    raise ValueError
        except ValueError:
            messagebox.showerror("Invalid input", "All four costs must be numbers ≥ 0.")
            return
        result.update(data)
        window.destroy()

    tk.Button(window, text="Save", width=12, command=on_save).grid(
        row=len(fields), column=0, padx=10, pady=10)
    tk.Button(window, text="Cancel", width=12,
              command=window.destroy).grid(row=len(fields), column=1, padx=10, pady=10)

    parent.wait_window(window)
    return result or None


def add_record(root, tree, output_box):
    data = record_form(root, "Add Farm Record")
    if not data:
        return
    if database.farm_exists(data["farm_id"]):
        messagebox.showerror("Duplicate", f"Farm '{data['farm_id']}' already exists.")
        return
    database.add_expense(data["farm_id"], data["crop"], data["seed"],
                         data["fertilizer"], data["labour"], data["irrigation"])
    refresh_table(tree)
    show_output(output_box, f"Record '{data['farm_id']}' added successfully.")


def update_record(root, tree, output_box):
    farm_id = selected_farm_id(tree)
    if not farm_id:
        return
    record = database.get_expense_by_farm(farm_id)
    summary = analysis.record_to_summary(record)
    data = record_form(root, f"Update {farm_id}", {
        "Farm ID": summary["farm_id"], "Crop": summary["crop"],
        "Seed Cost": summary["seed"], "Fertilizer Cost": summary["fertilizer"],
        "Labour Cost": summary["labour"], "Irrigation Cost": summary["irrigation"],
    })
    if not data:
        return
    database.update_expense(farm_id, data["crop"], data["seed"],
                            data["fertilizer"], data["labour"], data["irrigation"])
    refresh_table(tree)
    show_output(output_box, f"Record '{farm_id}' updated successfully.")


def delete_record(tree, output_box):
    farm_id = selected_farm_id(tree)
    if not farm_id:
        return
    if messagebox.askyesno("Confirm", f"Delete record '{farm_id}'?"):
        database.delete_expense(farm_id)
        refresh_table(tree)
        show_output(output_box, f"Record '{farm_id}' deleted.")


def cost_breakdown(tree, output_box):
    farm_id = selected_farm_id(tree)
    if not farm_id:
        return
    s = analysis.record_to_summary(database.get_expense_by_farm(farm_id))
    total = s["total"] or 1  # avoid dividing by zero
    lines = [f"--- Cost Breakdown: {farm_id} ({s['crop']}) ---",
             f"Source: {analysis.get_data_source(farm_id)}", ""]
    for label, key in (("Seed", "seed"), ("Fertilizer", "fertilizer"),
                       ("Labour", "labour"), ("Irrigation", "irrigation")):
        lines.append(f"{label:<12}: {rupees(s[key]):>12}  ({s[key] / total * 100:.1f}%)")
    lines += ["", f"Total Input Cost : {rupees(s['total'])}",
              f"Highest Cost     : {s['highest']}",
              f"Category         : {s['category']}"]
    show_output(output_box, "\n".join(lines))


def farmer_report(tree, output_box):
    farm_id = selected_farm_id(tree)
    if not farm_id:
        return
    s = analysis.record_to_summary(database.get_expense_by_farm(farm_id))
    lines = [f"--- Farm Report: {farm_id} ---",
             f"Crop             : {s['crop']}",
             f"Seed Cost        : {rupees(s['seed'])}",
             f"Fertilizer Cost  : {rupees(s['fertilizer'])}",
             f"Labour Cost      : {rupees(s['labour'])}",
             f"Irrigation Cost  : {rupees(s['irrigation'])}",
             f"Total Input Cost : {rupees(s['total'])}",
             f"Highest Cost     : {s['highest']}",
             f"Category         : {s['category']}"]
    if farm_id.startswith("TN-"):
        lines += ["", "Data Source : Government Reference Data — Tamil Nadu",
                  "              (state-average cost per hectare; TN DES Table XI.1)",
                  "Note        : 'Total Cost' above is the Project Input Cost",
                  "              (sum of the four project categories only),",
                  "              not the official total cost of cultivation."]
    show_output(output_box, "\n".join(lines))


def suggestions(tree, output_box):
    farm_id = selected_farm_id(tree)
    if not farm_id:
        return
    s = analysis.record_to_summary(database.get_expense_by_farm(farm_id))
    tip = analysis.get_suggestion(s["highest"])
    show_output(output_box,
                f"--- Suggestion: {farm_id} ---\n"
                f"Highest cost category: {s['highest']}\n\n{tip}")


def compare_farms(root, tree, output_box):
    farm1 = simpledialog.askstring("Compare Farms", "First Farm ID:", parent=root)
    farm2 = simpledialog.askstring("Compare Farms", "Second Farm ID:", parent=root)
    if not farm1 or not farm2:
        return
    rows = []
    for farm_id in (farm1.strip(), farm2.strip()):
        record = database.get_expense_by_farm(farm_id)
        if record is None:
            messagebox.showerror("Not found", f"Farm '{farm_id}' does not exist.")
            return
        rows.append(analysis.record_to_summary(record))
    a, b = rows
    lines = [f"--- Farm Comparison: {a['farm_id']} vs {b['farm_id']} ---", ""]
    for label, key in (("Crop", "crop"), ("Total Input Cost", "total"),
                       ("Highest Cost", "highest"), ("Category", "category")):
        va, vb = a[key], b[key]
        if key == "total":
            va, vb = rupees(va), rupees(vb)
        lines.append(f"{label:<16}: {a['farm_id'] + ' = ' + str(va):<28} | "
                     f"{b['farm_id']} = {vb}")
    winner = a if a["total"] >= b["total"] else b
    lines += ["", f"Higher total cost: {winner['farm_id']} ({rupees(winner['total'])})"]
    show_output(output_box, "\n".join(lines))


def compare_crops(output_box):
    totals = {}
    for record in database.get_all_expenses():
        s = analysis.record_to_summary(record)
        totals[s["crop"]] = totals.get(s["crop"], 0) + s["total"]
    lines = ["--- Crop Comparison (total input cost across records) ---", ""]
    for crop, total in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
        lines.append(f"{crop:<12}: {rupees(total)}")
    show_output(output_box, "\n".join(lines))


def highest_costs(output_box):
    totals = analysis.overall_category_totals()  # dict: category -> total
    top_cat = max(totals, key=lambda c: totals[c])
    farms = [analysis.record_to_summary(r) for r in database.get_all_expenses()]
    top_farm = max(farms, key=lambda s: s["total"])
    lines = ["--- Highest Costs ---", ""]
    for category, total in totals.items():
        lines.append(f"{category:<12}: {rupees(total)}")
    lines += ["",
              f"Highest-cost category: {top_cat} ({rupees(totals[top_cat])})",
              f"Highest-cost farm    : {top_farm['farm_id']} ({top_farm['crop']}) "
              f"at {rupees(top_farm['total'])}"]
    show_output(output_box, "\n".join(lines))


def load_tn_data(tree, output_box):
    """Run the existing government-data loader script and show its output."""
    proc = subprocess.run([sys.executable, "load_real_data.py"],
                          capture_output=True, text=True)
    refresh_table(tree)
    show_output(output_box, (proc.stdout or "") + (proc.stderr or "")
                or "Loader finished.")


def main():
    database.create_table()

    root = tk.Tk()
    root.title("Farmer Input Cost Analyzer")
    root.geometry("1100x700")

    tk.Label(root, text="Farmer Input Cost Analyzer",
             font=("Arial", 16, "bold")).pack(pady=8)

    columns = ("Farm ID", "Crop", "Seed", "Fertilizer", "Labour",
               "Irrigation", "Total", "Highest", "Category", "Source")
    tree = ttk.Treeview(root, columns=columns, show="headings", height=12)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100 if col != "Source" else 220)
    tree.pack(fill="x", padx=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=8)
    buttons = [
        ("Refresh", lambda: refresh_table(tree)),
        ("Add", lambda: add_record(root, tree, out)),
        ("Update", lambda: update_record(root, tree, out)),
        ("Delete", lambda: delete_record(tree, out)),
        ("Breakdown", lambda: cost_breakdown(tree, out)),
        ("Report", lambda: farmer_report(tree, out)),
        ("Suggestions", lambda: suggestions(tree, out)),
        ("Compare Farms", lambda: compare_farms(root, tree, out)),
        ("Compare Crops", lambda: compare_crops(out)),
        ("Highest Costs", lambda: highest_costs(out)),
        ("Load TN Govt Data", lambda: load_tn_data(tree, out)),
    ]
    for i, (label, command) in enumerate(buttons):
        tk.Button(button_frame, text=label, width=14,
                  command=command).grid(row=i // 6, column=i % 6, padx=4, pady=4)

    tk.Label(root, text="Output:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
    out = scrolledtext.ScrolledText(root, height=12, state="disabled")
    out.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    refresh_table(tree)
    root.mainloop()


if __name__ == "__main__":
    main()
