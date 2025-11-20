import csv
import random

MIN_DURATION = 2
EARLIEST_TIME = 0
LATEST_TIME = 24


def generate_times():
    possible_times = [i * 0.5 for i in range(int((LATEST_TIME - EARLIEST_TIME) / 0.5) + 1)]

    while True:
        start = random.choice(possible_times)
        end_candidates = [t for t in possible_times if t >= start + MIN_DURATION]
        if end_candidates:
            return start, random.choice(end_candidates)


def main():
    with open("names.csv", newline="") as infile, open("data.csv", "w", newline="") as outfile:
        reader = csv.reader(infile)
        header = next(reader)  # skip header

        writer = csv.writer(outfile)
        writer.writerow(["name", "start_time", "end_time"])

        for row in reader:
            name = row[0]
            start, end = generate_times()
            writer.writerow([name, start, end])


if __name__ == "__main__":
    main()
