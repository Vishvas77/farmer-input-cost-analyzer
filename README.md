<div align="center">


![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-3-lightgrey?logo=sqlite&logoColor=white)
![Deps](https://img.shields.io/badge/dependencies-zero-brightgreen)
![AI/ML](https://img.shields.io/badge/AI%2FML-none-red)
![GUI](https://img.shields.io/badge/GUI-tkinter%20(optional)-orange)

**The menu-driven Python + SQLite app that tells farmers where their money *actually* goes.**

*No AI. No cloud. No frameworks. Just `if` statements with agricultural dreams.* 🌾

</div>

---

## 🚜 What is this?

**Course End Project — Batch 17** · A9502 Programming for Problem Solving Laboratory · Vardhaman College of Engineering, CSE.

A farmer types in four costs — seed, fertilizer, labour, irrigation — and the app does the math nobody wants to do by hand: totals, cost breakdowns, farm-vs-farm and crop-vs-crop comparisons, highest-cost spotting, and plain-English saving suggestions. Data lives in SQLite, dignity stays intact.

## ⚡ Quickstart

```bash
# the classic (menu-driven CLI, 13 options)
python main.py

# the fancy (optional tkinter GUI — stdlib only, zero installs)
python gui.py

# load 8 REAL Tamil Nadu government reference records (optional, idempotent)
python load_real_data.py
```

System requirements: Python 3.11, and the patience of a farmer waiting for rain. 🌧️

## 📊 The sample farms, as modern art

Real numbers, straight from the database. No charts library was used — or needed.

```
F01 Rice     |█████████████████████       | Rs.37,000
F02 Cotton   |████████████████████████████| Rs.49,000
F03 Wheat    |████████████████            | Rs.28,000
F04 Tomato   |████████████████████        | Rs.36,000
F05 Maize    |█████████████               | Rs.24,000
F07 Cotton   |█████████████████████████   | Rs.45,000
```

##  the cost categories

```
Seed        |███████████                 | Rs.36,500
Fertilizer  |██████████████████          | Rs.56,500
Labour      |████████████████████████████| Rs.87,000
Irrigation  |████████████                | Rs.39,000
```

*Labour wins. Labour always wins.* 💪

## ✨ Features

- 📋 **13-option menu** — CRUD + analysis + reports, all keyboard-driven
- 🧮 **Real calculations** — totals, percentages, highest-cost detection (nothing hardcoded, the viva panel *will* check)
- ⚔️ **Comparisons** — farm vs farm, crop vs crop, highest-cost leaderboards
- 📄 **Reports** — per-farm reports with saving suggestions
- 🖥️ **Bonus GUI** — `gui.py`, tkinter, same brain as the CLI
- 🛡️ **Parameterized SQL everywhere** — Bobby Tables can't hurt us here
- ✅ **39 automated tests** — because hope is not a strategy

## 🧪 Two datasets, honestly labeled

| Tag | What it is |
|---|---|
| `[Sample Data]` | 6 assignment records (F01–F07). F07 = **₹45,000 / Labour / High**. The legend. |
| `[Government Reference Data — Tamil Nadu]` | 8 real records (TN-*) — state-average costs per hectare from the **TN Directorate of Economics and Statistics, Table XI.1** |

Source: https://www.tnagriculture.in/dashboard/report/11_01.pdf

Field mapping: `seed_cost` ← official Seed · `fertilizer_cost` ← Fertilizer+Manure total · `labour_cost` ← Human Labour total · `irrigation_cost` ← **0** (the source table reports no separate irrigation charge — recorded as 0 rather than inventing a number).

> ⚠️ On TN records, "Total Cost" = **Project Input Cost** (sum of the four project categories only), **not** the official total cost of cultivation. These are published state averages, not surveyed farms. Honesty is a feature.

## 🗂️ Project structure

```
farmer-input-cost-analyzer/
├── main.py              ← the 13-option menu (start here)
├── gui.py               ← optional tkinter frontend (the fancy hat 🎩)
├── database.py          ← SQLite CRUD, parameterized, no funny business
├── analysis.py          ← the math brain (totals, %s, classifications)
├── reports.py           ← pretty reports + provenance notes
├── validation.py        ← input bouncers (no negatives allowed 🚫)
├── sample_data.sql      ← the OGs: F01–F07
├── real_data_tn.sql     ← 8 real TN government records
├── load_sample_data.py / load_real_data.py
├── farmer_costs.db      ← SQLite, ships with all 14 records
├── report_assets/       ← architecture diagram + 12 screenshots
├── Farmer_Input_Cost_Analyzer_Report.docx  ← the full course report
├── VIVA_PREPARATION.md  ← read this the night before. trust us.
└── README.md            ← you are here. hi. 👋
```

## 🎓 Viva Survival Kit (one-liners)

- *"Why SQLite?"* → "Serverless, zero-config, and my data fits in 16 KB. Using Postgres would be like hiring a tractor to carry a sandwich."
- *"Why no AI/ML?"* → "The problem is arithmetic, not prediction. The smartest thing here is a SQL `SUM`."
- *"Did you hardcode F07's ₹45,000?"* → "Run it. Delete it. Re-add it. The number comes from addition, not from me."
- *"What happens on bad input?"* → "`validation.py` bounces negatives, letters, and empty strings before they touch the database."

## ❓ FAQ

**Q: Is there AI/ML?**
A: No. This project has never seen a neural network and it shows — proudly.

**Q: Does it run on Windows?**
A: Yes. `python main.py`. (Use `python`, not bare `py` — long story involving a haunted Python 3.13.)

**Q: Can I add my own farm?**
A: Option 3. Go wild. The database believes in you.

**Q: Why is irrigation ₹0 for Tamil Nadu records?**
A: The government source table has no separate irrigation charge. We record 0 instead of inventing data — see "honestly labeled" above.

**Q: Does it run on a potato?**
A: Only if the potato runs Python 3.11. 🥔

## 👥 Team Batch 17

- Ch Veekshana
- P Vishvas
- A Vivek

*Built with Python, SQLite, and an unreasonable amount of testing.*

## 📜 License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

```
[ ACHIEVEMENT UNLOCKED: read a README to the end ]
```

<sub>🌾 If you made it this far, the crops are proud of you. Star the repo and touch grass. 🌾</sub>

</div>
