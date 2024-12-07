"""Day 3 solutions for Advent of Code 2024.

This module contains solutions for Day 3 of the Advent of Code 2024 challenge.
It provides functions for solving both Part 1 and Part 2 of the puzzle.

Functions:
    - day_three_p1: Solves Part 1 of the puzzle.
    - day_three_p2: Solves Part 2 of the puzzle.

The solutions parse input data, perform necessary calculations, and return
results specific to the given problem description.
"""

import argparse
import re

import pandas as pd


def day_three_p1(in_file):
    """Solve Part 1 of Day 3."""
    # Load input Data
    with open(in_file) as f:
        lines = f.readlines()

    # Remove newline characters and create a DataFrame
    df = pd.DataFrame([line.strip() for line in lines], columns=["Lines"])

    def find_mul_patterns(line):
        """Function to find mul pattern."""
        # Regex for the pattern: "mul(1-3 digit#,1-3digit#)"
        pattern = r"mul\(\d{1,3},\d{1,3}\)"
        return re.findall(pattern, line)

    def compute_mul_sum(mul_list):
        """Define function to compute the sum of products from the matches."""
        total = 0
        for mul in mul_list:
            # Extract numbers from the mul pattern
            numbers = re.findall(r"\d+", mul)
            if len(numbers) == 2:
                total += int(numbers[0]) * int(numbers[1])
        return total

    # Find and Calc muls
    df["Muls"] = df["Lines"].apply(find_mul_patterns)
    df["Sum"] = df["Muls"].apply(compute_mul_sum)

    # Determin sum of muls
    total = df["Sum"].sum()
    print(f"Total is {total}")


def day_three_p2(in_file):
    """Solve Part 2 of Day 3."""
    # Load input data
    with open(in_file) as f:
        lines = f.read().replace("\n", "")

    # Regex to match "do", "don't", and mul(...) patterns
    pattern = r"(don't\(\)|do\(\)|mul\(\d{1,3},\d{1,3}\))"

    # Find all matches
    matches = re.findall(pattern, lines)
    proc_line = []
    opp_state = True
    for match in matches:
        if match == "don't()":
            opp_state = False
            continue
        elif match == "do()":
            opp_state = True
            continue
        if opp_state:
            proc_line.append(match)

    def compute_mul_sum(mul_list):
        total = 0
        for mul in mul_list:
            # Extract numbers from the mul pattern
            numbers = re.findall(r"\d+", mul)
            if len(numbers) == 2:
                total += int(numbers[0]) * int(numbers[1])
        return total

    total = compute_mul_sum(proc_line)
    print(f"Total Sum of mul with do and don't: {total}")


def main():
    """Main."""
    parser = argparse.ArgumentParser(description="Load input")
    parser.add_argument(
        "input_path", type=str, help="Path to the file containing input data"
    )
    args = parser.parse_args()
    day_three_p1(args.input_path)
    day_three_p2(args.input_path)


if __name__ == "__main__":
    main()
