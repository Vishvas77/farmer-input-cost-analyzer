# reports.py
# Builds the farmer input cost report.
# A report is first built as plain text, then it can be printed
# on screen or saved to a .txt file.

import analysis


def format_rupees(amount):
    """Format a number as Indian rupees, e.g. 45000 -> ₹45,000."""
    return f"₹{amount:,.0f}"


def build_report(summary):
    """Build the full report text for one farm's summary dict.

    Records from the Government Reference Data (farm IDs starting with
    'TN-') get an extra provenance block so the report never implies they
    are individual surveyed farms, and so the 'Total Cost' is not mistaken
    for the official total cost of cultivation. Sample-data reports are
    left exactly as specified in the assignment.
    """
    line = "-" * 45
    suggestion = analysis.get_suggestion(summary["highest"])
    provenance = ""
    if summary["farm_id"].startswith("TN-"):
        provenance = (
            f"\n"
            f"Data Source   : Government Reference Data \u2014 Tamil Nadu\n"
            f"                (state-average cost per hectare;\n"
            f"                 TN DES Table XI.1)\n"
            f"Note          : 'Total Cost' above is the Project Input Cost\n"
            f"                (sum of the four project categories only),\n"
            f"                not the official total cost of cultivation.\n"
        )
    report = (
        f"{line}\n"
        f"FARMER INPUT COST REPORT\n"
        f"{line}\n\n"
        f"Farm ID       : {summary['farm_id']}\n"
        f"Crop          : {summary['crop']}\n\n"
        f"Seed          : {format_rupees(summary['seed'])}\n"
        f"Fertilizer    : {format_rupees(summary['fertilizer'])}\n"
        f"Labour        : {format_rupees(summary['labour'])}\n"
        f"Irrigation    : {format_rupees(summary['irrigation'])}\n\n"
        f"{line}\n"
        f"Total Cost    : {format_rupees(summary['total'])}\n"
        f"Highest Cost  : {summary['highest']}\n"
        f"Category      : {summary['category']}\n"
        f"{line}\n"
        f"{provenance}\n"
        f"Suggestion:\n"
        f"{suggestion}\n"
    )
    return report


def print_report(summary):
    """Display the report on the terminal."""
    print()
    print(build_report(summary))


def save_report(summary, filename):
    """Save the report text to a file. Returns the filename."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(build_report(summary))
    return filename
