# Viva Preparation — Farmer Input Cost Analyzer

Everything below describes the **actual code** in this project. Read the code
once alongside this file and you will be able to answer anything.

---

## 1. Project explanation (simple language)

Farmers spend money on four things: **seeds, fertilizer, labour, irrigation**.
This project is a menu-driven Python program that records those expenses for
each farm, stores them in an SQLite database, and then analyzes them: it
calculates the total cost, finds which of the four categories costs the most,
classifies the total as Low/Medium/High, compares farms and crops against each
other, prints a cost report, and suggests how to control costs.

## 2. Project workflow

1. User starts the program: `python main.py`
2. `main.py` calls `database.create_table()` so the table always exists, then
   shows a 13-option menu in a `while True` loop.
3. The user picks an option. `validation.get_menu_choice()` makes sure the
   choice is a number between 1 and 13.
4. For data entry, `validation.get_non_empty_input()` (farm ID, crop) and
   `validation.get_positive_amount()` (the four costs) validate every input.
5. `database.py` runs the SQL query (INSERT/SELECT/UPDATE/DELETE) on
   `farmer_costs.db` using `?` placeholders.
6. `analysis.py` calculates the total, highest-cost category and cost
   classification, and runs comparison queries.
7. `reports.py` formats everything into a readable report on screen, and can
   save it to a `report_<farm_id>.txt` file.
8. Option 13 breaks the loop and the program ends. The `.db` file keeps all
   data, so records are still there next time.

## 3. What each file does

