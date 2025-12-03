"""
generate_chart.py

This script creates a PDF called "schedule_chart.pdf" that displays schedules
with blue background blocks and overlays washing (green) and drying (orange).
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


# --- Read CSV files ---
df_base = pd.read_csv("../data/data.csv")      # name, start_time, end_time
df_results = pd.read_csv("../data/results.csv")  # Student, WashMachine, WashTime, DryMachine, DryTime, Delay


# --- Helper function to convert decimal hours to AM/PM ---
def decimal_to_ampm(decimal_hour):
    hours = int(decimal_hour)
    minutes = int(round((decimal_hour - hours) * 60))
    suffix = "AM" if hours < 12 or hours == 24 else "PM"
    display_hour = hours % 12
    if display_hour == 0:
        display_hour = 12
    return f"{display_hour}:{minutes:02d} {suffix}"


# --- Helper for x-axis ---
def hour_label(h):
    display_hour = h % 12
    if display_hour == 0:
        display_hour = 12
    suffix = "AM" if h < 12 or h == 24 else "PM"
    return f"{display_hour}{suffix}"


# Merge both dataframes on name/student
df = pd.merge(
    df_base,
    df_results,
    left_on="name",
    right_on="Student",
    how="left"
)

# Durations for wash/dry
wash_duration = 0.5
dry_duration = 0.5


# --- PDF Output ---
pdf_file = "../4_4_schedule_chart.pdf"
with PdfPages(pdf_file) as pdf:
    row_height = 0.8
    fig_height = len(df) * 1.2
    fig, ax = plt.subplots(figsize=(12, fig_height))

    # y positions
    y_positions = range(len(df))
    ax.set_yticks(y_positions)
    ax.set_yticklabels(df['name'], fontsize=12)


    # --- FIRST: Draw the big blue base blocks ---
    for i, row in df.iterrows():
        start = row['start_time']
        end = row['end_time']
        duration = end - start

        ax.barh(
            i,
            duration,
            left=start,
            height=row_height,
            edgecolor='black',
            color='skyblue'     # original blue
        )

        # Blue block label
        label = f"{decimal_to_ampm(start)}\n-\n{decimal_to_ampm(end)}"
        ax.text(start + duration / 2, i, label,
                ha='center', va='center', fontsize=10, color='black')


    # --- SECOND: Overlay wash (green) and dry (orange) over blue ---
    for i, row in df.iterrows():
        # --- Wash Block ---
        if not pd.isna(row["WashTime"]):
            wash_start = row["WashTime"]

            ax.barh(
                i,
                wash_duration,
                left=wash_start,
                height=row_height,
                edgecolor='black',
                color='green',
                zorder=3     # <-- ensures it draws ON TOP
            )

        # --- Dry Block ---
        if not pd.isna(row["DryTime"]):
            dry_start = row["DryTime"]

            ax.barh(
                i,
                dry_duration,
                left=dry_start,
                height=row_height,
                edgecolor='black',
                color='orange',
                zorder=3
            )


    # --- Formatting ---
    ax.set_xlabel("Hour of Day", fontsize=12)
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25))
    ax.set_xticklabels([hour_label(h) for h in range(0, 25)], rotation=45)

    ax.set_ylim(-0.5, len(df) - 0.5)
    ax.invert_yaxis()
    ax.set_title("Laundry Schedule Timeline", fontsize=14)

    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()

print(f"PDF saved as {pdf_file}")
