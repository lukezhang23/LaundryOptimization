"""
generate_chart.py

This script creates a PDF called "initial_schedule_chart.pdf" that displays schedules in a graphical manner.
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# --- Read CSV ---
df = pd.read_csv("../data/data.csv")  # expects columns: name, start_time, end_time

# --- Helper function to convert decimal hours to AM/PM string ---
def decimal_to_ampm(decimal_hour):
    hours = int(decimal_hour)
    minutes = int(round((decimal_hour - hours) * 60))
    suffix = "AM" if hours < 12 or hours == 24 else "PM"
    display_hour = hours % 12
    if display_hour == 0:
        display_hour = 12
    return f"{display_hour}:{minutes:02d} {suffix}"

# --- Helper function for x-axis labels ---
def hour_label(h):
    display_hour = h % 12
    if display_hour == 0:
        display_hour = 12
    suffix = "AM" if h < 12 or h == 24 else "PM"
    return f"{display_hour}{suffix}"

# --- PDF output ---
pdf_file = "initial_schedule_chart.pdf"
with PdfPages(pdf_file) as pdf:
    # --- Plot setup ---
    row_height = 0.8
    fig_height = len(df) * 1.2
    fig, ax = plt.subplots(figsize=(12, fig_height))

    # Map names to y positions
    y_positions = range(len(df))
    ax.set_yticks(y_positions)
    ax.set_yticklabels(df['name'], fontsize=12)

    # Draw blocks with wrapped AM/PM labels
    for i, row in df.iterrows():
        start = row['start_time']
        duration = row['end_time'] - row['start_time']
        ax.barh(i, duration, left=start, height=row_height, color='skyblue', edgecolor='black')

        # Wrap label into 3 lines
        label = f"{decimal_to_ampm(start)}\n-\n{decimal_to_ampm(row['end_time'])}"
        ax.text(start + duration / 2, i, label, ha='center', va='center', fontsize=10, color='black')

    # --- Formatting ---
    ax.set_xlabel("Hour of Day", fontsize=12)
    ax.set_xlim(0, 24)
    ax.set_xticks(range(0, 25))
    ax.set_xticklabels([hour_label(h) for h in range(0, 25)], rotation=45)

    # Remove gaps at top and bottom
    ax.set_ylim(-0.5, len(df) - 0.5)
    ax.invert_yaxis()
    ax.set_title("Schedule Timeline", fontsize=14)

    plt.tight_layout()
    pdf.savefig(fig)
    plt.close()

print(f"PDF saved as {pdf_file}")