| File | Role |
|---|---|
| `main.py` | The menu and all user interaction. Each menu option calls a small function (`add_record()`, `view_records()`, `compare_farms()`, …). |
| `database.py` | Opens the SQLite connection and contains every SQL query. Nothing else in the project touches SQL. |
| `analysis.py` | Pure calculations: total, highest category, Low/Medium/High classification, suggestions, and the comparison queries. |
| `reports.py` | Turns a farm's data into the formatted text report; prints it or saves it to a file. |
| `validation.py` | Three input helpers that loop until the user types valid input, so the program never crashes. |
| `load_sample_data.py` | One-time script that loads `sample_data.sql` into the database (skips farms that already exist). |
| `sample_data.sql` | Six sample `INSERT` statements (fictional data, includes the assignment's F07 Cotton sample). |
| `farmer_costs.db` | The actual SQLite database file — created automatically, persists after the program closes. |
| `requirements.txt` | States that only the Python standard library is used (no installs needed). |

## 4. The database table

```sql
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
```

- One row = one farm's expense record.
- `farm_id` is `UNIQUE` so the same farm can't be added twice by mistake.
- `created_at` fills itself in with the current date/time — the program never
  types it.
- There is **no** `total_cost` column on purpose: the total is always
  calculated from the four cost columns (in Python or in SQL). If we stored it,
  an UPDATE could leave a stale, wrong total behind. Calculating it every time
  means it can never go out of sync.

## 5. Important functions (what they do and how)

**`database.get_connection()`** — opens `farmer_costs.db` with
`sqlite3.connect()`. Every function closes its connection after use.

**`database.add_expense(...)`** — runs a parameterized `INSERT`:
```sql
INSERT INTO farm_expenses
    (farm_id, crop, seed_cost, fertilizer_cost, labour_cost, irrigation_cost)
VALUES (?, ?, ?, ?, ?, ?)
```
The `?` placeholders are filled with the values separately, so user input is
never pasted into the SQL text (this prevents SQL injection).

**`database.get_expense_by_farm(farm_id)`** — `SELECT * ... WHERE farm_id = ?`,
returns one row or `None`. Used by search/update/delete/total/breakdown/report.

**`database.search_expenses(keyword)`** — searches both farm ID and crop with
`LIKE`, so partial text like `ott` finds `Cotton`.

**`database.update_expense(...)` / `database.delete_expense(...)`** — `UPDATE`
/ `DELETE` with `WHERE farm_id = ?`. Both return `cursor.rowcount` (how many
rows changed). If it's `0`, the farm didn't exist — the program prints
"No record found".

**`analysis.calculate_total(seed, fertilizer, labour, irrigation)`** — returns
the sum of the four costs. This is the single place the total is computed, so
every feature (add, view, compare, report) uses the same formula.

**`analysis.get_highest_cost_category(...)`** — puts the four amounts in a
dictionary `{"Seed": ..., "Fertilizer": ..., "Labour": ..., "Irrigation": ...}`
and returns `max(costs, key=costs.get)` — the key with the biggest value.
On a tie, the first category in the order wins.

**`analysis.classify_cost(total)`** — `total < 25000` → `"Low"`;
`total <= 40000` → `"Medium"`; otherwise `"High"`. Limits are constants
`LOW_LIMIT` / `HIGH_LIMIT` at the top of `analysis.py`.

**`analysis.farm_cost_summary()`** — computes each farm's total **inside SQL**
(`seed_cost + fertilizer_cost + labour_cost + irrigation_cost AS total`) and
`ORDER BY total DESC`, so the most expensive farm comes first.

**`analysis.crop_comparison()`** — `GROUP BY crop` with `COUNT(*)`, `SUM(...)`
and `AVG(...)`: number of farms, total cost and average cost per crop.

**`analysis.overall_category_totals()`** — `SUM` of each of the four cost
columns across all records; the biggest sum is the highest-cost category
overall.

**`analysis.get_suggestion(category)`** — looks up a rule-based advice string
in the `SUGGESTIONS` dictionary (e.g. Labour → "Consider optimizing labour
usage and scheduling.").

**`validation.get_positive_amount(prompt)`** — loops with `try/except
ValueError`: rejects non-numbers and negative numbers, accepts zero and above.

**`reports.build_report(summary)`** — builds the whole report as one text
string (used both for printing and for saving to file, so the two can never
disagree). `reports.format_rupees(45000)` → `₹45,000`.

## 6. Important SQL queries and what they do

| Query | Purpose |
|---|---|
| `CREATE TABLE IF NOT EXISTS farm_expenses (...)` | Creates the table once; safe to run every startup |
| `INSERT INTO farm_expenses (...) VALUES (?, ?, ?, ?, ?, ?)` | Adds one record |
| `SELECT * FROM farm_expenses ORDER BY id` | View all records |
| `SELECT * FROM farm_expenses WHERE farm_id = ?` | Fetch one farm (used by 6 features) |
| `SELECT * FROM farm_expenses WHERE farm_id LIKE ? OR crop LIKE ?` | Search by farm or crop |
| `UPDATE farm_expenses SET crop=?, ... WHERE farm_id=?` | Update a record |
| `DELETE FROM farm_expenses WHERE farm_id=?` | Delete a record |
| `SELECT farm_id, crop, seed_cost+fertilizer_cost+labour_cost+irrigation_cost AS total FROM farm_expenses ORDER BY total DESC` | Farm comparison, totals computed in SQL |
| `SELECT crop, COUNT(*), SUM(...), AVG(...) FROM farm_expenses GROUP BY crop ORDER BY total DESC` | Crop comparison |
| `SELECT SUM(seed_cost), SUM(fertilizer_cost), SUM(labour_cost), SUM(irrigation_cost) FROM farm_expenses` | Highest-cost category overall |
| `SELECT COUNT(*) FROM farm_expenses` | Checks whether the database is empty |

## 7. The 30-second explanation

> "Farmer Input Cost Analyzer is a menu-driven Python program with an SQLite
> database. It records what each farm spends on seeds, fertilizer, labour and
> irrigation, calculates the total cost, finds the biggest cost category,
> classifies the cost as Low, Medium or High, compares farms and crops using
> SQL aggregation, and generates a cost report with a cost-control suggestion."

## 8. The 2-minute explanation

> "The problem is that farmers don't know which input — seeds, fertilizer,
> labour or irrigation — drives their production cost. My project solves this
> with a simple CLI app. The user picks from a 13-option menu to add, view,
> search, update or delete farm expense records, which are stored in an SQLite
> table called farm_expenses.
>
> For every record the program calculates total input cost as the sum of the
> four costs, finds the highest-cost category, and classifies the total as
> Low, Medium or High using fixed thresholds. Comparisons are done partly in
> SQL — for example, farm totals are computed with an SQL expression and
> ordered descending, and crop comparison uses GROUP BY with SUM and AVG.
>
> Finally it generates a formatted cost report with a rule-based suggestion,
> like optimizing labour scheduling when labour is the highest cost. All input
> is validated so the program never crashes, all SQL uses parameterized
> queries, and everything is plain Python with no external libraries."

## 9. Explain the DBMS part

> "I used SQLite because it's a real relational database that needs no server
> and stores everything in one file, farmer_costs.db, which persists after the
> program closes. The table farm_expenses has a primary key id, a unique
> farm_id, crop name, the four cost columns as REAL, and an auto-filled
> timestamp. The project demonstrates CREATE TABLE, INSERT, SELECT with WHERE,
> LIKE, ORDER BY, GROUP BY, and aggregate functions SUM, AVG, COUNT — for
> example, crop comparison is a GROUP BY query and the highest-cost category
> uses SUM on each cost column. All queries are parameterized with ?
> placeholders, so user input can't inject SQL."

## 10. Explain the Python part

> "The Python code is procedural and split into five modules: main.py handles
> the menu loop and user interaction; database.py owns all SQLite operations;
> analysis.py does the calculations; reports.py formats output; validation.py
> validates input. I used functions, if/else, loops, dictionaries — for
> example the highest-cost category is found with max() over a dictionary of
> the four costs — and try/except for input validation. No classes, no
> frameworks, no external libraries; only the sqlite3 module from the standard
> library."

## 11. Thirty likely viva questions

1. **What does your project do?** — Records farm input expenses (seed,
   fertilizer, labour, irrigation) in SQLite and analyzes which category costs
   the most, with farm/crop comparisons and a cost report.
2. **How is the total input cost calculated?** — `calculate_total()` in
   `analysis.py` returns `seed + fertilizer + labour + irrigation`. One
   function, used everywhere, so it's always consistent.
3. **How do you find the highest-cost category?** — The four amounts go into a
   dictionary and `max(costs, key=costs.get)` returns the key with the largest
   value. Ties go to the first category in Seed/Fertilizer/Labour/Irrigation
   order.
4. **How does cost classification work?** — `classify_cost()`: below ₹25,000
   is Low, ₹25,000–₹40,000 is Medium, above ₹40,000 is High. The limits are
   constants `LOW_LIMIT`/`HIGH_LIMIT`.
5. **Verify with the sample: F07 Cotton 8000/12000/18000/7000.** —
   Total = 45,000; largest is Labour (18,000); 45,000 > 40,000 → High. The
   program computes this, nothing is hardcoded.
6. **Why SQLite?** — Serverless, single-file database, zero setup, persists
   data between runs, and supports real SQL including GROUP BY and aggregates.
7. **What is the table schema?** — `farm_expenses(id, farm_id UNIQUE, crop,
   seed_cost, fertilizer_cost, labour_cost, irrigation_cost, created_at)`.
8. **Why is there no total_cost column?** — It's always calculated from the
   four cost columns, so it can never become stale after an UPDATE.
9. **What SQL operations did you demonstrate?** — CREATE TABLE, INSERT,
   SELECT, UPDATE, DELETE, WHERE, LIKE, ORDER BY, GROUP BY, SUM, AVG, COUNT.
10. **How do you prevent SQL injection?** — Every query uses `?` placeholders;
    values are passed separately, never concatenated into the SQL string.
11. **How does search work?** — `WHERE farm_id LIKE ? OR crop LIKE ?` with
    `%keyword%`, so partial matches work on both fields.
12. **How do you compare farms?** — `farm_cost_summary()` selects each farm
    with the total computed in SQL (`seed_cost + ... AS total`) and
    `ORDER BY total DESC`; the first row is the highest-cost farm.
13. **How do you compare crops?** — `GROUP BY crop` with `COUNT(*)`,
    `SUM(total)` and `AVG(total)` per crop, ordered by total descending.
14. **How do you find the highest-cost category across all farms?** —
    `SELECT SUM(seed_cost), SUM(fertilizer_cost), SUM(labour_cost),
    SUM(irrigation_cost)` and take the maximum of the four sums.
15. **What does `cursor.rowcount` tell you?** — How many rows an UPDATE/DELETE
    changed; `0` means the farm ID didn't exist, so the program prints "No
    record found".
16. **How is invalid input handled?** — `validation.py`: empty text is
    rejected, costs must be numbers ≥ 0 (try/except ValueError), menu choice
    must be an integer 1–13. Each helper loops until input is valid.
17. **What happens on an empty database?** — `count_records()` returns 0, and
    `has_records()` in main.py prints "No records found. Please add a record
    first" instead of running the analysis.
18. **How is the report generated?** — `build_report()` assembles the text
    from a summary dict; `print_report()` shows it, `save_report()` writes the
    same string to `report_<farm_id>.txt`.
19. **How are cost-control suggestions decided?** — Rule-based: a `SUGGESTIONS`
    dictionary maps each highest-cost category to one advice string.
20. **What does `record_to_summary()` do?** — Converts a raw DB row tuple into
    a dictionary with calculated fields (`total`, `highest`, `category`) added.
21. **Why split the code into five files?** — Separation of concerns: menu/UI,
    database, calculations, reporting, validation. Easier to explain and test
    each part alone.
22. **Where does the data go when the program closes?** — It stays in
    `farmer_costs.db`; SQLite writes to disk on `commit()`, and the file is
    reopened on the next run.
23. **What is `IF NOT EXISTS` for?** — Lets `create_table()` run safely on
    every startup without erasing existing data.
24. **Why is `farm_id` UNIQUE?** — Prevents duplicate farm records; the Add
    option checks `farm_exists()` and tells the user to use Update instead.
25. **What does the loader script do?** — `load_sample_data.py` reads
    `sample_data.sql` and runs the INSERTs with `INSERT OR IGNORE`, so
    re-running it never creates duplicates.
26. **How would you add a fifth cost category, say pesticides?** — Add a
    `pesticide_cost` column, include it in the INSERT/UPDATE, add it to
    `CATEGORIES`, `calculate_total()`, and the SQL total expressions.
27. **How would you change the Low/Medium/High limits?** — Edit `LOW_LIMIT`
    and `HIGH_LIMIT` at the top of `analysis.py`; everything else follows.
28. **What would you improve next?** — CSV export, month-wise tracking, or a
    simple chart of category shares.
29. **Did you use any AI/ML or web framework?** — No. Plain Python + SQLite,
    standard library only, as required for a Python course project.
30. **What was the hardest bug you fixed?** — The sample-data loader skipped
    the first INSERT because comment lines were removed per chunk instead of
    per line; fixed by stripping comment lines from the whole file before
    splitting on `;`. (Also: always test with real runs, not just reading code.)

## 12. Common professor questions (and how to handle them)

- **"Show me it working."** → Run `python main.py`, use option 2 (view), 8
  (compare farms), 11 (report for F07). Have `load_sample_data.py` already run.
- **"Change something live."** → See section 13; the easiest are thresholds
  and suggestions.
- **"Why didn't you use MySQL?"** → SQLite needs no server setup and the
  whole DB is one portable file — ideal for a course project; SQL used is
  standard and transferable.
- **"Is the output hardcoded?"** → No: delete a record or change a cost via
  option 4 and re-run the report — every number changes accordingly. The F07
  sample passes through the same `calculate_total()` as everything else.

## 13. Live modifications a professor may ask for

1. **Add a new farm record** — option 1; shows validation (try a negative cost
   to demo the error handling).
2. **Change classification thresholds** — edit `LOW_LIMIT`/`HIGH_LIMIT` in
   `analysis.py`, re-run option 11 and watch the Category change.
3. **Add a suggestion for a new category** — add an entry to `SUGGESTIONS`.
4. **Show records sorted differently** — change `ORDER BY total DESC` to `ASC`
   in `farm_cost_summary()` and re-run option 8.
5. **Filter by crop in SQL** — run in a Python shell:
   `SELECT * FROM farm_expenses WHERE crop = 'Cotton';`
6. **Delete and re-add** — options 5 then 1; proves the DB file persists.

## 14. Data Source and Provenance (Sample vs Government Reference Data)

The project works with **two clearly distinguished datasets**:

1. **Assignment / Sample Data** — six fictional farms (F01–F07) from
   `sample_data.sql`, loaded by `load_sample_data.py`. Realistic but invented
   values, including the assignment's required F07 Cotton sample. These ship
   in `farmer_costs.db`.
2. **Government Reference Data — Tamil Nadu** — eight real records
   (`real_data_tn.sql`, loaded by `load_real_data.py`) from the Directorate
   of Economics and Statistics, Tamil Nadu, Table "XI.1: Cost of Cultivation
   for Principal Agricultural Crops"
   (https://www.tnagriculture.in/dashboard/report/11_01.pdf), in rupees per
   hectare (state averages).

**Field mapping (government data):** `seed_cost` ← official "IV Seed";
`fertilizer_cost` ← official "V Fertilizer & Manure" total;
`labour_cost` ← official "I Human Labour" total;
`irrigation_cost` ← 0, because the source table reports no separate
irrigation charge (Tamil Nadu provides free farm electricity) — recorded as
0 rather than inventing a number.

**Fields omitted** (in the official table, outside the four-category schema):
bullock labour, machine labour, insecticides, interest on working capital,
and fixed costs (land rent, land revenue, depreciation, interest on fixed
capital).

**Terminology:** the program's "Total Cost" for these records is the
**"Project Input Cost"** (sum of the four project categories only). It is NOT
the official total cost of cultivation. Generated reports for TN records
carry a provenance note saying exactly this.

**How the app distinguishes them:** `analysis.get_data_source(farm_id)`
labels farm IDs starting with `TN-` as "Government Reference Data —
Tamil Nadu" and everything else as "Sample Data"; the label appears on every
record listing, and TN reports include the provenance note.

**Explicit statement (say this in viva):** the TN figures are published
crop-level averages/reference values from a government table — NOT
individual surveyed farms, NOT our own field survey — used only to
validate/demonstrate that the implementation works on real data.

### Provenance questions a professor may ask

- **"Where did the government data come from?"** → TN Directorate of
  Economics and Statistics, Table XI.1 (URL in `real_data_tn.sql` header);
  I downloaded the table and mapped its rows to the schema — the mapping is
  documented in the SQL file's comments.
- **"Are these real farms you surveyed?"** → No — they are state-average
  costs per hectare for 8 crops (Paddy, Sorghum, Maize, Black gram,
  Groundnut, Gingelly, Cotton, Sugarcane). The farm IDs (`TN-PADDY` etc.)
  and the on-screen labels make this explicit.
- **"Why is irrigation zero for all government records?"** → The source
  table has no separate irrigation charge; Tamil Nadu gives free farm
  electricity. I recorded 0 and documented why, instead of making up a
  number.
- **"Is ₹1,80,624 the official total cost of sugarcane cultivation?"** →
  No — it is the Project Input Cost (seed + fertilizer&manure + labour +
  0 irrigation). The official total (₹2,77,275 in the source) adds machine
  labour, insecticides, fixed costs, etc., which are outside our schema.
- **"Why keep the fictional data at all?"** → The assignment requires the
  F07 sample (₹45,000 / Labour / High); the fictional set also gives
  different highest-cost categories per farm, which the government set
  doesn't (labour dominates all 8 TN crops).
- **"How do I know you didn't invent the TN numbers?"** → Every value is
  traceable: the SQL file cites the exact table rows ("IV Seed", "V
  Fertilizer & Manure" total, "I Human Labour" total), and the PDF is public
  at the documented URL.
