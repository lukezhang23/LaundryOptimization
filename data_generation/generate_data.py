"""
generate_data.py

This script creates a CSV in the project root folder called "data.csv".
It uses names from "seed/names.csv" and generates their start and end times
You can set weights for times in "seed/start_time_weights.csv" and "seed/length_weights.csv".
"""

import csv
import random
import pandas as pd
import numpy as np
import os

MIN_DURATION = 2
EARLIEST_TIME = 0
LATEST_TIME = 24

# --- Weighted selection helper ---
def pick_weighted_with_half(df, col_name):
    """
    Pick a weighted random value from df[col_name], allowing 0.5 increments.
    Assumes df has columns: col_name, weight
    """
    choices = []
    weights = []
    for _, row in df.iterrows():
        base = row[col_name]
        w = row['weight']
        # Add base and base+0.5
        choices.extend([base, base + 0.5])
        weights.extend([w, w])
    weights = np.array(weights)
    weights = weights / weights.sum()  # normalize
    return np.random.choice(choices, p=weights)

# --- Generate a random start/end time with optional weights ---
def generate_times(start_weights=None, length_weights=None):
    possible_times = [i * 0.5 for i in range(int((LATEST_TIME - EARLIEST_TIME) / 0.5) + 1)]

    if start_weights is not None and length_weights is not None:
        while True:
            start = pick_weighted_with_half(start_weights, "hour")
            length = pick_weighted_with_half(length_weights, "length")
            end = start + length
            if end <= LATEST_TIME and length >= MIN_DURATION:
                return start, end
    else:
        # fallback to uniform random as before
        while True:
            start = random.choice(possible_times)
            end_candidates = [t for t in possible_times if t >= start + MIN_DURATION]
            if end_candidates:
                return start, random.choice(end_candidates)


def main():
    # Load optional weights CSVs if they exist
    start_weights = None
    length_weights = None
    if os.path.exists("seed/start_time_weights.csv") and os.path.exists("seed/length_weights.csv"):
        start_weights = pd.read_csv("seed/start_time_weights.csv")
        length_weights = pd.read_csv("seed/length_weights.csv")

    with open("seed/names.csv", newline="") as infile, open("../data/data.csv", "w", newline="") as outfile:
        reader = csv.reader(infile)
        header = next(reader)  # skip header

        writer = csv.writer(outfile)
        writer.writerow(["name", "start_time", "end_time"])

        for row in reader:
            name = row[0]
            start, end = generate_times(start_weights, length_weights)
            writer.writerow([name, start, end])


if __name__ == "__main__":
    main()
